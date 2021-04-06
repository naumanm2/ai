
from plans import PlanNode, PlanEmpty

import random

#
# Find a plan that solves a partially observable planning problem
#

# Identify all actions applicable in a state set.
# This is the intersection of the sets of actions
# applicable in each state.

def Bapplicable(bstate0):
    bstate = bstate0.copy()
    s = bstate.pop()
    actions = s.applActions()
    def inall(a):
        for s2 in bstate:
            if not a in s2.applActions():
                return False
        return True
    return [ a for a in actions if inall(a) ]

# Compute the successor state set w.r.t. a given action.

def Bsucc(bstate,action):
    result = set()
    for s in bstate:
        result.update(s.succs(action))
    return result

# Return the subset of states compatible with the observation.

def Bobserve(bstate,observation):
    return { s for s in bstate if s.compatible(observation) }

# Construct a branching plan for a problem instance with partial observability.

def POsolver(instance):
    ''' Your code here '''
    initialStates, goalStates, allActions = instance
    
    def solver(s, path, gS):

        for x in path:
            if x.issubset(s):
                return None
        if s.issubset(gS):
            return PlanEmpty()

        actions = Bapplicable(s)
#        random.shuffle(actions)
        
        for action in actions:
            branches = []
            f=True

            for o in action.observations():
                #successor states of an action
                succ = Bsucc(s, action)
                
                #successor states of an action w.r.t observation
                bsucc = Bobserve(succ, o)

                x = solver(bsucc, path+[s], gS)
                
                if x is None:
                    f=False
                    break
                else:
                    branches.append((o, x))
            if f:
                return PlanNode(action, branches)
        return None
        
        
        
    return solver(initialStates, [], goalStates)


