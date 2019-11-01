#! /usr/bin/env python
# -*- coding: utf-8 -*-

from std_msgs.msg import Header
from geometry_msgs.msg import TwistStamped, Twist, Vector3Stamped, Vector3
from moveit.task_constructor import core, stages
from math import pi
import time

from moveit.python_tools import roscpp_init
roscpp_init("mtc_tutorial")

group = "panda_arm"
eef_frame = "panda_link8"

# Cartesian interpolation planner
cartesian = core.CartesianPath()

task = core.Task()

# start from current robot state
task.add(stages.CurrentState("current state"))

# move along x
move = stages.MoveRelative("x +0.2", cartesian)
move.group = group
header = Header(frame_id = "world")
move.setDirection(Vector3Stamped(header=header, vector=Vector3(0.2,0,0)))
task.add(move)

# move along y
move = stages.MoveRelative("y -0.3", cartesian)
move.group = group
move.setDirection(Vector3Stamped(header=header, vector=Vector3(0,-0.3,0)))
task.add(move)

# rotate about z
move = stages.MoveRelative("z +90°", cartesian)
move.group = group
move.setDirection(TwistStamped(header=header, twist=Twist(angular=Vector3(0,0,pi/4.))))
task.add(move)

# moveTo named posture
move = stages.MoveTo("moveTo ready", cartesian)
move.group = group
move.setGoal("ready")
task.add(move)


if task.plan():
    task.publish(task.solutions[0])
time.sleep(100)

