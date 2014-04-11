import tempfile, os, shutil, signal, sys, ConfigParser, logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('FuzzEd')

# Determine parameters from command line 
if len(sys.argv) != 6:
    logger.error('%s [--eps|--pdf] <working_dir> <input file> <output file> <log file>'%sys.argv[0])
    exit(-1)
kind = sys.argv[1][2:]   
working_dir = sys.argv[4] 
input_fname = sys.argv[2]
output_fname = sys.argv[3]

# Only needed for Ubuntu 12.10, all others have it as part of the installation
shutil.copy("rendering/adjustbox.sty", working_dir)
shutil.copy("rendering/collectbox.sty", working_dir)
shutil.copy("rendering/adjgrfx.sty", working_dir)

# Latex cannot operate well on files in another directory, so we go there directly
# This is anyway epxected to be the temporary job execution directory created by the daemon
olddir = os.getcwd()
os.chdir(working_dir)
os.rename(input_fname, 'graph.tex')
exit_code = -1
if kind == 'eps':
    os.system("latex -interaction nonstopmode graph.tex")
    if os.path.exists('graph.dvi'):
        os.system("dvips graph")
        os.system("ps2eps -R + -f -a graph.ps")
        os.rename('graph.eps', output_fname)
        exit_code = 0
elif kind == 'pdf':
    os.system("pdflatex -interaction nonstopmode graph.tex")
    if os.path.exists('graph.pdf'):
        os.rename('graph.pdf', output_fname)
        exit_code = 0

os.chdir(olddir)
exit(exit_code)