from SCons.Script import * 

def build_xmlschema_wrappers(target, source, env):
    '''
        SCons needs real file names, so the main script must use proper file
        name suffixes for the Python file.

        PyXBGen, however, wants no .py suffix, otherwise modules are generated.
        Therefore, we strip the suffix before calling PyXBGen.
    '''
    sources = [str(src) for src in source]
    targets = [str(trg).rsplit('.')[0] for trg in target]
    modulespec = ['-u %s -m %s'%(src, trg) for src, trg in zip(sources,targets)]

    # generate new bindings
    cmdline = 'pyxbgen '+' '.join(modulespec)
    print cmdline
    if os.system(cmdline) != 0:
        raise Exception('Execution of pyxbgen failed.')

# Define Builder for Django config file from settings INI file
pyxbbuilder = Builder(action = build_xmlschema_wrappers)


