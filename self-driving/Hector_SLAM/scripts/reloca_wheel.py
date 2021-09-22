#! /usr/bin/env python

import rospy

from geometry_msgs.msg import Point
from sensor_msgs.msg import LaserScan

from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState

from std_srvs.srv import *

def clbk_laser(msg):
    # 720 / 5 = 144
    regions = {
        'right':  min(min(msg.ranges[0:35]), 10),
        'fright': min(min(msg.ranges[36:71]), 10),
        'front':  min(min(msg.ranges[72:107]), 10),
        'fleft':  min(min(msg.ranges[108:143]), 10),
        'left':   min(min(msg.ranges[144:179]), 10),
    }
    #rospy.loginfo(regions)
    #print 'LEft:   %s ' % (regions['left'])
    #print 'right:  %s ' % (regions['right'])

def main():
    rospy.init_node('reading_laser')
    
    sub = rospy.Subscriber('/m2wr/laser/scan', LaserScan, clbk_laser)


    model_state = ModelState()
    model_state.model_name = 'wheel'
    model_state.pose.position.x = 0
    model_state.pose.position.y = 7
    #model_state.pose.position.z = 0
  
    rospy.wait_for_service('/gazebo/set_model_state')
    
    srv_client_set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
    
    resp = srv_client_set_model_state(model_state)
    
    rospy.spin()
   
if __name__ == '__main__':
    main()
