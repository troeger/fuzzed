#pragma once
#include <memory>
#include "Model.h"
#include "events/TopLevelEvent.h"

std::shared_ptr<TopLevelEvent> fromGraphModel(const Model& graphMLModel);

void convertFaultTreeRecursive(
	std::shared_ptr<FaultTreeNode> node,
	const Node& templateNode,
	const unsigned int& missionTime);