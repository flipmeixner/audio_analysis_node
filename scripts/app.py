import streamlit as st
import rospy
from audio_analysis_node.msg import AudioFeatures, Prediction, AudioRaw
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread
import time

# Initialize ROS node for subscribers
rospy.init_node('streamlit_audio_analysis', anonymous=True)

# Shared data storage for real-time updates
audio_data = None
feature_data = None
prediction = None

# Callback functions for ROS subscribers
def audio_callback(msg):
    global audio_data
    audio_data = np.frombuffer(msg.data, dtype=np.int16)

def feature_callback(msg):
    global feature_data
    feature_data = np.array(msg.data)

def prediction_callback(msg):
    global prediction
    prediction = msg.prediction

def feature_line_plot(st, features):
    st.subheader("Processed Audio Features")    
    fig, ax = plt.subplots()
    ax.plot(features, color='green', linewidth=1.5)
    ax.set_title("Processed Feature Pattern")
    ax.set_xlabel("Feature Index")
    ax.set_ylabel("Feature Value")
    st.pyplot(fig)

def raw_audio_waveform(st, audio_data):
    fig, ax = plt.subplots()
    ax.plot(audio_data, color='blue')
    ax.set_title("Raw Audio Signal")
    ax.set_xlabel("Samples")
    ax.set_ylabel("Amplitude")
    st.pyplot(fig)

def prediction_display(prediction):
    prediction_text = "Abnormal" if prediction == 1 else "Normal"
    prediction_display.write(f"Prediction: **{prediction_text}**")

# ROS Subscribers
rospy.Subscriber('/audio_raw', AudioRaw, audio_callback)
rospy.Subscriber('/audio_features', AudioFeatures, feature_callback)
rospy.Subscriber('/predictions', Prediction, prediction_callback)

# Streamlit app layout
st.title("Real-Time Audio Analysis with ROS")

# Placeholders for real-time visualization
raw_audio_plot = st.empty()
feature_plot = st.empty()
prediction_display = st.empty()

# Helper function to keep Streamlit in sync with ROS updates
def update_visualizations():
    while not rospy.is_shutdown():
        # Update Raw Audio Visualization
        if audio_data is not None:
            raw_audio_waveform(st, audio_data)

        # Update Feature Visualization
        if feature_data is not None:
            feature_line_plot(st, feature_data)

        # Update Prediction Display
        if prediction is not None:
            prediction_display(prediction)

        # Adjust the delay as necessary for your refresh rate
        time.sleep(1)

# Run the update function in a separate thread to keep Streamlit and ROS subscribers responsive
if __name__ == '__main__':
    Thread(target=update_visualizations, daemon=True).start()
