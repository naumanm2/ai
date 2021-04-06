def dpll(valuation, clauses, variables):

    def cc(v, c):
        ul = []
        for literal, polarity in c:
            if literal in v and polarity is v[literal]:
                return True, []
            if literal not in v:
                ul.append((literal, polarity))
        return False, ul

    def upp(v, c):
        q = []
        hope = True
        while hope:
            hope = False
            for clause in c:
                sat, ul = cc(v, clause)
                if not sat:
                    if len(ul)==0:
                        return False
                    if len(ul)==1:
                        v[ul[0][0]] = ul[0][1]
                        hope=True
        return True
                
    if not upp(valuation, clauses):
        return False
        
    nv = 0
    for x in variables:
        if x not in valuation:
            nv = x
            break
    
    if nv == 0:
        return True
    
    tv = valuation.copy()
    tv[nv] = True
    
    if dpll(tv, clauses, variables):
        valuation.update(tv)
        return True
    
    fv = valuation.copy()
    fv[nv] = False
    
    if dpll(fv, clauses, variables):
        valuation.update(fv)
        return True
        
    return False
    
