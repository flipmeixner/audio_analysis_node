#!/home/flip/python_envs/rover_env/bin/python
import rospy
from audio_common_msgs.msg import AudioData
import numpy as np
from collections import deque
import threading
import time

from audio_processing.utils import feature_extraction
from std_msgs.msg import Float32MultiArray
from audio_analysis_node.msg import AudioFeatures, AudioRaw

class AudioProcessor:
    def __init__(self, window_duration=10.0, overlap=0.5):
        """
        Initialize the audio processor.

        Parameters:
        - window_duration: Duration of each window in seconds.
        - overlap: Fraction of overlap between windows (0 to <1).
        """
        self.window_duration = window_duration
        self.overlap = overlap
        self.buffer = deque()
        self.lock = threading.Lock()
        self.sr = None  # Sample rate (to be set when data is received)
        self.chunk_size = None  # Number of samples per message
        self.window_size = None  # Number of samples per window
        self.step_size = None  # Number of samples to step each time
        self.initialized = False

        rospy.init_node('audio_processor')
        rospy.Subscriber('/audio', AudioData, self.audio_callback)
        
        self.feature_pub = rospy.Publisher('/audio_features', AudioFeatures, queue_size=10)
        self.raw_pub = rospy.Publisher('/audio_raw', AudioRaw, queue_size=10)

    def audio_callback(self, msg):
        with self.lock:
            # Convert byte data to numpy array
            audio_chunk = np.frombuffer(msg.data, dtype=np.int16)

            if not self.initialized:
                # Initialize parameters
                self.sr = 44100  # Replace with actual sample rate
                self.chunk_size = len(audio_chunk)
                self.window_size = int(self.sr * self.window_duration)
                self.step_size = int(self.window_size * (1 - self.overlap))
                self.initialized = True
            # Create msg
            raw_msg = AudioRaw()
            raw_msg.data = audio_chunk.tolist() # Convert numpy array to list
            self.raw_pub.publish(raw_msg)
            rospy.loginfo("Published a chunk of audio")
            self.buffer.extend(audio_chunk)
            self.process_buffer()

    def process_buffer(self):
        rospy.loginfo(f"Checking buffer for window processing --> buffer length is {len(self.buffer)}")
        while len(self.buffer) >= self.window_size:
            rospy.loginfo("Buffer full, processing window")
            # Extract window
            window = [self.buffer.popleft() for _ in range(self.window_size)]
            # Process window in a separate thread to avoid blocking
            threading.Thread(target=self.process_window, args=(np.array(window),)).start()
            # Remove overlapping samples
            for _ in range(int(self.step_size)):
                if self.buffer:
                    self.buffer.popleft()
                else:
                    break

    def process_window(self, audio_data):
        # Feature extraction
        start_time = time.time()
        features = feature_extraction(audio_data)
        rospy.loginfo(f"Feature extraction took {time.time() - start_time:.2f} seconds")
        # Create a ROS publisher
        features_msg = AudioFeatures()
        features_msg.features = Float32MultiArray()
        features_msg.features.data = features.tolist()

        self.feature_pub.publish(features_msg)

        rospy.loginfo("Processed a window of audio data.")

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    processor = AudioProcessor(window_duration=10.0, overlap=0.5)
    processor.run()