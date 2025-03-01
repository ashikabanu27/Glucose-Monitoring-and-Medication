import streamlit as st
import pandas as pd
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# Function to load PPG Data
def load_ppg_data(uploaded_file):
    data = pd.read_csv(uploaded_file)
    ppg_signal = data.iloc[:, 1].values  # Assuming PPG values are in the second column
    return ppg_signal

# Function to detect peaks (heartbeats) in PPG signal
def detect_heart_rate(ppg_signal, fs=125):
    peaks, _ = signal.find_peaks(ppg_signal, distance=fs//2)
    heart_rate = len(peaks) * 60 / (len(ppg_signal) / fs)
    return heart_rate, peaks

# Function to suggest medication based on heart rate
def suggest_medication(heart_rate):
    if heart_rate < 60:
        return "Bradycardia detected. Suggested: Consult a doctor for evaluation."
    elif 60 <= heart_rate <= 100:
        return "Normal heart rate. No medication required."
    else:
        return "Tachycardia detected. Suggested: Beta-blockers or consult a cardiologist."

# Streamlit UI
st.title("Heart Rate Monitoring from PPG Data")

uploaded_file = st.file_uploader("Upload a PPG CSV File", type=["csv"])

if uploaded_file is not None:
    st.write("File uploaded successfully!")

    # Load PPG Data
    ppg_signal = load_ppg_data(uploaded_file)

    # Detect Heart Rate
    heart_rate, peaks = detect_heart_rate(ppg_signal)

    # Display Results
    st.subheader("Heart Rate Analysis")
    st.write(f"**Detected Heart Rate:** {heart_rate:.2f} BPM")
    st.write(f"**Medication Suggestion:** {suggest_medication(heart_rate)}")

    # Plot PPG Signal with Detected Peaks
    st.subheader("PPG Signal with Detected Peaks")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(ppg_signal, label="PPG Signal", alpha=0.7)
    ax.scatter(peaks, ppg_signal[peaks], color='red', marker="x", label="Heartbeats")
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("PPG Signal Amplitude")
    ax.legend()
    st.pyplot(fig)
