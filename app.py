import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load model ---
model = joblib.load("breast_cancer_model.pkl")

# --- Page layout ---
st.set_page_config(page_title="Hospital Breast Cancer Dashboard", layout="wide")
st.title("🏥 Hospital Breast Cancer Dashboard")
st.write("Predict and visualize tumor diagnosis for single or multiple patients with confidence scores.")

# --- Input Validation ---
def validate_input(value, min_val, max_val):
    return (value >= min_val) and (value <= max_val)

# --- Sidebar: Navigation ---
menu = ["Single Patient", "Batch Patients", "Analytics"]
choice = st.sidebar.selectbox("Menu", menu)

# --- SINGLE PATIENT ---
if choice == "Single Patient":
    st.header("Single Patient Prediction")
    radius_mean = st.number_input("Radius Mean", min_value=0.0, max_value=50.0, value=14.0)
    texture_mean = st.number_input("Texture Mean", min_value=0.0, max_value=40.0, value=20.0)
    perimeter_mean = st.number_input("Perimeter Mean", min_value=0.0, max_value=200.0, value=90.0)
    area_mean = st.number_input("Area Mean", min_value=0.0, max_value=2500.0, value=650.0)
    concavity_mean = st.number_input("Concavity Mean", min_value=0.0, max_value=1.0, value=0.1)
    concave_points_mean = st.number_input("Concave Points Mean", min_value=0.0, max_value=0.5, value=0.05)
    radius_worst = st.number_input("Radius Worst", min_value=0.0, max_value=50.0, value=16.0)
    perimeter_worst = st.number_input("Perimeter Worst", min_value=0.0, max_value=200.0, value=110.0)
    area_worst = st.number_input("Area Worst", min_value=0.0, max_value=2500.0, value=800.0)
    concave_points_worst = st.number_input("Concave Points Worst", min_value=0.0, max_value=0.5, value=0.07)
    
    if st.button("Predict"):
        features = np.array([[radius_mean, texture_mean, perimeter_mean, area_mean,
                              concavity_mean, concave_points_mean,
                              radius_worst, perimeter_worst, area_worst,
                              concave_points_worst]])
        ranges = [(0,50),(0,40),(0,200),(0,2500),(0,1),(0,0.5),(0,50),(0,200),(0,2500),(0,0.5)]
        valid = all(validate_input(f,r[0],r[1]) for f,r in zip(features[0], ranges))
        if valid:
            pred = model.predict(features)[0]
            prob = model.predict_proba(features)[0][pred]*100
            if pred == 1:
                st.error(f"Prediction: Malignant ({prob:.2f}% confidence)")
            else:
                st.success(f"Prediction: Benign ({prob:.2f}% confidence)")
        else:
            st.error("Invalid input values! Check the ranges.")

# --- BATCH PATIENTS ---
elif choice == "Batch Patients":
    st.header("Batch Prediction (CSV Upload)")
    st.write("Upload a CSV with the following columns:")
    st.write("radius_mean, texture_mean, perimeter_mean, area_mean, concavity_mean, concave_points_mean, radius_worst, perimeter_worst, area_worst, concave_points_worst")
    
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        cols = ['radius_mean','texture_mean','perimeter_mean','area_mean','concavity_mean',
                'concave_points_mean','radius_worst','perimeter_worst','area_worst','concave_points_worst']
        
        if all(c in df.columns for c in cols):
            invalid_rows=[]
            for idx,row in df.iterrows():
                for c,(minv,maxv) in zip(cols, [(0,50),(0,40),(0,200),(0,2500),(0,1),(0,0.5),(0,50),(0,200),(0,2500),(0,0.5)]):
                    if not validate_input(row[c],minv,maxv):
                        invalid_rows.append(idx)
                        break
            if invalid_rows:
                st.error(f"Invalid rows: {invalid_rows}")
            else:
                preds = model.predict(df[cols])
                probs = model.predict_proba(df[cols])
                df['Prediction'] = ['Malignant' if p==1 else 'Benign' for p in preds]
                df['Confidence (%)'] = [probs[i][preds[i]]*100 for i in range(len(preds))]
                
                # Color highlight
                def highlight_row(row):
                    color = 'red' if row['Prediction']=='Malignant' else 'green'
                    return ['background-color: {}'.format(color) if col in ['Prediction','Confidence (%)'] else '' for col in row.index]
                
                st.dataframe(df.style.apply(highlight_row, axis=1))
                
                # Download CSV
                csv = df.to_csv(index=False)
                st.download_button("Download Predictions CSV", csv, "predictions.csv", "text/csv")

# --- ANALYTICS ---
elif choice == "Analytics":
    st.header("Dashboard Analytics")
    uploaded_file = st.file_uploader("Upload CSV to analyze", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'Prediction' in df.columns and 'Confidence (%)' in df.columns:
            # Count plot
            st.subheader("Malignant vs Benign Count")
            st.bar_chart(df['Prediction'].value_counts())
            
            # Confidence histogram
            st.subheader("Confidence Distribution")
            fig, ax = plt.subplots()
            sns.histplot(df['Confidence (%)'], bins=10, kde=True, color='blue', ax=ax)
            ax.set_xlabel("Confidence (%)")
            ax.set_ylabel("Number of Patients")
            st.pyplot(fig)
            
            # Scatter plot of top 2 features (radius_mean vs radius_worst)
            st.subheader("Radius Mean vs Radius Worst")
            fig2, ax2 = plt.subplots()
            colors = df['Prediction'].map({'Malignant':'red','Benign':'green'})
            ax2.scatter(df['radius_mean'], df['radius_worst'], c=colors, alpha=0.7)
            ax2.set_xlabel("Radius Mean")
            ax2.set_ylabel("Radius Worst")
            st.pyplot(fig2)
        else:
            st.error("CSV must have 'Prediction' and 'Confidence (%)' columns")
