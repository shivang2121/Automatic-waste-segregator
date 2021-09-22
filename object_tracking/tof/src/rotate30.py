#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
import time
cmd = 0
count = 0
countright = 0
turn = 0
def callback(data):
    global cmd,count
    print("get")
    

    cmd = data.data
    count = 0

def turn_left():
    action = Twist()
    action.angular.z = 0.2
    return action
    
    
def turn_right():
    action = Twist()
    action.angular.z = -0.2
    return action

def stop():
    action = Twist()
    action.angular.z = 0
    action.linear.x = 0
    return action


       
        
    
    
def main():
    global pub,count,count_state,cmd,countright,turn

  
    rospy.init_node('search', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.Subscriber("search", Int16, callback)
    pub_1 = rospy.Publisher('pick_50', Int16, queue_size=10)
    pub_2 = rospy.Publisher('camera_Signal', Int16, queue_size=10)
    rate = rospy.Rate(20)
    print("wait- rotate 90 = search left = 1 right = 2")
    
    time.sleep(0.8)
    pub_2.publish(1)

    print("initial screen")

    
    while not rospy.is_shutdown():
        action = Twist()

        if(cmd == 1 and countright < 170):
            
            action = turn_left()
            countright += 1
            pub.publish(action)
        elif(cmd == 2 and count < 56):
            action = turn_right()
            count += 1
            pub.publish(action)
        
        elif(count == 56 and turn <3):
            action = stop()
            pub.publish(action)
            time.sleep(0.8)
            pub_2.publish(2)
            turn +=1
            print("second screen")
            
            countright +=1
            count +=1
        elif turn == 3:
            pub_2.publish(3)
            turn +=3

        elif(cmd == 3 ):
            action = stop()
            pub.publish(action)
            cmd = 0
            time.sleep(0.8)
            pub_1.publish(1)

            
            


        
        
        
        # if count == 80 and count_state == 0:
        #     count_state = 5
        #     count = 0
        # elif count == 80 and count_state ==1:
        #     count_state = 5
        #     count = 0
            

            

        rate.sleep()


    
         

    
    
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        
        pass
