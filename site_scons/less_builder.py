from SCons.Script import * 

lessbuilder = Builder(action='lesscpy $SOURCE -o $TARGET',
                      src_suffix = '.less')
