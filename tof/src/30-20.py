#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
import time
distance = 999
pub = None
minnum = 999


def callback(data):
    global distance, count
    

    distance = data.data
    #rospy.loginfo(distance)


def findmin():
    
    num = prev

    if distance < num:
        global prev
        prev = distance
        num = distance
    return num

def move_forward():
    action = Twist()
    action.linear.x = 0.2
    return action

def move_back():
    action = Twist()
    action.linear.x = -0.2
    return action

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
    global pub, minnum
  
    rospy.init_node('dis_pickup', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.Subscriber("tofdis", Int16, callback)
    
    rate = rospy.Rate(20)

    cali = 0
    flag = 0
    count = 0
    done_cali = 0
    stage = 0.8
 
    
    
    while not rospy.is_shutdown():
        action = Twist()
        
        #rospy.loginfo(distance)
        #print(cali)
        if(cali == 1 and count < 8):
            print("cali")
            if(flag ==1 and minnum < distance):
                action = turn_left()
            elif(flag == 1 and minnum < distance):
                action = turn_right()
            elif(flag == 1 and minnum == distance):
                action = stop()
            else:
                minnum = distance
                action = turn_right()
                flag = 1
            
            
            count += 1 
        elif(cali == 1 and count == 8):
            action = stop()
            if minnum != distance:
                #count = 0
                rospy.loginfo(minnum)
                rospy.loginfo("round two")
        
        elif(cali == 0 and done_cali == 0):
            if(distance > 35):
                action = move_forward()
            elif(distance <= 35):
                action = stop()
                cali = 1
                stage = 0.3
        



        else:
            action = stop()
            if minnum != distance:
                #count = 0
                rospy.loginfo(minnum)
                rospy.loginfo("round two")
            
            
            # elif(distance == 23):
            #     action = stop()
            # elif distance < 20 and distance > 16:
            #     action = stop()
            # elif(distance < 16):
            #     action = move_back()


        
        pub.publish(action)
        time.sleep(stage)



        rate.sleep()


    
         

    
    
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        
        pass
