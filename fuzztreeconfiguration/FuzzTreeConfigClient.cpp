#include "FuzzTreeConfigClient.h"

#include "beanstalkdconfig.h"

using namespace Beanstalkpp;
using namespace std;

FuzzTreeConfigClient::FuzzTreeConfigClient(const string& tubeName, const string& serverIP, int port)
	: Client(serverIP, port), m_tubeName(tubeName)
{
	try
	{
		Client::connect();
	} 
	catch (exception& e)
	{
		cerr << e.what() << endl;
		exit(1);
	}
}

void FuzzTreeConfigClient::run()
{
	while (true) 
	{
		Job j = Client::reserve();
		printf("Received job:\n%s\n", j.asString().c_str());
		Client::del(j);
	}
}
