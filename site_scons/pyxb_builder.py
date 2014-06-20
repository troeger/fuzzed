from SCons.Script import * 

#TODO: Take source XSD and target PY module from Builder arguments

def build_xmlschema_wrappers(target, source, env):

    IS_WINDOWS     = os.name == 'nt'
    FILE_EXTENSION = '.py' if IS_WINDOWS else ''

    # generate new bindings
    if os.system('pyxbgen%(extension)s -u %(source)s -m %(target)s' % {
        'extension': FILE_EXTENSION,
        'source':    str(source[0]),
        'target':    str(target[0])
    }) != 0:
        raise Exception('Execution of pyxbgen failed.')

# Define Builder for Django config file from settings INI file
pyxbbuilder = Builder(action = build_xmlschema_wrappers,
                      suffix = '.py',
                      src_suffix = '.xsd')

