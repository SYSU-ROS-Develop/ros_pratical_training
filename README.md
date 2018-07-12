# 中山大学软件工程实训 - 面向云机器人开发
## 图书馆自动取书系统

### 项目介绍
本项目为图书馆云机器人自动取书系统。
用户通过在浏览器端发起取书任务，机器人即可自动出发前往对应的书架位置取书。机器人取书后返回原位，接受下一个任务。当没有队列中没有任务时，机器人会自动轮询云端的数据库，当有新的任务到达时，机器人会自动出发。
本项目基于 Ubuntu 16.04 LTS + ROS kinectic + Turtlebot3 + gazebo 7.11 模拟实现。

### 配置教程：
1. 拉取仓库
2. 进入`ros_pratical_training/catkin_ws/`,执行`$ catkin_make`
3. 执行`source devel/setup.bash`
4. 执行`roslaunch turtlebot3_gazebo library.launch`
5. 执行`roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=xxxxx/map.yaml`这里xxxxx为工作空间下的`map/`目录
6. 执行`rosrun beginner_turorials talker.py`
7. 访问[取书页面](http://meal.mlg.kim/interface.html)，添加任务（目前数据库只录入了四大名著的名字，有需求可以再添加）。
8. 初次运行需要将机器人复位，执行`rostopic pub -1 /move_base_simple/goal geometry_msgs/PoseStamped '{header: {stamp: now, frame_id: "map"}, pose: {position: {x: -2.9, y: -0.0, z: 0.0}, orientation: {w: 1.0}}}'`

### 需求分析
1.	需求痒点
“我们如何在图书馆里找到一本书？”
(1)	使用图书馆的电脑查询书的粗略位置、ISBN等信息
(2)	到图书馆对应的位置
(3)	根据书的分类找到对应的书架
(4)	在书架上找到这本书
痒点：取书流程复杂、存书量巨大，书的类别多而杂、取书受时间空间限制。
2.	项目优势
(1)	大幅简化找书的流程，提高效率。
(2)	减少图书馆内的走动，保持图书馆安静。
(3)	图书馆可以增大藏书密度，提高存书量。
(4)	破除取书的时间和空间限制。提前取书，即拿即走。

### 项目结构
![img1](https://github.com/SYSU-ROS-Develop/ros_pratical_training/blob/dev-jerry/doc/imgs/1.png)
	前端：一个简单的表格提交页面，用于发起取书请求。
	服务器端：接受取书请求，检验请求合法性后加入到请求队列中。
	数据库端：存储书名和书的对应位置，以及请求队列。
	机器人控制端：轮询数据库，根据请求查询书的位置并将坐标发送到机器人。
	机器人：根据控制端发来的数据自动导航取书。
系统构建过程
1.	建立虚拟世界地图。
 ![img2] (https://github.com/SYSU-ROS-Develop/ros_pratical_training/blob/dev-jerry/doc/imgs/2.jpg)
在gazebo模拟器中建立模拟现实世界的地图，此处即图书馆。
2.	扫描地图
![img4] (https://github.com/SYSU-ROS-Develop/ros_pratical_training/blob/dev-jerry/doc/imgs/map.jpg)
使用机器人对地图进行扫描，记录地图数据。
3.	加入导航控制
![img3] (https://github.com/SYSU-ROS-Develop/ros_pratical_training/blob/dev-jerry/doc/imgs/3.jpg)
此处使用了Turtlebot3提供的navigation库，能够实时规划路线并导航。
4.	加入云服务功能
编写前端页面、后端服务器页面，以及查询任务队列的ROS节点，并建立该节点与navigation节点的通信，从而控制机器人导航。
部署方法
安装运行环境（Ubuntu 16.04+ROS Kinectic+Turtlebot3+gazebo7.11）后，将项目clone至工作目录下，执行catkin_make和source devel/setup.bash后，依次在不同的Terminal中执行cmd文件中的命令。
### 项目过程中的困难
1.	崭新的领域
ROS对于我们是一个崭新的领域，我们所有的小组成员都是零基础开始接触ROS和机器人。虽然ROS的Wiki上有最基本的教程，但仍不能满足开发这个系统的需要，我们仍然花了大量的时间来摸索ROS的机制。
2.	学习资料较少
虽然当时技术选型时有意选择了学习资料较多的机器人型号（Turtlebot3），但由于手头没有实际的机器人，我们不得已使用gazebo来进行机器人的模拟实现。然而基于gazebo的Turtlebot3学习资料实在不多，我们花了相当多的时间纠缠在gazebo的问题上。
3.	版本兼容问题
这里的版本问题涉及到Turtlebot版本、Ubuntu版本、ROS版本、gazebo版本，这些版本之间的互相支持并不是特别好，且没有确切的文档说明。我们花了不少的时间，最后摸索出Ubuntu16.04+ROS Kinectic+Turtlebot3+gazebo7.11的搭配，能够比较好地兼容彼此。
4.	机器人特性
我们发现Turtlebot3地图系统一个潜在的问题：如果建立的地图中有不同的部分完全相似的话，Turtlebot3会混淆这两个地方，导致地图扫描出现错误。我们卡在这个地方研究了相当长的一段时间才发现并解决这个问题。
5.	电脑性能
我们也曾尝试运行更为拟真的地图（见下），但由于电脑性能的原因，加载这个地图时gazebo会失去响应。而且也因为地图扫描的问题，我们选择了建立更加简单的地图。
![img4] (https://github.com/SYSU-ROS-Develop/ros_pratical_training/blob/dev-jerry/doc/imgs/4.jpg)

### 有待改进
该项目离实用仍有较大差距，目前看到可以完善的点：
1.	实现多机器人部署
2.	一次行程取多本书籍。
3.	增加机械臂等部件，真正完成取书功能。
