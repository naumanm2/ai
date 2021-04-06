
from logic import *

# Mapping from actions and initial and goal states to a formula

# Turn variable name 'x' to an atomic formula 'x@t'.

def timedVar(varname,time):
    return ATOM(varname + "@" + str(time))

# Turn action name 'x' to an atomic formula 'x@t'.

def timedAction(varname,time):
    return ATOM("ACTION" + varname + "@" + str(time))

# Two actions cannot be taken at the same time?

def exclusive(c1,pe1,ne1,c2,pe2,ne2):
    return (bool(set(c1) & set(ne2))) or (bool(set(ne1) & set(c2)))

# Map a reachability problem to a propositional formula

def reachability2fma(init,goal,actions,T):
    initvars = { v for v in init }
    goalvars = { v for v in goal }
    actioncvars = { v for n,c,pe,ne in actions for v in c }
    actionpvars = { v for n,c,pe,ne in actions for v in pe }
    actionnvars = { v for n,c,pe,ne in actions for v in ne }
    varsets = [initvars,goalvars,actioncvars,actionpvars,actionnvars]
    allStateVars = set().union(*varsets)

    initformulas = [ timedVar(v,0) for v in initvars ] + [ NOT(timedVar(v,0)) for v in allStateVars if v not in initvars ]

    goalformulas = [ timedVar(v,T) for v in goalvars ]

    preconditions = [ IMPL(timedAction(n,t),timedVar(x,t)) for n,c,pe,ne in actions for t in range(0,T) for x in c ]

    posEffects = [ IMPL(timedAction(n,t), timedVar(x,t+1)) for n,c,pe,ne in actions for t in range(0, T) for x in pe ]

    negEffects = [ IMPL(timedAction(n,t), NOT(timedVar(x,t+1))) for n,c,pe,ne in actions for t in range(0, T) for x in ne]

    posFrameAxioms = [ IMPL(AND([NOT(timedVar(x,t)),timedVar(x,t+1)]),OR([ timedAction(n,t) for n,c,pe,ne in actions if x in pe ])) for t in range(0,T) for x in allStateVars ]
    
    negFrameAxioms = [ IMPL(AND([timedVar(x,t),NOT(timedVar(x,t+1))]),OR([ timedAction(n,t) for n,c,pe,ne in actions if x in ne ])) for t in range(0,T) for x in allStateVars ]

#    negFrameAxioms = [ IMPL( AND( [timedVar(x, t), NOT(timedVar(x, t+1))] ), OR([timedAction(n,t) for n,c,pe,ne in actions])) for n,c,pe,ne in actions for t in range(0, T) for x in ne ]

    actionMutexes = [ NOT(AND([timedAction(n1,t),timedAction(n2,t)])) for t in range(0,T) for n1,c1,pe1,ne1 in actions for n2,c2,pe2,ne2 in actions if not(n1 == n2) and exclusive(c1,pe1,ne1,c2,pe2,ne2) ]

    return AND(initformulas + goalformulas + preconditions + posEffects + negEffects + posFrameAxioms + negFrameAxioms + actionMutexes)
