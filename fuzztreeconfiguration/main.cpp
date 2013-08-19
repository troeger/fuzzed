#include "FuzzTreeTransform.h"
#include "FuzzTreeConfigClient.h"
#include "beanstalkdconfig.h"

int main(int argc, char **argv)
{
	FuzzTreeConfigClient client(BEANSTALK_SERVER, BEANSTALK_PORT);
	client.run();
}