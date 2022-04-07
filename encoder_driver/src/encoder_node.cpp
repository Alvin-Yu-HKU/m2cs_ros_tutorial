#include "ros/ros.h"
#include "std_msgs/Int32.h"
#include <sstream>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>

#include <linux/can.h>
#include <linux/can/raw.h>


// add the includes needed for socketCAN

int main(int argc, char **argv)
{
  ros::init(argc, argv, "encoder_node");
  ros::NodeHandle nh;
  ros::Rate loop_rate(1.0);
  ros::Publisher encoder_pub = nh.advertise<std_msgs::Int32>("p_feedback", 1000);

    // set up socket
	int s; 
	struct sockaddr_can addr;
	struct ifreq ifr;
	struct can_frame frame;


	if ((s = socket(PF_CAN, SOCK_RAW, CAN_RAW)) < 0) {
		perror("Socket");
		return 1;
	}

	strcpy(ifr.ifr_name, "vcan0" );
	ioctl(s, SIOCGIFINDEX, &ifr);

	memset(&addr, 0, sizeof(addr));
	addr.can_family = AF_CAN;
	addr.can_ifindex = ifr.ifr_ifindex;

	if (bind(s, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
		perror("Bind");
		return 1;
	}

  int count = 0;
  int nbytes;
  int i;
  int numberOfBits = 0;
  int c = 0;

  while (ros::ok())
  {
    // read the CAN frame
    nbytes = read(s, &frame, sizeof(struct can_frame));
    if (nbytes < 0) {
	perror("Read");
	return 1;
    }
    printf("0x%03X [%d] ",frame.can_id, frame.can_dlc);
    for (i = 0; i < frame.can_dlc; i++){
	printf("%02X ",frame.data[i]);
	printf("// %d //",frame.data[i]);
    }
    printf("\r\n");
    
    std_msgs::Int32 msg;
    // fill in msg based on the contents from CAN frame
    // publish msg
    for (i = 0; i < frame.can_dlc; i++){
    	printf("i: %d",i);
    	printf("\r\n");
	if(i>2){
	  msg.data = msg.data + (frame.data[i] << (numberOfBits));
	  printf("frame data: %d",frame.data[i] << (numberOfBits));
	  c = c+1;
	  if(frame.data[i] != 0){
		  numberOfBits = numberOfBits + (int)log2(frame.data[i])+1+c;
		  printf("msg: %d",msg.data);
		  printf("\r\n");
		  printf("bits: %d",numberOfBits);
		  printf("\r\n");
	  }
	}
	
    }
    encoder_pub.publish(msg);
    
    loop_rate.sleep();
    ros::spinOnce();
    
    count++;
  }

    // close socket

  return 0;
}

