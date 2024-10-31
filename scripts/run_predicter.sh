#!/bin/bash
# Activate the virtual environment
source /home/philip/rover_ws/ros_audio_env/bin/activate
# Run the ROS node using the Python interpreter from the virtual environment
exec /home/philip/rover_ws/ros_audio_env/bin/python /home/philip/rover_ws/src/audio_processing/scripts/predicter.py
