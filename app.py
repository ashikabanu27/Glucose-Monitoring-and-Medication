import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Function to analyze blood glucose levels
def analyze_glucose_levels(data):
    # Ensure the dataset contains 'Glucose_level'
    if 'Glucose_level' not in data.columns:
        st.error("Error: The uploaded file must contain a 'Glucose_level' column.")
        return None

    glucose_levels = data['Glucose_level'].dropna()

    if glucose_levels.empty:
        st.warning("No glucose data found in the uploaded file.")
        return None

    # Define risk categories
    risk_levels = []
    for value in glucose_levels:
        if value < 100:
            risk_levels.append("Normal")
        elif 100 <= value < 125:
            risk_levels.append("Prediabetes")
        else:
            risk_levels.append("Diabetes")

    # Add classification to the DataFrame
    data['Risk Level'] = risk_levels

    # Display data preview
    st.subheader("📊 Data Preview with Risk Levels")
    st.write(data[['Glucose_level', 'Risk Level']].head())

    # Plot distribution
    st.subheader("📈 Glucose Level Distribution")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(glucose_levels, bins=20, kde=True, ax=ax)
    ax.axvline(100, color='yellow', linestyle='dashed', label="Prediabetes (100 mg/dL)")
    ax.axvline(125, color='red', linestyle='dashed', label="Diabetes (125 mg/dL)")
    ax.set_xlabel("Blood Glucose Level (mg/dL)")
    ax.set_ylabel("Count")
    ax.legend()
    st.pyplot(fig)

    # Medication suggestions
    st.subheader("💊 Medication Suggestions")
    suggestions = []
    for risk, level in zip(data['Risk Level'], glucose_levels):
        if risk == "Normal":
            suggestions.append(f" Glucose Level: {level} mg/dL - No medication needed. Maintain a balanced diet.")
        elif risk == "Prediabetes":
            suggestions.append(f" Glucose Level: {level} mg/dL - Consider lifestyle changes, exercise, and diet control.")
        else:
            suggestions.append(f" Glucose Level: {level} mg/dL - Consult a doctor. Medications like Metformin may be recommended.")
    
    for suggestion in suggestions[:5]:  # Display first 5 suggestions
        st.write(suggestion)

# Streamlit UI
st.title("🔬 Blood Glucose Level Prediction & Medication Suggestion")
st.write("Upload your CSV file containing **PPG Signal & Glucose Levels** to analyze risk levels and get medication recommendations.")

# File uploader
uploaded_file = st.file_uploader(" Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the uploaded file
    df = pd.read_csv(uploaded_file)
    
    # Display first few rows
    st.subheader("📜 Uploaded Data Preview")
    st.write(df.head())

    # Analyze glucose data
    analyze_glucose_levels(df)
