count = %1%;
simTime = %2%;
netPath = "%3%";
netPath.replace("\\", "/");

netName = netPath.slice(0, netPath.lastIndexOf("."));
rootDir = netPath.slice(0, netPath.lastIndexOf("\/"));

for(i = 0; i<count; i++)
{
	//create parameters
	parameters = new Packages.client.SimulationParameters("0", simTime, true);
	parameters.setServerIP("localhost");
	parameters.setServerPort("4445");
	parameters.setResultIP("localhost");
	parameters.setResultPort("4455");
	parameters.setLogging(true);
	
	//start simulation	
	gpsc_instance.startSimulationNoResultmonitor(netPath, parameters);
	println("simulation #" + (i+1) + " done");

	//copy files to safety
	dir = new java.io.File(rootDir + "\/log"+i);			
	dir.mkdir();
	
	logName = netName + ".log"+"\/sim.log";
	outName = dir+"\/sim"+i+".log";
	println("copy " + logName + " to " + outName);
	println("###");
	inSim = new java.io.File(logName);
	outSim = new java.io.File(outName);
	inChannel = java.io.FileInputStream(inSim).getChannel();
	outChannel = java.io.FileOutputStream(outSim).getChannel();
	inChannel.transferTo(0,inChannel.size(),outChannel);
	inChannel.close();
	outChannel.close();
}