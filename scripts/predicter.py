#!/home/flip/python_envs/ros_env/bin/python

import rospy
from audio_analysis_node.msg import AudioFeatures, Prediction
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os


class PredictNode:
	def __init__(self, nca_model_path, knn_model_path):
		#Initialize the node
		rospy.init_node('inference_node')
		rospy.loginfo("Initializing node")
		#Load the models
		if not os.path.isfile(nca_model_path):
		    rospy.logerr(f"NCA model file not found at {nca_model_path}")
		if not os.path.isfile(knn_model_path):
		    rospy.logerr(f"KNN model file not found at {knn_model_path}")
		self.nca_model = self.load_model(nca_model_path)
		self.knn_model = self.load_model(knn_model_path)

		self.scaler = StandardScaler()
		self.feature_buffer = []
		self.scaler_fitted = False
		

		#Subscribe to the audio features topic
		rospy.Subscriber('/audio_features', AudioFeatures, self.callback)

		self.prediction = None

		#Publish the prediction
		self.prediction_pub = rospy.Publisher('/predictions', Prediction, queue_size=10)

	def load_model(self, model_path):
		"""
		Load the trained model from a file.
		"""
		rospy.loginfo(f"Loading model from {model_path}")
		with open(model_path, 'rb') as f:
			model = joblib.load(f)
		rospy.loginfo("Model loaded successfully")
		return model

	def callback(self, msg):
		x = np.array(msg.features.data)
		x = x.reshape(1, -1)
		if not self.scaler_fitted:
			self.scaler.fit(x)
			self.scaler_fitted = True
			rospy.loginfo("StandardScaler fitted with initial data")				
		else:
			x_scaled = self.scaler.transform(x)
			x_nca = self.nca_model.transform(x_scaled)
			self.prediction = self.knn_model.predict([x_nca])
			rospy.loginfo(f"Predicted Class: {self.prediction[0]}")
			self.publish_prediction(self.prediction)

	def publish_prediction(self, prediction):
		pred_msg = Prediction()
		pred_msg.prediction = prediction[0]
		self.prediction_pub.publish(pred_msg)
		rospy.loginfo("Published preodiction")

	def spin(self):
		rospy.spin()


if __name__ == '__main__':
	try:
		nca_model_path = '/home/flip/aan_files/nca_model.pkl'
		knn_model_path = '/home/flip/aan_files/knn_model.pkl'
		pred_node = PredictNode(nca_model_path, knn_model_path)
		pred_node.spin()
	except rospy.ROSInterruptException:
		pass