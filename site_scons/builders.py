from SCons.Script import * 
from setup_settings import createDjangoDevSettings, createBackendSettings

def add_to_env(env):
    # Define Builder for lessc compiler
    lessbuilder = Builder(action='lessc $SOURCE $TARGET',
                          suffix = '.css',
                          src_suffix = '.less')
    env.Append(BUILDERS = {'Lessc' : lessbuilder})

    # Define Builder for Django config file from settings INI file
    djangoconfbuilder = Builder(action = createDjangoDevSettings,
                                suffix = '.py',
                                src_suffix = '.ini')
    env.Append(BUILDERS = {'DjangoConfig' : djangoconfbuilder})

    # Define Builder for Backend daemon config file from settings INI file
    daemonconfbuilder = Builder(action = createBackendSettings,
                                suffix = '.ini',
                                src_suffix = '.ini')
    env.Append(BUILDERS = {'DaemonConfig' : daemonconfbuilder})
