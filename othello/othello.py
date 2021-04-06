import random
from othello import OthelloState
from agent_interface import AgentInterface


class Agent(AgentInterface):
    """
    
    An agent who plays the Othello game
    MY_COMMENTS___
        I implemented an sort of a hybrid where the agent first yields the best
        actions on the basis of their value on the weighted board. weighted board appreciates corners and edges of the map. If time allows, the agent iterates through alphabeta, and yields the best action possible given the depth constraints.
        
        Through a 10-game simulation against minimax with similar depth constraints (6) and time-limit of 2 seconds my agent has no timeouts and won 10 times out of 10.
        
        Through a 20-game simulation against minimax with similar depth constraints (6) and time-limit of 3 seconds my agent has no timeouts and won 15 times out of 20.

    Methods
    -------
    `info` returns the agent's information
    `decide` chooses an action from possible actions
    """
    
    def __init__(self, depth):
        """
        `depth` is the limit on the depth of Minimax tree
        """
        self.depth = depth

    @staticmethod
    def info():
        """
        Return the agent's information

        Returns
        -------
        Dict[str, str]
            `agent name` is the agent's name
            `student name` is the list team members' names
            `student number` is the list of student numbers of the team members
        """
        # -------- Task 1 -------------------------
        # Please complete the following information

        return {"agent name": "000",  # COMPLETE HERE
                "student name": ["max naumanen"],  # COMPLETE HERE
                "student number": ["526801"]}  # COMPLETE HERE

    def decide(self, state: OthelloState, actions: list):
        weighted_board = [
            [120, -20,  20,   5,   5,  20, -20, 120],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [ 20,  -5,  15,   3,   3,  15,  -5,  20],
            [  5,  -5,   3,   3,   3,   3,  -5,   5],
            [  5,  -5,   3,   3,   3,   3,  -5,   5],
            [ 20,  -5,  15,   3,   3,  15,  -5,  20],
            [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
            [120, -20,  20,   5,   5,  20, -20, 120]
        ]

        values = {}
        w_actions = {}
        for action in actions:
            w_actions[action] = weighted_board[action[0]][action[1]]
        f_actions = {k: v for k, v in sorted(w_actions.items(), key=lambda item: item[1], reverse=True)}
        best_yet = list(f_actions.keys())[0]
        v = f_actions[best_yet]
        yield best_yet
        for action in f_actions:
            values[action] = self.alphabeta(state.successor(action), weighted_board, self.depth-1, -10000, 10000, False) #+ weighted_value
            candidates = {k: v for k, v in sorted(values.items(), key=lambda item: item[1], reverse=True)}
            if candidates[action]>candidates[best_yet]:
                yield action
                best_yet=action
            
        max_value = max(values.values())
        candidates = [action for action in actions if (values[action] - max_value > -1)]
        yield random.choice(candidates)
        
        
        
    def alphabeta(self, state, wb, depth, alpha, beta, maxPlayer):
        actions = state.actions()
        if not actions:
            if (not state.previousMoved):
                if maxPlayer:
                    if (state.count(state.player)>state.count(state.otherPlayer)):
                        return 10000
                    if (state.count(state.player)<state.count(state.otherPlayer)):
                        return -10000
                    return state.count(state.player)
                else:
                    if (state.count(state.player)<state.count(state.otherPlayer)):
                        return 10000
                    if (state.count(state.player)>state.count(state.otherPlayer)):
                        return -10000
                    return state.count(3-state.player)
            else:
                if not (depth == 0):
                    if maxPlayer:
                        return self.alphabeta(OthelloState(state), wb, depth - 1, alpha, beta, False)
                    else:
                        return self.alphabeta(OthelloState(state), wb, depth - 1, alpha, beta, True)
        if depth == 0:
            if maxPlayer:
                return state.count(state.player)
            else:
                return state.count(3-state.player)
                
        if maxPlayer:
            best = float('-inf')
        else:
            best = float('inf')
            
            
        w_actions = {}
        for action in actions:
            w_actions[action] = wb[action[0]][action[1]]
        f_actions = {k: v for k, v in sorted(w_actions.items(), key=lambda item: item[1], reverse=True)}
            
        for action in f_actions:
            v = self.alphabeta(state.successor(action), wb, depth-1, alpha, beta, not maxPlayer)
            if not maxPlayer:
                best = min(best, v)
                beta = min(beta, best)
            else:
                best = max(best, v)
                alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best
#        if maxPlayer:
#            best = float('-inf')
#            for action in actions:
#                v = self.alphabeta(state.successor(action), depth-1, alpha, beta, False)
#                best = max(best, v)
#                alpha = max(alpha, best)
#                if alpha >= beta:
#                    break
##            print(f"{maxPlayer, eval, beta, alpha}")
##            return best
#        else:
#            best = float('inf')
#            for action in actions:
#                v = self.alphabeta(state.successor(action), depth-1, alpha, beta, True)
#                best = min(best, v)
#                beta = min(beta, best)
#                if alpha >= beta:
#                    break
#        return best
        
#        values = {}
#        for action in actions:
#            values[action] = self.min_value(state.successor(action), self.depth - 1)+2*weighted_board[action[0]][action[1]]
#        max_value = max(values.values())
#        candidates = [action for action in actions if (values[action] - max_value > -1)]
#        yield random.choice(candidates)
#
#
#    def max_value(self, state, depth):
#        actions = state.actions()
#        if not actions:
#            if (not state.previousMoved):
#                if (state.count(state.player)>state.count(state.otherPlayer)):
#                    return 10000
#                if (state.count(state.player)<state.count(state.otherPlayer)):
#                    return -10000
#                return state.count(state.player)
#            else:
#                if not (depth == 0):
#                    return self.min_value(OthelloState(state), depth - 1)
#        if depth == 0:
#            return state.count(state.player)
#        value = float('-inf')
#
#
#        for action in actions:
#            value = max(value, self.min_value(state.successor(action), depth - 1))
#        return value
#
#    def min_value(self, state, depth):
#        actions = state.actions()
#        if not actions:
#            if (not state.previousMoved):
#                if (state.count(state.player)<state.count(state.otherPlayer)):
#                    return 10000
#                if (state.count(state.player)>state.count(state.otherPlayer)):
#                    return -10000
#                return state.count(3 -state.player)
#            else:
#                if not (depth == 0):
#                    return self.max_value(OthelloState(state), depth - 1)
#        if depth == 0:
#            return state.count(3 - state.player)
#        value = float('inf')
#        for action in actions:
#            value = min(value, self.max_value(state.successor(action), depth - 1))
#        return value

