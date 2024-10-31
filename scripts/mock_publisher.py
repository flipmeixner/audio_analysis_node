#!/usr/bin/env python

import rospy
from audio_common_msgs.msg import AudioData
import numpy as np

def audio_publisher():
    rospy.init_node('audio_publisher', anonymous=True)
    audio_pub = rospy.Publisher('/audio', AudioData, queue_size=10)
    rate = rospy.Rate(10)  # Publish at 10 Hz

    while not rospy.is_shutdown():
        # Generate mock audio data (e.g., a sine wave or random noise)
        audio_chunk = (np.random.rand(1024) * 32767).astype(np.int16)  # Mock 16-bit audio chunk
        audio_msg = AudioData()
        audio_msg.data = audio_chunk.tobytes()

        # Publish the audio data
        audio_pub.publish(audio_msg)
        rospy.loginfo("Published audio data chunk")

        rate.sleep()

if __name__ == '__main__':
    try:
        audio_publisher()
    except rospy.ROSInterruptException:
        pass
