# Machine Learning Project Report: Agriculture Crop Yield Prediction

**Student Name:** [Your Name]  
**Course / Subject:** [Course Name]  
**Date:** [Submission Date]  

---

## 1. Introduction
The objective of this project was to build a supervised machine learning model capable of predicting agriculture crop yield (measured in tons per hectare). Utilizing the Kaggle "Agriculture Crop Yield" dataset, the project investigates how various environmental and agricultural factors such as **Rainfall**, **Temperature**, **Soil Type**, and **Weather Conditions** influence the final yield of crops like Wheat, Rice, and Maize.

This project gave me hands-on experience in the complete data science lifecycle, from data preprocessing to model training and evaluation.

## 2. Stages of Project Creation

### Stage 1: Data Collection & Loading
I utilized the `pandas` library to load the dataset (`crop_yield.csv`). By examining the data structure (`df.head()`), I identified the target variable (`Yield_tons_per_hectare`) and separated it from the input features (the conditions leading to the yield).

### Stage 2: Data Preprocessing
Machine learning algorithms only understand numbers. Since the dataset contained both numerical and categorical text data, I built a preprocessing pipeline using `scikit-learn`:
- **Categorical Data (Text):** Features like `Region`, `Soil_Type`, `Crop`, and `Weather_Condition` were converted into numbers using a technique called **One-Hot Encoding**. This creates distinct 1s and 0s for each category.
- **Numerical Data:** Features like `Rainfall_mm` and `Temperature_Celsius` operate on vastly different scales. I applied a **StandardScaler** to normalize these values so that large numbers (like 1500mm of rainfall) don't overpower smaller numbers (like 25 degrees Celsius).

### Stage 3: Splitting the Data
To verify that the model doesn't just memorize the data, I used `train_test_split` to divide the dataset:
- **Training Set (80%):** Given to the model to learn the patterns.
- **Testing Set (20%):** Kept hidden from the model to evaluate its real-world accuracy later.

### Stage 4: Model Training
I selected a supervised machine learning algorithm to train on the 80% training dataset. 

### Stage 5: Evaluation and Feature Importance
Once trained, the model was tested on the remaining 20% of the data. I compared the model's predictions with the actual known crop yields to calculate our error margins. The model also calculated which features played the most important roles in predicting yield (Feature Importance).

## 3. The Model Used: Random Forest Regressor

For this project, I used a **Random Forest Regressor**. 

**What is a Random Forest?**
As a beginner, the easiest way to understand a Random Forest is to imagine asking a single expert for advice—that's called a *Decision Tree*. A Decision Tree asks a series of yes/no questions (e.g., "Is the rainfall > 500mm?") to reach a conclusion.
However, a single expert might be biased. A **Random Forest** is an "ensemble" (a collection) of hundreds of different Decision Trees. By averaging the predictions of all these trees, the Random Forest produces a highly accurate and stable prediction.

**Parameters Used:**
- `n_estimators = 100`: The model builds exactly 100 separate decision trees and averages their final yield predictions.
- `random_state = 42`: This ensures reproducibility. It forces the computer to make the exact same random choices every time the script runs, ensuring the results don't randomly change for the professor or grader.

## 4. Accuracy and Evaluation Metrics
Because this is a **Regression** problem (predicting a continuous number, the crop yield), we do not use "percentage accuracy." Instead, we measure the error distance. Our script evaluates the model using the following metrics:

1. **Mean Absolute Error (MAE):** On average, this shows exactly how many tons per hectare our prediction was off by. 
2. **Mean Squared Error (MSE) & RMSE:** This penalizes the model heavily if it makes a very large mistake on a single crop calculation. 
3. **R-squared ($R^2$) Score:** This represents how much of the variance in crop yield is successfully explained by our model. A score of `1.0` is perfect prediction, while `0.0` is a random guess. 

**Final Model Performance:**
- **MAE:** 0.4120
- **MSE:** 0.2667
- **RMSE:** 0.5165
- **R-squared Score:** 0.9075 (90.75% accuracy)

*This means the model can predict the crop yield with 90.75% accuracy, and on average, the predictions are only off by 0.41 tons per hectare.*

## 5. What I Learned
Through this project, I gained practical skills in:
- Connecting data science theory to an actual, real-world Python implementation.
- How to handle mixed data types (numbers and text) using `ColumnTransformer` and `Pipelines`.
- The difference between classification (predicting a category) and regression (predicting an exact number), and why we use error metrics instead of "accuracy percentages" for regression.
- How powerful Random Forests are out-of-the-box for tabular data sets.
