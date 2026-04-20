# 🚀 Quick Start - AgriPredict

## In 3 Steps:

### 1️⃣ Create the Virtual Environment
```bash
python -m venv .venv
```

### 2️⃣ Activate and Install Dependencies
**Windows:**
```cmd
.\.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

**Mac/Linux:**
```bash
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

### 3️⃣ Run the Server
**Windows:**
- Double-click `run_server.bat`, OR
- In Command Prompt: `python app.py`

**Mac/Linux:**
```bash
python app.py
```

### 3️⃣ Open Website
Go to: **http://localhost:5000**

---

## Architecture

```
┌─────────────────────────────────────┐
│  Browser (Frontend)                 │
│  - agripredict.html                 │
│  - Beautiful UI                     │
│  - Charts & predictions             │
└────────────┬────────────────────────┘
             │ HTTP Requests
             │ (JSON)
             ▼
┌─────────────────────────────────────┐
│  Flask Server (Backend)             │
│  - app.py                           │
│  - API endpoints                    │
│  - Model predictions                │
│  - Retraining logic                 │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Machine Learning                   │
│  - model.pkl (trained model)        │
│  - Random Forest (100 trees)        │
│  - Scikit-learn                     │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Data & Training                    │
│  - crop_yield.csv                   │
│  - Pandas preprocessing             │
│  - Train/test split                 │
└─────────────────────────────────────┘
```

---

## 📁 Files Explained

| File | Purpose |
|------|---------|
| `app.py` | 🔴 **MAIN** - Flask backend server |
| `agripredict.html` | 🔵 Frontend website interface |
| `crop_yield.csv` | 📊 Training dataset (1M records) |
| `requirements.txt` | 📦 Python package dependencies |
| `model.pkl` | 🧠 Trained ML model (auto-created) |
| `run_server.bat` | ⚙️ Start script for Windows |
| `run.py` | ⚙️ Start script for Python |
| `README.md` | 📚 Full documentation |
| `SETUP_GUIDE.md` | 🎓 Detailed setup guide |

---

## 🔌 API Endpoints

All endpoints are called automatically by the website.

### Predict Yield
```
POST http://localhost:5000/predict
Input: crop, region, soil, rainfall, temp, etc.
Output: prediction, insights
```

### Retrain Model
```
POST http://localhost:5000/retrain
Input: CSV file upload
Output: success, new metrics
```

### Get Metrics
```
GET http://localhost:5000/metrics
Output: R², RMSE, MAE, training timestamp
```

---

## ✨ Features

✅ **Predict** crop yield from farm conditions  
✅ **Retrain** model with your own data  
✅ **Visualize** feature importance & data  
✅ **Mobile-friendly** responsive design  
✅ **Drag-and-drop** file upload  
✅ **Real-time** predictions  
✅ **Beautiful UI** with modern styling  
✅ **No cloud needed** - runs locally  

---

## 🎯 What You Can Do

### As a Farmer 👨‍🌾
- Predict yield before planting
- Optimize fertilizer & irrigation
- Understand what affects your crops

### As a Researcher 👨‍🔬
- Analyze 1,000,000 crop records
- Retrain with your own data
- Understand feature importance

### As a Developer 👨‍💻
- Use as template for ML web apps
- Customize model parameters
- Deploy to production

---

## 🛠️ Customization

### Change prediction model:
Edit `app.py`, line ~70:
```python
model = RandomForestRegressor(
    n_estimators=200,      # More trees
    max_depth=20,          # Deeper trees
    random_state=42
)
```

### Change server port:
Edit `app.py`, last line:
```python
app.run(debug=True, host='localhost', port=8080)  # Change 5000 to 8080
```

### Add more input features:
Edit `app.py` and `agripredict.html` to add new columns

---

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| "Connection refused" | Start server with `python app.py` |
| "CSV upload fails" | Check column names match exactly |
| "No predictions" | Refresh page, wait for model to train |
| "Port already in use" | Change port in `app.py` last line |

---

## 📊 Model Details

- **Algorithm**: Random Forest Regressor
- **Trees**: 100
- **Features**: 9 inputs
- **Target**: Yield (tons/hectare)
- **Performance**: R² ≈ 0.91
- **Accuracy**: ±0.41 tons/hectare

---

## 🚀 Next Steps

1. ✅ Run the server
2. ✅ Test predictions
3. ✅ Explore visualizations
4. ✅ Try model retraining
5. ✅ Share with team
6. ✅ Deploy to cloud (optional)

---

## 📞 Support

- Check `SETUP_GUIDE.md` for detailed instructions
- Check `README.md` for API documentation
- All code is well-commented for customization

**Happy predicting!** 🌾🚀
