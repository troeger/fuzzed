import faulttree, fuzztree, rbd

# What notations are installed (meaning: available AND usable)
# To extend this list import the notations and add the config to the list
installed = [faulttree.CONFIG, fuzztree.CONFIG, rbd.CONFIG]

# A map that indexes the available notations by its kind identifier
by_kind = {}
for notation in installed:
    by_kind[notation['kind']] = notation

# This is a django.db.model.Field choice mapping for all available notations
# The first element of each tuple is a unique string identifying the notation
# whereas the second element is a human readable version of it
choices = [(notation['kind'], notation['name']) for notation in installed]

# Another django.db.model.Field choice mapping for each node
# The nodes are grouped by their individual notation category
node_choices = []
for notation in installed:
    nodes = notation['nodes']
    node_category = (notation['name'],)

    for node_kind, node in nodes.items():
        node_category += ((node_kind, node['name']),)

    node_choices.append(node_category)