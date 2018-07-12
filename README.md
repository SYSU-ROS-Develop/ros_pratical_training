# 中山大学软件工程实训 - 面向云机器人开发
## 图书馆自动取书系统

目前仓库环境设置：ubuntu 16.04 LTS + ROS kinectic + Turtlebot3 + gazebo 7.11
**配置教程：**
1. 拉取仓库
2. 进入`ros_pratical_training/catkin_ws/`,执行`$ catkin_make`
3. 执行`source devel/setup.bash`
4. 执行`roslaunch turtlebot3_gazebo library.launch`
5. 执行`roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=xxxxx/map.yaml`这里xxxxx为工作空间下的`map/`目录
6. 执行`rosrun beginner_turorials talker.py`
7. 访问[取书页面](http://meal.mlg.kim/interface.html)，添加任务（目前数据库只录入了四大名著的名字，有需求可以再添加）。
8. 初次运行需要将机器人复位，执行`rostopic pub -1 /move_base_simple/goal geometry_msgs/PoseStamped '{header: {stamp: now, frame_id: "map"}, pose: {position: {x: -2.9, y: -0.0, z: 0.0}, orientation: {w: 1.0}}}'`
