#!/usr/bin/env python
import os
import threading
import cv2
import rospy
import numpy as np
from std_msgs.msg import Int16
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images

#count = 0

class CameraBufferCleanerThread(threading.Thread):
    def __init__(self, camera, name='camera-buffer-cleaner-thread'):
        self.camera = camera
        self.last_frame = None
        super(CameraBufferCleanerThread, self).__init__(name=name)
        self.start()

    def run(self):
        while not rospy.is_shutdown():
            ret, self.last_frame = self.camera.read()



camera = cv2.VideoCapture(0)
camera.set(3,1280)
camera.set(4,960)
cam_cleaner = CameraBufferCleanerThread(camera)
def callback(data):
    signal=data.data
    #global count
    print("signal")
    if signal == 1 or signal == 2 or signal == 3:
        
            
        print("take")
        if cam_cleaner.last_frame is not None:
            image_np = cam_cleaner.last_frame
        else:
            ret, image_np = camera.read()
        #name = 'rawcamera' + str(count) +'.jpg'
        #cv2.imwrite(name,cv2.resize(image_np, (800, 600)))
        #path = '/home/tan/objectTrackingpic/test'

        br = CvBridge()
        pub = rospy.Publisher('video_frames', Image, queue_size=10)
        rospy.loginfo('publishing video frame')
        pub.publish(br.cv2_to_imgmsg(image_np))
        #cv2.imwrite(os.path.join(path,name),image_np)
    
        #count += 1
        #print(name)
        
def main():
   
    rospy.init_node('sender', anonymous=True)

    rospy.Subscriber("camera_Signal", Int16, callback)
    print("wait")

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        camera.release()
        
        pass

