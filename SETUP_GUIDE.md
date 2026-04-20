# AgriPredict Setup Guide

## ✅ What You Have

Your AgriPredict project now includes:

1. **Backend Server** (`app.py`)
   - Flask REST API for predictions
   - Model training and retraining
   - Metrics tracking

2. **Frontend Website** (`agripredict.html`)
   - Beautiful, responsive interface
   - Prediction interface
   - Data visualization with charts
   - Model retraining interface
   - Project information

3. **Data** (`crop_yield.csv`)
   - Training dataset with ~1 million records
   - 9 input features and 1 target variable

## 🚀 Getting Started - Step by Step

> Recommended: Use Python 3.14 (64-bit) for best compatibility with `pandas` and `numpy` on Windows.

### Windows Users

#### Option 1: Simple Batch File (Easiest)
1. Navigate to the project folder in File Explorer
2. Double-click `run_server.bat`
3. A command prompt will open and start the server
4. Open your browser and go to: http://localhost:5000

#### Option 2: Command Prompt
1. Open Command Prompt (Win+R, type `cmd`, press Enter)
2. Navigate to the project folder:
   ```cmd
   cd C:\Users\dell\Downloads\archive
   ```
3. Create a virtual environment:
   ```cmd
   python -m venv .venv
   ```
4. Activate the virtual environment:
   ```cmd
   .\.venv\Scripts\activate
   ```
5. Install dependencies (first time only):
   ```cmd
   python -m pip install --upgrade pip setuptools wheel
   python -m pip install -r requirements.txt
   ```
6. Run the server:
   ```cmd
   python app.py
   ```
7. Open browser: http://localhost:5000

#### Option 3: Windows Launcher Script
1. Open Command Prompt
2. Navigate to project folder
3. Run:
   ```cmd
   setup_venv.bat
   ```
4. After setup completes, run:
   ```cmd
   run_server.bat
   ```

### macOS/Linux Users

1. Open Terminal
2. Navigate to project folder:
   ```bash
   cd ~/Downloads/archive
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the server:
   ```bash
   python app.py
   ```
5. Open browser: http://localhost:5000

## 🎮 Using the Website

### Tab 1: 🔮 Predict Yield
1. **Fill in the form** with your farm conditions:
   - Select crop type (Wheat, Rice, Maize, etc.)
   - Select region (North, South, East, West)
   - Select soil type (Loam, Clay, Sandy, etc.)
   - Set rainfall (100-1000mm using slider)
   - Set temperature (15-40°C using slider)
   - Set days to harvest (60-149 days)
   - Toggle fertilizer usage (Yes/No)
   - Toggle irrigation usage (Yes/No)

2. **Click "⚡ Predict Crop Yield"**
3. **See your prediction** with:
   - Predicted yield (tons/hectare)
   - Comparison to average
   - Growing condition insights
   - Visual badge (Low/Average/High yield)

### Tab 2: 📊 Analysis
View 5 data visualizations:
- **Feature Importance**: Which factors most influence yield
- **Average Yield by Crop**: Compare crops
- **Fertilizer & Irrigation Impact**: See how inputs affect yield
- **Yield by Soil Type**: Soil quality comparison
- **Rainfall vs Yield**: Most important factor analysis

### Tab 3: 🔄 Retrain Model
**Upload new data to improve the model:**

1. **Prepare your CSV file** with these columns:
   - Region
   - Soil_Type
   - Crop
   - Rainfall_mm
   - Temperature_Celsius
   - Fertilizer_Used (True/False)
   - Irrigation_Used (True/False)
   - Weather_Condition
   - Days_to_Harvest
   - Yield_tons_per_hectare

2. **Upload the file:**
   - Click the upload box, OR
   - Drag and drop your CSV file

3. **Wait for training** (progress bar shows)

4. **View results:**
   - New model metrics (R², RMSE, MAE)
   - Training timestamp
   - Sample counts

### Tab 4: 🌍 About Project
Learn about:
- The real-world problem it solves
- How the machine learning model works
- Feature importance breakdown
- Dataset information
- Applications and impact

## 🔧 Troubleshooting

### Issue: "Failed to connect to backend"
**Solution:**
- Make sure the server is running (command prompt should show running status)
- Check you're on http://localhost:5000 (not https)
- If using a different port, check `app.py` line near the end

### Issue: "Model not loaded" error
**Solution:**
- Ensure `crop_yield.csv` is in the same folder as `app.py`
- The first run trains the model (takes 1-2 minutes)
- Refresh the page and try again

### Issue: Charts not showing
**Solution:**
- Open browser developer tools (F12)
- Check Console for errors
- Make sure internet connection works (Chart.js loads from CDN)

### Issue: CSV upload doesn't work
**Solution:**
- Ensure CSV filename ends with `.csv`
- Verify all 10 required columns are present
- Check column names are spelled exactly correctly
- Ensure no NULL values in the data

### Issue: Port 5000 already in use
**Solution:**
- Edit `app.py`, find the last line: `app.run(...)` 
- Change `port=5000` to another number like `port=5001`
- Then use http://localhost:5001

## 📊 Sample CSV Format

Here's what your training CSV should look like:

```csv
Region,Soil_Type,Crop,Rainfall_mm,Temperature_Celsius,Fertilizer_Used,Irrigation_Used,Weather_Condition,Days_to_Harvest,Yield_tons_per_hectare
North,Loam,Wheat,600,25,True,False,Sunny,105,5.2
South,Clay,Rice,800,28,True,True,Rainy,120,6.1
East,Sandy,Maize,500,26,False,False,Cloudy,90,4.1
West,Chalky,Cotton,700,30,True,False,Sunny,110,5.8
```

## 💾 Project Files

```
archive/
├── app.py                 # BACKEND - Flask server (main)
├── agripredict.html      # FRONTEND - Website interface
├── crop_yield.csv        # DATA - Training dataset
├── crop_yield_model.py   # REFERENCE - Original training script
├── requirements.txt      # DEPENDENCIES - Python packages
├── README.md             # DOCUMENTATION - Full guide
├── run.py                # LAUNCHER - Python starter script
├── run_server.bat        # LAUNCHER - Windows batch file
├── setup_guide.md        # THIS FILE
├── model.pkl             # AUTO-CREATED - Trained model
└── uploads/              # AUTO-CREATED - Uploaded CSV files
```

## 🎯 Key Features Explained

### 1. Predictions
- Uses Random Forest machine learning model
- 100 decision trees for accurate predictions
- Considers 9 environmental and management factors
- Real-time predictions via API

### 2. Model Retraining
- Upload your own CSV data
- Automatically preprocesses categorical variables
- Trains new model in seconds
- Updates website predictions immediately
- Saves model for persistence

### 3. Model Persistence
- Trained model saved as `model.pkl`
- Persists between server restarts
- Upload datasets archived in `uploads/` folder
- Metrics history available

### 4. Responsive Design
- Works on desktop, tablet, mobile
- Beautiful, modern interface
- Smooth animations and interactions
- Accessible color schemes

## 📈 Model Performance

Current model typically achieves:
- **R² Score**: ~0.91 (explains 91% of yield variance)
- **RMSE**: ~0.41 tons/hectare average error
- **MAE**: ~0.41 tons/hectare
- **Training samples**: 999,769 records

## 🔐 Security Notes

- Server runs locally on `localhost:5000`
- Not exposed to the internet by default
- All data stays on your machine
- CORS enabled for local testing

To change this:
- Edit `app.py` to change host/port
- Remove `CORS(app)` if not needed
- Add authentication for production

## 🚀 Next Steps

1. **Run the server** using one of the methods above
2. **Test predictions** with the pre-trained model
3. **Upload your data** to retrain if desired
4. **Share the website** with others (if on same network)
5. **Deploy to cloud** for wider access (requires additional setup)

## 📚 Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Scikit-learn Docs: https://scikit-learn.org/
- Pandas Documentation: https://pandas.pydata.org/
- Chart.js: https://www.chartjs.org/

## ❓ FAQ

**Q: Can I use this on my phone?**
A: Yes! Open http://localhost:5000 on same WiFi network (change localhost to your computer's IP)

**Q: How do I stop the server?**
A: Press Ctrl+C in the command prompt

**Q: Will my data be safe?**
A: Yes, everything stays on your computer. Data is not sent anywhere.

**Q: Can I deploy this online?**
A: Yes, but requires hosting (AWS, Azure, Heroku, etc.) - see README.md

**Q: Can I customize the model?**
A: Yes, edit `app.py` and `crop_yield_model.py` to change algorithm, parameters, etc.

---

You're all set! 🎉 Run the server and start predicting crop yields!
