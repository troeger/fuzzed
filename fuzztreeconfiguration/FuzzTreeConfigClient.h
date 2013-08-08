#pragma once

#include <string>
#include <client.h>


namespace faulttree
{
	class FaultTree;
}

class FuzzTreeConfigClient final : public Beanstalkpp::Client
{
public:
	FuzzTreeConfigClient(const std::string& serverIP, int port);
	void run();
	
private:
	static std::string concatXMLString(const std::vector<faulttree::FaultTree>& trees);
};