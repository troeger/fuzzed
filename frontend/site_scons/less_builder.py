from SCons.Script import * 

lessbuilder = Builder(action='lessc $SOURCE $TARGET',
                      suffix = '.css',
                      src_suffix = '.less')
