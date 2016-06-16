#include "ros/ros.h"
#include "sensor_msgs/LaserScan.h"
#include "ros/spinner.h"
#include <iostream>

// schussstärke zwischen 101 & 3.5k
// schussweite ca 12m
void chatterCallback(sensor_msgs::LaserScanPtr msg)
{
    std::cout<<"in callback"<< std::endl;
    ROS_INFO("I heard: [%f]", msg->ranges[1]);
}

int main(int argc, char **argv)
{
//   std::cout<<"test"<<std::endl;
    ros::init(argc, argv, "subscriber");
    ros::NodeHandle *n = new ros::NodeHandle();
    ros::Subscriber sub = n->subscribe("scan", 1000, chatterCallback);

    if(sub){
        std::cout<<sub<<std::endl;
        ros::AsyncSpinner *spinner = new ros::AsyncSpinner(3);
        spinner->start();
        while(ros::ok())
        {
            sleep(1);
        }

        sub.shutdown();
        delete sub;
    }
    else
    {
        std::cout<<"no sub"<<std::endl;
    }

  return 0;
}
-
