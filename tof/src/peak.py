#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16
import cv2



def callback(data):
    distance=data.data
    print("check")
    if distance != 0:
        rospy.loginfo("peak!")
        cap = cv2.VideoCapture(0)
        while(True):
            ret, frame =cap.read()
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF ==ord('q'):
                    break
        cap.release()
        cv2.destroyAllWindows()



    
    #cv2.imwrite("pic.jpg",frame)
    

    



    
    
    
   
    
def peak():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('peak', anonymous=True)

    rospy.Subscriber("chatter", Int16, callback)
    
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        peak()
    except rospy.ROSInterruptException:
        pass

    