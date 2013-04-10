import minbool

def getcutsets(structformula):
    result=[]
    res = minbool.simplify(structformula)
    sets = str(res).split("or")
    for s in sets:
        s=s.replace("(","")
        s=s.replace(")","")
        andnodes = [int(el) for el in s.split(" ") if el.isdigit()]
        result.append({"nodes": andnodes})
    return result