#!/usr/bin/env python
#coding:utf-8
# license removed for brevity
import rospy
import time
import urllib
import json

from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
from std_msgs.msg import Header
from move_base_msgs.msg import MoveBaseActionResult
from tf.transformations import quaternion_from_euler

status = 1
t = 0

def callback(data):
    if data.status.status is 3:
        global status
        status = -status
        talker()
        #global t
        #if time.time() - t > 5:

        #rospy.loginfo("status:%s", status)


def listener():

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/move_base/result", MoveBaseActionResult, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


def talker():
    pub = rospy.Publisher('/move_base_simple/goal',PoseStamped,queue_size = 10)#创建一个话题
    #rospy.init_node('talker',anonymous = True)#声明一个发布话题的节点
    #hello_str = "hello world %s" % time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    interval = 3
    try:           
        global status
        message = PoseStamped()
        message.header.stamp = rospy.get_rostime()
        message.header.frame_id = '/map'
        if status is 1:
            formertime = time.time()
            while 1:
                if time.time() - formertime > interval:
                #time_remaining = interval - time.time() % interval
                #time.sleep(time_remaining) 
                    testHtml = urllib.urlopen('http://meal.mlg.kim/query/get_pos')
                    testHtml1 = testHtml.read()
                    testJson = json.loads(testHtml1)
                    if testHtml is not None:
                        rospy.loginfo("Fetch from database.")
                        global t
                        t = time.time()
                        message.pose.position.x = testJson['pos_x']
                        message.pose.position.y = testJson['pos_y']
                        message.pose.position.z = 0.000
                        q = quaternion_from_euler(0.0, 0.0, 0.0)
                        message.pose.orientation = Quaternion(*q)
                        #rospy.loginfo(message)#将数据打印出来
                        pub.publish(message)#将数据发送到话题上
                        break
                    else :
                        formertime = time.time()
                        rospy.loginfo("waiting.")
                        continue
                else :
                    rospy.loginfo("waiting.")
                    continue
        if status is -1:
            message.pose.position.x = -2.8
            message.pose.position.y = 0.0
            message.pose.position.z = 0.000
            q = quaternion_from_euler(0.0, 0.0, 0.0)
            message.pose.orientation = Quaternion(*q)
            rospy.loginfo("Going home.")
            #rospy.loginfo(message)#将数据打印出来
            pub.publish(message)#将数据发送到话题上
    except Exception, e:
        print e

if __name__ == '__main__':
    listener()

 