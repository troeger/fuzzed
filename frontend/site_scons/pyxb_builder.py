from SCons.Script import *


def build_xmlschema_wrappers(target, source, env):
    '''
        SCons needs real file names, so the main script must use proper file
        name suffixes for the Python file.

        PyXBGen, however, wants no .py suffix, otherwise modules are generated.
        Therefore, we strip the suffix before calling PyXBGen.

        Wee also need to use a proper "--binding-root" parameter, otherwise
        the path names become part of the generated Python module names
    '''

    sources = [str(src) for src in source]

    # Targets are the Python modules to be generated
    # If they all share the same directory prefix, then strip it and
    # use it as binding root. This gives relative imports in the generated
    # Python code, which is nicer
    prefix = ""
    all_same_prefix = True
    for t in target:
        new_prefix = str(t).rsplit('/', 1)[0]
        if new_prefix != prefix:
            if prefix == "":
                prefix = new_prefix
            else:
                all_same_prefix = False
        prefix = new_prefix

    if all_same_prefix:
        targets = [str(trg).rsplit('/', 1)[1].rsplit('.')[0] for trg in target]
        modulespec = ['-u %s -m %s' % (src, trg)
                      for src, trg in zip(sources, targets)]
        cmdline = 'pyxbgen --binding-root=' + \
            prefix + ' ' + ' '.join(modulespec)
    else:
        targets = [str(trg).rsplit('.')[0] for trg in target]
        modulespec = ['-u %s -m %s' % (src, trg)
                      for src, trg in zip(sources, targets)]
        cmdline = 'pyxbgen ' + ' '.join(modulespec)

    print cmdline
    if os.system(cmdline) != 0:
        raise Exception('Execution of pyxbgen failed.')


# Define Builder for Django config file from settings INI file
pyxbbuilder = Builder(action=build_xmlschema_wrappers)
