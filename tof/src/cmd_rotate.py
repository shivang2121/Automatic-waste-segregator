#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
import time
distance = 999
pub = None
count = 0
pos = 0
count_state = 0
smaller = 80
prev = 300

def callback(data):
    global distance, count
    

    distance = data.data
    #rospy.loginfo(distance)


def findmin():
    global pos
    num = prev
    if distance < num:
        global prev
        prev = distance
        pos = count
        num = distance
    #rospy.loginfo(pos)

    
    
    

    return num

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
    global pub,count,count_state, smaller

  
    rospy.init_node('dis_pickup', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    rospy.Subscriber("tofdis", Int16, callback)
    
    rate = rospy.Rate(20)
    min_left = 999
    min_right = 999
    direction = 0
    
    
    while not rospy.is_shutdown():
        action = Twist()
        #rospy.loginfo(distance)

        if(count_state == 0):
            min_left = findmin()
            rospy.loginfo("left "+str(min_left))
            action = turn_left()
        elif(count_state==1):
            #min_left = findmin()
            #rospy.loginfo(min_left)
            action = turn_right()
        elif(count_state==2):
            min_right = findmin()
            rospy.loginfo("right "+str(min_right))
            action = turn_right()
        elif(count_state==3):
            #min_right = findmin()
            action = turn_left()
        elif(count_state == 4):
            if(min_left<min_right):
                action = turn_left()
                rospy.loginfo("left")
                rospy.loginfo(min_left)
                
            elif(min_left>min_right):
                action = turn_right()
                rospy.loginfo("right")
                rospy.loginfo(min_right)

        else:
            action = stop()
            


        
        pub.publish(action)
        count += 1
        if count == 80 and count_state == 0:
            count_state = 1
            count = 0
        elif count == 80 and count_state ==1:
            count_state = 2
            count = 0
        elif count == 80 and count_state ==2:
            count_state =3
            count = 0
        elif count == 80 and count_state ==3:
            action = Twist()
            action = stop()
            pub.publish(action)
            time.sleep(1)
            count_state = 4
            count = 0
            rospy.loginfo(pos)
            
        elif count == pos and count_state ==4:
            action = Twist()
            action = stop()
            pub.publish(action)
            time.sleep(1)
            count_state = 5

            count = 0
            smaller = smaller / 2
            rospy.loginfo(smaller)
            if smaller == 20:
                count_state = 5
            

        rate.sleep()


    
         

    
    
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        
        pass
