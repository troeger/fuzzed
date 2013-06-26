import beanstalkc, tempfile, os, shutil, signal

def shutdown(sig, func=None):
    print "Shutting down beanstalk connection ..."
    b.close()    

# Register cleanup code for termination
signal.signal(signal.SIGTERM, shutdown)
b=beanstalkc.Connection()
# We expect the requester to send the graph TIKZ code through the "rendering" tube
b.watch('rendering')
b.use('renderingResults')
while 1:
    job=b.reserve()
    # perform Latex compilation in temporary directory
    tmpdir = tempfile.mkdtemp() 
    # Store TiKZ code there
    f = open(tmpdir+os.sep+'graph.tex','w')
    f.write(job.body)
    f.close()
    # Copy the neccessary image files for Latex compilation
    #TODO: This should be smarter
    for root, dirs, files in os.walk('rendering/img/'):
        for f in files:
            if f.endswith('.eps'):
                print "Copying "+f
                shutil.copy(root+os.sep+f, tmpdir)
    # Run Latex, copy result pdf document to current directory
    # pdflatex really sucks in being run with files in another directory,
    # so we simply got their for the time being
    olddir = os.getcwd()
    os.chdir(tmpdir)
    os.system("latex graph.tex")
    os.system("dvips graph")
    os.system("ps2eps -R + -f -a graph.ps")
    # read resulting file content
    result = open(tmpdir+os.sep+"graph.eps","r")
    # send back the result via messaging, provide original job ID as prefix
    b.put("[%u]\n%s"%(job.stats()['id'], result.read()))
    # clean up
    job.delete()
    result.close()
    os.chdir(olddir)
    shutil.rmtree(tmpdir, ignore_errors=True)

