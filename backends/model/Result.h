#pragma once

class Result
{
public:
	const std::string& getModelId() const		{ return m_modelId; };
	const std::string& getId() const			{ return m_id; };
	const std::string& getTimestamp() const;	{ return m_timestamp; };

private:
	Result(std::string modelId, std::string id, std::string timestamp)
		: m_modelId(modelId), m_id(id), m_timestamp(timestamp) {};

	std::string m_modelId;
	std::string m_id;
	std::string m_timestamp;
};