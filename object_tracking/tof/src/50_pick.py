#!/usr/bin/env python
import rospy
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
import time
distance = 999
pub = None
minnum = 999
cmd = 0

def callback(data):
    global distance, count
    

    distance = data.data
    #rospy.loginfo(distance)

def call2back(data):
    global cmd
    cmd = data.data



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
    rospy.Subscriber("pick_50", Int16, call2back)
    pub_1 = rospy.Publisher('rec', Int16, queue_size=10)
    
    rate = rospy.Rate(20)

    direction = 0
    cali = 1
    flag = 0
    count = 0
    done_cali = 0
    sec = 0
    final_check = 0
    stage = 0.3
    
 
    print("wait")
    
    while not rospy.is_shutdown():
        

        if cmd == 1:
            print("work")
            action = Twist()
            
            #rospy.loginfo(distance)
            #print(cali)
            if(cali == 1 and count < 8 and sec <4):
                print("cali")
                if(flag ==1 and minnum < distance ):
                    action = turn_left()
                    direction = 1
                elif(flag == 1 and minnum < distance):
                    action = turn_right()
                    direction = -1
                elif(flag == 1 and minnum == distance):
                    action = stop()
                else:
                    minnum = distance
                    action = turn_right()
                    # if direction == 0 or direction == 1:
                    #     print("right")
                    #     action = turn_right()
                    #     direction = -1
                    # elif direction == -1:
                    #     print("left")
                    #     action = turn_left()
                    #     direction = 1

                    flag = 1
                count += 1 


            elif((cali == 1 or cali == 2) and count == 8):
                action = stop()
                time.sleep(stage)
                print("here")
                if minnum > distance + 2 or minnum < distance - 2 :
                    count = 0
                    sec += 1 
                    flag = 0
                    rospy.loginfo(minnum)
                    rospy.loginfo("round two")
                else:
                    count = 0
                    flag = 0
                    sec = 0
                    done_cali = 1
                    cali = 0
                    aim = distance
                    cur = distance - 5
                    print("aim = " + str(aim))
                    print(cur)
                    print("done")

            
            elif(cali == 0 and done_cali == 1):
                print("here2")

                if(distance > cur and distance > 19):
                    if(distance < 30):
                        stage = 0.1
                    else:
                        stage = 0.1
                    
                    if(distance < aim +3 ):
                        action = move_forward()
                    else:
                        action = stop()
                        print("bias cali")
                        cali = 1
                        done_cali = 0
                elif(distance <= cur and distance > 19):
                    action = stop()
                    print("45 cali")
                    cali = 1
                    done_cali = 0
                    print(stage)
                
                elif(distance <= 19 ):
                    print("here3")
                    if(final_check < 8):
                        print("final_check")
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
                        final_check += 1 
                    else:
                        action = stop()
                        pub.publish(action)
                        print("pick")
                        time.sleep(0.8)
                        pub_1.publish(1)
                        print("FINISH")
                        break
            
            else:
                print("here4")
                action = stop()




            
            pub.publish(action)
            time.sleep(stage)



        rate.sleep()
    
    action = stop()
    pub.publish(action)


    
         

    
    
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        
        pass
