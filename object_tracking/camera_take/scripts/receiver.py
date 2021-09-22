#!/usr/bin/env python
import os
import threading
import cv2
import rospy
import numpy as np
from std_msgs.msg import Int16
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images

count = 0


def callback(data):
    br = CvBridge()
    global count
    
        
            
    print("get")
    current_frame = br.imgmsg_to_cv2(data)
    name = 'rawcamera' + str(count) +'.jpg'
    #cv2.imwrite(name,cv2.resize(image_np, (800, 600)))
    path = '/home/tan/objectTrackingpic'

    cv2.imwrite(os.path.join(path,name),current_frame)

    count += 1
    print(name)
        
def main():
   
    rospy.init_node('receiver', anonymous=True)

    rospy.Subscriber("video_frames", Image, callback)
    print("wait")

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        camera.release()
        
        pass

