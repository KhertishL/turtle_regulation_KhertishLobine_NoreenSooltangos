#!/usr/bin/env python
import rospy
import math
from std_msgs.msg import String
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from math import atan2, atan, sqrt

global coords
coords = [7,7]

def Subscriber_pose():
	global turtlePose
	turtlePose = None
	rospy.init_node('set_way_point')
	rospy.Subscriber('pose', Pose, getPosition)
	pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
	rate = rospy.Rate(10)

	kp = rospy.get_param("~kp", 1.0)

	while not rospy.is_shutdown():
		message = Twist()



		if turtlePose is not None:
			theta = angle()
			print(theta)

			error_angle = error(theta)
			#print("Error Angle = ", error_angle)
			u = kp * error_angle
			message.angular.z = u
			print(message)


		pub.publish(message)
		rate.sleep()

def getPosition(pose):
	global turtlePose
 	turtlePose = pose

def angle():
	return atan2(coords[1] - turtlePose.y ,coords[0] - turtlePose.x)

def angular_vel(kp, error_angle):
	return kp * error_angle


def error(theta):

	return atan(math.tan((theta - turtlePose.theta)/2))

#def distance()
	#return sqrt((coords[1]-turtlePose.x)^2 + (coords[0]-turtlePose)^2)



if __name__=="__main__":
	try :
		Subscriber_pose()

	except rospy.ROSInterruptException:
		pass
