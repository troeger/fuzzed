import logging, minbool
logger = logging.getLogger('FuzzEd')

def get(formula):
    result = []
    simplified = minbool.simplify(formula)
    cutsets = str(simplified).split('or')

    for cutset in cutsets:
        cutset = cutset.replace('(','').replace(')', '')
        result.append({'nodes': [int(term) for term in cutset.split() if term.isdigit()]})
    logging.debug('[CUTSETS] results are %s' % result)

    return result