''' Dummy backend implementation. '''

import sys

working_dir, input_file, output_files = sys.argv[1:4]

print "Dummy was called with the following arguments: "
print "     Working dir:  "+working_dir
print "     Input file:   "+input_file
print "     Output files: "+output_files


if output_files.startswith("*"):
	suffix = output_files[1:]
	open(working_dir+"/foo"+suffix,"w").close()
	open(working_dir+"/bar"+suffix,"w").close()
else:
	open(working_dir+"/"+output_files)
