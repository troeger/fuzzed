#include "FuzzTreeConfigClient.h"

#include "FuzzTreeTransform.h"
#include "beanstalkdconfig.h"

#include <boost/format.hpp>

using namespace Beanstalkpp;
using namespace std;

FuzzTreeConfigClient::FuzzTreeConfigClient(const string& serverIP, int port)
	: Client(serverIP, port)
{
	try
	{
		Client::connect();

		Client::use(BEANSTALK_CONFIG_RESULT_QUEUE);
		Client::watch(BEANSTALK_CONFIG_QUEUE);
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
		const auto jobXML = j.asString();

		FuzzTreeTransform transform(jobXML);
		
		Client::put( 
			(boost::format("[%1] \n %2") 
				% j.getJobId() 
				% concatXMLString(transform.transform())).str() );
		Client::del(j);
	}
}

std::string FuzzTreeConfigClient::concatXMLString(const std::vector<faulttree::FaultTree>& trees)
{
	return ""; // TODO
}
