from SCons.Script import * 
import os

def patch(target, source, env):
    ''' 
    	The first file in the source list is the patch file,
    	then comes the file to be patched.
    	The target argument contains the file to be created.
    '''
    patch_file = str(source[0])
    assert(patch_file.endswith('.patch'))
    orig_file = str(source[1])
    target_file = str(target[0])
    print "Patching third party code ..."
    os.system("patch -o %s %s %s"%(target_file, orig_file, patch_file))

patchbuilder = Builder(action = patch)
