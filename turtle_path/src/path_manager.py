#!/usr/bin/env python
import rospy
from math import pi, fmod, sin, cos, sqrt
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtle_path.srv import *
# hint: some imports are missing

cur_pos = Pose()

def cb_pose(data): # get the current position from subscribing the turtle position
    global cur_pos
    cur_pos = data

def cb_walk(req):
    if (req.distance < 0):
        return False

    # hint: calculate the projected (x, y) after walking the distance,
    # and return false if it is outside the boundary
    
    px = cur_pos.x + req.distance * cos(cur_pos.theta)
    py = cur_pos.y + req.distance * sin(cur_pos.theta)
    
    if(px > 11 or px < 0 or py > 11 or py < 0)
    	return false
 
    rate = rospy.Rate(100) # 100Hz control loop
    
    d = sqrt((px - cur_pos.x)**2 + (py - cur_pos.y)**2)
    while (d != 0): # control loop
        
        # in each iteration of the control loop, publish a velocity

        # hint: you need to use the formula for distance between two points
        vel = Twist()
        vel.linear.x = d
        pub.publish(vel)
        
        d = sqrt((px - cur_pos.x)**2 + (py - cur_pos.y)**2)
        rate.sleep()
    
    vel = Twist() # publish a velocity 0 at the end, to ensure the turtle really stops
    vel.linear.x = 0
    pub.publish(vel)

    return True

def cb_orientation(req):

    rate = rospy.Rate(100) # 100Hz control loop
    
    a_d = fmod(req.orientation - cur_pos.theta + pi + 2 * pi, 2 * pi) - pi
      
    while (a_d != 0): # control loop
        
        # in each iteration of the control loop, publish a velocity

        # hint: signed smallest distance between two angles: 
        # see https://stackoverflow.com/questions/1878907/the-smallest-difference-between-2-angles
        #     dist = fmod(req.orientation - cur_pos.theta + pi + 2 * pi, 2 * pi) - pi
        vel = Twist()
        vel.angular.z = a_d
        pub.publish(vel)
        
        a_d = fmod(req.orientation - cur_pos.theta + pi + 2 * pi, 2 * pi) - pi
        rate.sleep()
    
    vel = Twist() # publish a velocity 0 at the end, to ensure the turtle really stops
    vel.angular.z = 0
    pub.publish(vel)

    return True

if __name__ == '__main__':
    rospy.init_node('path_manager')
    
    pub = rospy.Publisher('turtle1/cmd_vel',Twist, queue_size = 1)
    sub = rospy.Subsriber('turtle1/pose',Pose,cb_pose)
    
    ## init each service server here:
    # rospy.Service( ... )		# callback to cb_orientation
    rospy.Service('set_orientation',SetOrientation,cb_orientation)
    # rospy.Service( ... )		# callback to cb_walk
    rospy.Service('walk_distance',WalkDistance,cb_walk)
    
    rospy.spin()
