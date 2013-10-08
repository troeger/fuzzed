import tempfile, os, shutil, signal, sys, ConfigParser
from .pg_msgqueue import PgMessageQueue

def shutdown(sig, func=None):
    print "Shutting down beanstalk connection ..."
    b.close()    

# Initialize message queue, based on config file given on the command line
if len(sys.argv) != 2:
    print("%s configFile"%sys.argv[0])
    exit(-1)
queue = PgMessageQueue(sys.argv[1], ('renderEps','renderPdf'))

# Register cleanup code for termination
signal.signal(signal.SIGTERM, shutdown)

# We expect the requester to send the database ID in the TikzCache table
while 1:
    message = queue.pull_message()
    tikzCacheId = int(message['payload'])
    # perform Latex compilation in temporary directory
    tmpdir = tempfile.mkdtemp() 
    # Store TiKZ code there
    f = open(tmpdir+os.sep+'graph.tex','w')
    tikzCode = 
    f.write(job.body)
    f.close()
    # Run Latex, copy resulting document to current directory
    # pdflatex really sucks in being run with files in another directory,
    # so we simply got their for the time being
    olddir = os.getcwd()
    os.chdir(tmpdir)
    latexError = False
    if tube == 'renderEps':
        os.system("latex -interaction nonstopmode graph.tex")
        if os.path.exists('graph.dvi'):
            os.system("dvips graph")
            os.system("ps2eps -R + -f -a graph.ps")
            # read resulting file content
            result = open(tmpdir+os.sep+"graph.eps","r")
            b.use('renderEpsResult')
        else:
            print "Error during LaTex compilation"
            latexError = True
    elif tube == 'renderPdf':
        os.system("pdflatex -interaction nonstopmode graph.tex")
        if os.path.exists('graph.pdf'):
            # read resulting file content
            result = open(tmpdir+os.sep+"graph.pdf","r")
            b.use('renderPdfResult')
        else:
            print "Error during LaTex compilation"
            latexError = True
    if not latexError:
        # send back the result via messaging, provide original job ID as prefix
        b.put("[%u]\n%s"%(job.stats()['id'], result.read()))
        result.close()
        job.delete()
    else:
        job.bury()
    # clean up
    os.chdir(olddir)
    shutil.rmtree(tmpdir, ignore_errors=True)

