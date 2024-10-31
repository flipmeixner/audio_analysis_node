import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import rospy

from audio_processing.msg import AudioFeatures, Prediction, AudioRaw


class AudioStreamlit:
    def __init__(self):
        rospy.init_node('streamlit_ node')

        self.raw_sub = rospy.Subscriber('/audio_raw', AudioRaw, self.callback_raw)
        self.feature_sub = rospy.Subscriber('/audio_features', AudioFeatures, self.callback_feature)
        self.prediction_sub = rospy.Subscriber('/predictions', self.callback_pred)

    def callback_raw(self, raw):

# Assume 'raw_audio_data' is a 1D NumPy array representing the raw audio data
raw_audio_data = np.random.rand(1000)  # Replace with actual data

# Assume 'preprocessed_data' is a 2D NumPy array representing the preprocessed audio data (e.g., spectrogram)
preprocessed_data = np.random.rand(10, 100)

# Assume 'prediction_output' is a 1D NumPy array representing the output of your model
prediction_output = np.random.rand(10)  # Replace with actual data

st.title("Audio Analysis App")

# Module 1: Raw Audio Visualization
col1, col2, _ = st.columns([3, 1, 1])
with col1:
    st.markdown("**Raw Audio Waveform**")
    plt.plot(raw_audio_data)
    st.pyplot(plt.gcf())

# Module 2: Preprocessed Data Visualization
with col2:
    st.markdown("**Preprocessed Data (Spectrogram)**")
    plt.imshow(preprocessed_data, cmap='hot', interpolation='nearest')
    st.pyplot(plt.gcf())

# Module 3: Prediction Output Visualization
with col3:
    st.markdown("**Prediction Output**")
    plt.bar(range(len(prediction_output)), prediction_output)
    st.pyplot(plt.gcf())


def spin(self):
    rospy.spin()