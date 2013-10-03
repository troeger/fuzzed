// #include "FuzzTreeConfigClient.h"
// 
// #include "FuzzTreeTransform.h"
// #include "beanstalkdconfig.h"
// 
// #include <boost/format.hpp>
// 
// using namespace Beanstalkpp;
// using namespace std;
// 
// FuzzTreeConfigClient::FuzzTreeConfigClient(const string& serverIP, int port)
// 	: Client(serverIP, port)
// {
// 	try
// 	{
// 		cout << "Connecting Config Client... " << endl;
// 		Client::connect();
// 		cout << "...done." << endl;
// 
// 		Client::use(BEANSTALK_CONFIG_RESULT_QUEUE);
// 		Client::watch(BEANSTALK_CONFIG_QUEUE);
// 
// 		cout 
// 			<< "Watching Queue: " << BEANSTALK_CONFIG_QUEUE << endl
// 			<< "Using Queue:	" << BEANSTALK_CONFIG_RESULT_QUEUE << endl;
// 
// 		for (const auto& t : Client::listTubes())
// 			cout << " - " << t << endl;
// 	} 
// 	catch (exception& e)
// 	{
// 		cerr << "ERROR: " << e.what() << endl;
// 		exit(1);
// 	}
// }
// 
// void FuzzTreeConfigClient::run()
// {
// 	try
// 	{
// 		cout << "Running Config Client... " << endl;
// 		while (true) 
// 		{
// 			boost::shared_ptr<Job> jobPtr;
// 			Client::put("foo");
// 			Client::reserveWithTimeout(jobPtr, 1000);
// 			Client::peekReady(jobPtr);
// 			if (jobPtr)
// 			{
// 				const auto jobXML = jobPtr->asString();
// 				cout << "Received job: " << jobXML << endl;
// 
// 				FuzzTreeTransform transform(jobXML);
// 
// 				Client::put( 
// 					(boost::format("[%1] \n %2") 
// 					% jobPtr->getJobId() 
// 					% concatXMLString(transform.transform())).str() );
// 				Client::del(jobPtr);
// 			}
// 			else
// 			{
// 				cout << "Timeout without receiving job... " << endl;
// 			}
// 		}
// 	}
// 	catch (const exception& e)
// 	{
// 		cerr << "ERROR: " << e.what() << endl;
// 		exit(1);
// 	}
// }
// 
// std::string FuzzTreeConfigClient::concatXMLString(const std::vector<fuzztree::FuzzTree>& trees)
// {
// 	std::stringstream res;
// 	
// 	for (const auto& tree : trees)
// 	{
// 		fuzztree::fuzzTree(res, tree);
// 	}
// 
// 	std::cout << res;
// 	return res.str(); // TODO
// }
