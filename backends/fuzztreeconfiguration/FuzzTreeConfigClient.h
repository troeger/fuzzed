// #pragma once
// 
// #include <string>
// 
// namespace fuzztree
// {
// 	class FuzzTree;
// }
// 
// class FuzzTreeConfigClient
// {
// public:
// 	FuzzTreeConfigClient(const std::string& serverIP, int port);
// 	void run();
// 	
// private:
// 	static std::string concatXMLString(const std::vector<fuzztree::FuzzTree>& trees);
// };