import beanstalkc, tempfile, os, shutil, signal

def shutdown(sig, func=None):
    print "Shutting down beanstalk connection ..."
    b.close()    

# Register cleanup code for termination
signal.signal(signal.SIGTERM, shutdown)
b=beanstalkc.Connection()
# We expect the requester to send the graph TIKZ code through the "rendering" tube
b.watch('renderEps')
b.watch('renderPdf')
while 1:
    job=b.reserve()
    tube = job.stats()['tube']
    # perform Latex compilation in temporary directory
    tmpdir = tempfile.mkdtemp() 
    # Store TiKZ code there
    f = open(tmpdir+os.sep+'graph.tex','w')
    f.write(job.body)
    f.close()
    # Run Latex, copy resulting document to current directory
    # pdflatex really sucks in being run with files in another directory,
    # so we simply got their for the time being
    olddir = os.getcwd()
    os.chdir(tmpdir)
    if tube == 'renderEps':
        os.system("latex graph.tex")
        os.system("dvips graph")
        os.system("ps2eps -R + -f -a graph.ps")
        # read resulting file content
        result = open(tmpdir+os.sep+"graph.eps","r")
        b.use('renderEpsResult')
    elif tube == 'renderPdf':
        os.system("pdflatex graph.tex")
        # read resulting file content
        result = open(tmpdir+os.sep+"graph.pdf","r")
        b.use('renderPdfResult')
    # send back the result via messaging, provide original job ID as prefix
    b.put("[%u]\n%s"%(job.stats()['id'], result.read()))
    # clean up
    job.delete()
    result.close()
    os.chdir(olddir)
    shutil.rmtree(tmpdir, ignore_errors=True)

