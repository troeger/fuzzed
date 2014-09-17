from less_builder import lessbuilder
from pyxb_builder import pyxbbuilder
from conf_builder import confbuilder
from tikz_builder import tikzbuilder
from notations_builder import notationsbuilder
from package_builder import packagebuilder
from patch_builder import patchbuilder
from run_commands import *

def fuzzed_builders(env):
	env.Append(BUILDERS = 
				{
					'Lessc' : lessbuilder,
					'FuzzedConfig' : confbuilder,
					'PyXB' : pyxbbuilder,
					'Tikz' : tikzbuilder,
					'Notations' : notationsbuilder,
					'Package' : packagebuilder,
					'Patch' : patchbuilder
				})

