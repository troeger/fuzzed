#pragma once

#include <string>
#include <client.h>

class FuzzTreeConfigClient final : public Beanstalkpp::Client
{
public:
	FuzzTreeConfigClient(const std::string& tubeName, const std::string& serverIP, int port);
	void run();
	
private:
	std::string m_tubeName;
};