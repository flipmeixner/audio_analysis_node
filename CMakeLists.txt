cmake_minimum_required(VERSION 3.0.2)
project(audio_analysis_node)


find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
  audio_common_msgs
)

catkin_python_setup()
# set(PYTHON_EXECUTABLE "/home/flip/python_envs/ros_env/bin/python")


add_message_files(
  FILES
  AudioFeatures.msg
  Prediction.msg
  AudioRaw.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS rospy std_msgs message_runtime audio_common_msgs
)

# Install Python scripts
catkin_install_python(PROGRAMS
  scripts/audio_processor.py
  scripts/predicter.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)


install(DIRECTORY src/audio_processing
  DESTINATION ${CATKIN_PACKAGE_PYTHON_DESTINATION}
)

install(DIRECTORY msg
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)