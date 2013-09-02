#pragma once

#include <string>
#include <client.h>

namespace fuzztree
{
	class FuzzTree;
}

class FuzzTreeConfigClient : public Beanstalkpp::Client
{
public:
	FuzzTreeConfigClient(const std::string& serverIP, int port);
	void run();
	
private:
	static std::string concatXMLString(const std::vector<fuzztree::FuzzTree>& trees);
};