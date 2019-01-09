from less_builder import lessbuilder
from pyxb_builder import pyxbbuilder
from tikz_builder import tikzbuilder
from notations_builder import notationsbuilder
from package_builder import packagebuilder
from patch_builder import patchbuilder


def ore_builders(env):
    env.Append(BUILDERS={
        'Lessc': lessbuilder,
        'PyXB': pyxbbuilder,
        'Tikz': tikzbuilder,
        'Notations': notationsbuilder,
        'Package': packagebuilder,
        'Patch': patchbuilder
    })
