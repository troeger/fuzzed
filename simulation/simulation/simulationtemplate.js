// parameters:
count = %1%;
simulationTime = %2%;
netName = "%3%";
fileName = "%4%";

folder = new java.io.File(fileName.slice(0,fileName.lastIndexOf("."))+".log");
folder.mkdir();

println("Starting Javascript");
for(i = 0; i<count; i++)
{
	// copy net file
	str = fileName.replace(".xml",i+".xml");
	newFile = new java.io.File(str);     
	oldFile = new java.io.File(fileName);
	inChannel = new java.io.FileInputStream(oldFile).getChannel();
	outChannel = new java.io.FileOutputStream(newFile).getChannel();
	inChannel.transferTo(0,inChannel.size(),outChannel);
	inChannel.close();
	outChannel.close();
	
	parameters = new Packages.client.SimulationParameters("0", simulationTime, true);
	parameters.setServerIP("localhost");
	parameters.setServerPort("4455");
	parameters.setResultIP("localhost");
	parameters.setResultPort("4455");
	parameters.setLogging(true)
	gpsc_instance.startSimulation(fileName, parameters);
	println("simulation #" + (i+1) + " done");
	
	//copy logfiles to result folder
	dir = new java.io.File(netName+"_script"+i+".log");
	dir.mkdir();
	println("Copying results from round "+i);
	inSim = new java.io.File(folder+"\\sim.log");
	outSim = new java.io.File(dir+"\\sim"+i+".log");
	inChannel = java.io.FileInputStream(inSim).getChannel();
	outChannel = java.io.FileOutputStream(outSim).getChannel();
	inChannel.transferTo(0,inChannel.size(),outChannel);
	inChannel.close();
	outChannel.close();

	//delete xml files of subnets
	deleteMethod = dir.getClass().getDeclaredMethod("delete", null);
	xmlFile = java.io.File(netName+"_script"+i+".xml");
	deleteMethod.invoke(xmlFile,null);

	//delete generated folders
	println("Tidying up round "+i);
	fileDeleter = java.io.File(dir+"\\server.log");
	deleteMethod.invoke(fileDeleter,null);
	fileDeleter = java.io.File(dir+"\\sim.log");
	deleteMethod.invoke(fileDeleter,null);
	deleteMethod.invoke(dir,null);
	fileDeleter = java.io.File(netName+"_script"+i+".result\\results.log");
	deleteMethod.invoke(fileDeleter,null);
	fileDeleter = java.io.File(netName+"_script"+i+".result");
	deleteMethod.invoke(fileDeleter,null);
	}