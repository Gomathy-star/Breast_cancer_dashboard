# 🏥 Hospital Breast Cancer Dashboard

A **Streamlit-based web dashboard** to predict whether a breast tumor is **Malignant** or **Benign** using a trained Random Forest model. Designed for hospital staff to quickly assess patient data individually or in batches.

---

## **Features**

1. **Single Patient Prediction**  
   - Enter tumor features manually via the web interface.  
   - Instant prediction with confidence score.

2. **Batch Prediction (CSV Upload)**  
   - Upload CSV files containing multiple patient data.  
   - Get predictions for all patients with a downloadable results table.

3. **Analytics & Visualization**  
   - Bar charts for **Malignant vs. Benign** counts.  
   - Scatter plots and histograms for feature analysis.  
   - Easy interpretation for hospital staff.

---

## **Top Features Used**

The model uses the **top 10 features** from the Breast Cancer dataset:

- radius_mean  
- texture_mean  
- perimeter_mean  
- area_mean  
- concavity_mean  
- concave_points_mean  
- radius_worst  
- perimeter_worst  
- area_worst  
- concave_points_worst  

---

## **Installation**

1. Clone the repository:

```bash
git clone https://github.com/Gomathy-star/breast_cancer_dashboard.git
cd breast_cancer_dashboard

    Create a virtual environment (optional but recommended):

python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

    Install dependencies:

pip install -r requirements.txt

Run the Dashboard

streamlit run app.py

    Open your browser at the URL shown (usually http://localhost:8501).

    Use the single patient input, batch CSV upload, or analytics menu.

Sample CSV Files

    sample_patients.csv → 4 sample patients for testing single/batch predictions.

    sample_patients_large.csv → 20 patients for batch testing.

CSV format example:

radius_mean,texture_mean,perimeter_mean,area_mean,concavity_mean,concave_points_mean,radius_worst,perimeter_worst,area_worst,concave_points_worst
12.0,15.0,75.0,450.0,0.05,0.02,13.0,90.0,600.0,0.03
20.0,30.0,130.0,1400.0,0.3,0.12,23.0,160.0,1800.0,0.15

Validation

    Input validation ensures realistic feature ranges.

    Invalid values are flagged in the dashboard.

    Missing or incorrect CSV columns will show errors.

Project Structure

breast_cancer_dashboard/
│
├─ app.py                  # Streamlit dashboard
├─ breast_cancer_model.pkl # Trained ML model
├─ requirements.txt        # Python dependencies
├─ sample_patients.csv     # Test CSV (4 patients)
├─ sample_patients_large.csv # Test CSV (20 patients)
├─ README.md               # Project documentation
└─ .gitignore              # Ignored files

Contributing

    Fork the repository.

    Create a new branch: git checkout -b feature/new-feature.

    Make your changes.

    Commit: git commit -m "Add new feature".

    Push and open a Pull Request.

License

MIT License © 2025
