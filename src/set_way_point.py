#!/usr/bin/env python
import rospy
import math
from std_msgs.msg import String
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from math import atan2, atan
from turtle_regulation_KhertishLobine_NoreenSooltangos.srv import waypoint

global coords
coords = [7,7]

def Subscriber_pose():
	global turtlePose
	turtlePose = None
	rospy.init_node('set_way_point')
	rospy.Service('set_waypoint_srv', waypoint, set_waypoint_service)
	rospy.Subscriber('pose', Pose, getPosition)
	pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
	rate = rospy.Rate(10)

	kp = rospy.get_param("~kp", 5.0)
	kpl = rospy.get_param("~kpl", 1.0)

	while not rospy.is_shutdown():

		if turtlePose is not None:
			rotate(kp, pub, rate)
			is_moving(pub, rate, kpl)

			#print(message)

def getPosition(pose):
	global turtlePose
 	turtlePose = pose



def rotate(kp, pub,rate):
	message = Twist()
	theta = angle()
	print(theta)

	error_angle = error(theta)
	#print("Error Angle = ", error_angle)
	u = kp * error_angle
	message.angular.z = u

	pub.publish(message)
	rate.sleep()


def is_moving(pub ,rate ,kpl):
	message = Twist()

	y_length = (coords[1] - turtlePose.y)* (coords[1] - turtlePose.y)
	x_length = (coords[0] - turtlePose.x)* (coords[0] - turtlePose.x)


	distance_travelled = math.sqrt(y_length + x_length)

	v = kpl * distance_travelled
	message.linear.x = v
	print("Commande Lineaire = ", v)

	pub.publish(message)
	rate.sleep()



def angle():
	return atan2(coords[1] - turtlePose.y ,coords[0] - turtlePose.x)

def error(theta):

	return atan(math.tan((theta - turtlePose.theta)/2))

def set_waypoint_service(input):
	global coords
	coords = [input.x.data, input.y.data] 
	return Bool(True)


if __name__=="__main__":
	try :
		Subscriber_pose()

	except rospy.ROSInterruptException:
		pass
