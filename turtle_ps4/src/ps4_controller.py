#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen, SetPenRequest
from std_srvs.srv import Empty, EmptyRequest
from m2_ps4.msg import  Ps4Data


# hint: some imports are missing

old_data = Ps4Data()
k = 1
def callback(data):
    global old_data
    global k
    Ps4 = Twist()
    Pen = SetPenRequest()
    E = EmptyRequest()
    # you should publish the velocity here!
    
    # hint: to detect a button being pressed, you can use the following pseudocode:
    # 
    # if ((data.button is pressed) and (old_data.button not pressed)),
    # then do something...
    if(data.dpad_y > 0 and data.dpad_y != old_data.dpad_y and k < 5):
        k+=1
    if(data.dpad_y < 0 and data.dpad_y != old_data.dpad_y and k > 1):
        k-=1
    if(data.hat_ly != old_data.hat_ly):
        Ps4.linear.x = data.hat_ly  * k
    elif(data.hat_ly == -1 or data.hat_ly == 1):
    	Ps4.linear.x = data.hat_ly  * k

    if(data.hat_rx != old_data.hat_rx):
        Ps4.angular.z = data.hat_rx * 10
    elif(data.hat_rx == -1 or data.hat_rx == 1):
    	Ps4.angular.z = data.hat_rx * 10
    	
    pub.publish(Ps4)
    
    if(data.ps and data.ps != old_data.ps):
    	srv_col2(E)
    
    if(data.triangle and data.triangle != old_data.triangle):
    	Pen.r = 0
    	Pen.g = 255
    	Pen.b = 0
    	srv_col(Pen)
    elif(data.circle and data.circle != old_data.circle):
    	Pen.r = 255
    	Pen.g = 0
    	Pen.b = 0
    	srv_col(Pen)
    elif(data.cross and data.cross != old_data.cross):
    	Pen.r = 0
    	Pen.g = 0
    	Pen.b = 255
    	srv_col(Pen)
    elif(data.square and data.square != old_data.circle):
    	Pen.r = 255
    	Pen.g = 0
    	Pen.b = 255
    	srv_col(Pen)
	
    old_data = data

if __name__ == '__main__':
    rospy.init_node('ps4_controller')
    
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 1)
    # publisher object goes here... hint: the topic type is Twist
    sub = rospy.Subscriber('/input/ps4_data', Ps4Data, callback)
    # subscriber object goes here
    
    # one service object is needed for each service called!
    
    srv_col = rospy.ServiceProxy('/turtle1/set_pen', SetPen)
    # service client object goes here... hint: the srv type is SetPen
    srv_col2 = rospy.ServiceProxy('/clear',Empty)
    # fill in the other service client object...
    
    rospy.spin()
