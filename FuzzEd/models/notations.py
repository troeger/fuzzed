try:
    import json
except ImportError:
    import simplejson as json

import os
from django.contrib.staticfiles import finders

def read_notations():
    notations_dir = finders.find('notations')
    file_list = os.listdir(notations_dir)
    notations = []

    for file in [os.path.join(notations_dir, file_name) for file_name in file_list]:
        if os.path.isfile(file) and file.endswith('.json'):
            handle = open(file)
            notations.append(json.loads(handle.read()))
            handle.close()

    return notations

notations = read_notations()

# A map that indexes the available notations by its kind identifier
by_kind = {notation['kind']: notation for notation in notations}

# This is a django.db.models.Field choice mapping for all available notations
# The first element of each tuple is a unique string identifying the notation
# whereas the second element is a human readable version of it
choices = [(notation['kind'], notation['name']) for notation in notations]

# Another django.db.models.Field choice mapping for each node
# The nodes are grouped by their individual notation category
node_choices = []
for notation in notations:
    nodes = notation['nodes']
    node_category = (notation['name'],)
    node_category_choices = ()

    for node_kind, node in nodes.items():
        if not 'name' in node: continue
        node_category_choices += ((node_kind, node['name']),)

    node_category += (node_category_choices,)
    node_choices.append(node_category)
