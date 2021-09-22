#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16
import time

flag = 0


def callback(data):
    global flag
    distance=data.data
    pub = rospy.Publisher('rec', Int16, queue_size=10)
    if distance <= 18 and flag == 0:
        rospy.loginfo("pick")
        time.sleep(1)

	pub.publish(1)
        flag = 1
    if distance > 80 and flag ==1:
        flag = 0
        
    

    



    
    
    
   
    
def peak():

  
    rospy.init_node('dis_pickup', anonymous=True)
    

    rospy.Subscriber("tofdis", Int16, callback)

    
    
    rospy.spin()

if __name__ == '__main__':
    try:
        peak()
    except rospy.ROSInterruptException:
        cap.release()
        pass

    
