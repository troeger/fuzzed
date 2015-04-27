from SCons.Script import * 
from contextlib import contextmanager
import os, tarfile

def package_builder(target, source, env):
    '''
    	Performs packaging.
    '''    
    # Remove first directory part of target name,
    # so "dist/foo_v1.0" becomes "foo_v1.0"
    target_name = str(target[0]).split('/',1)[1]
    inclusions = [[str(s), str(s)] for s in source]
    exclusion_suffix=[".pyc", ".sqlite", ".orig"]
    exclusion_files = []
    exclusion_dirs = [".git"]

    def tarfilter(tarinfo):
        fname = tarinfo.name
        if tarinfo.isdir():
            for dirname in exclusion_dirs:
                # if the filter is "/static", we still want to add "/static-release"
                if fname.endswith(dirname) or dirname+os.sep in fname:
                    print "Skipping directory "+fname
                    return None
            print "Adding directory "+fname
            return tarinfo
        elif tarinfo.isfile():
            if fname in exclusion_files:
                print "Skipping file "+fname
                return None
            for suffix in exclusion_suffix:
                if fname.endswith(suffix):
                    print "Skipping file "+fname
                    return None
            print "Adding file "+fname
            return tarinfo

    tar = tarfile.open(str(target[0])+".tar.gz","w:gz")
    for src, dest in inclusions:
        tar.add(src, dest, filter=tarfilter)
    tar.close()

packagebuilder = Builder(action=package_builder)
