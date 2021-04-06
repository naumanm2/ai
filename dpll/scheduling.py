from logic import AND, OR, NOT, ATOM, IMPL, EQVI


# Encoding a scheduling problem into a SAT problem.
#------------------------------------------------------------------------------
#
# In this file, we encode a scheduling problem into a SAT problem. The first
# part of the file provides some helper functions to make the encoding easier.
#
# TASK 1
# ======
# There are two functions that you need to implement:
# `at_most_one`: in this function, you are given a list of formulas, and you
#                need to create a new formula that expresses at least one
#                formula in the list must be true.
# `exactly_one`: in this function, you are given a list of formulas, and you
#                need to create a new formula that expresses exactly one formula
#                in the list must be true.
#
#
#
# In the second part of the file, we encode the scheduling problem into a SAT
# problem:
#
# TASK 2
# ======
# In this task, you will implement the `problem2fma` function to translate a
# scheduling problem into a SAT problem. In other words, you should implement
# the constraints you have learned from the lecture to describe a scheduling
# problem as a SAT problem.
#
# Good luck :)


def all_pairs(lst):
    """
    Helper function, giving all pairs of a list of formulas.

    Parameter
    --------
    lst : list of formulas

    Returns
    -------
    generator of pairs
       Each unique pairing of the formulas in `lst`.
    """
    return ((lst[i], lst[j]) for i in range(0, len(lst)) \
            for j in range(i + 1, len(lst)))


def at_least_one(fmas):
    """
    Expresses that at least one formula in a list must be true.

    Parameters
    ----------
    fmas : list of formulas (len > 1)
       Of this list, at least one expression must evaluate to true.

    Returns
    -------
    Formula
    """
    # At least one true is easy. Disjuction.
    return OR(fmas)


def at_most_one(fmas):
    """
    Expresses that at most one formula in a list must be true.

    Parameters
    ----------
    fmas : list of formulas (len > 1)
       Of this list, at least at most one must be true.

    Returns
    -------
    Formula
    """
    # Hint: You can use the function 'allpairs' above to get the pairing
    #       of formulas.
    

    return AND([NOT(AND([x,y])) for (x,y) in all_pairs(fmas)])

def exactly_one(fmas):
    """
    Expresses that exactly one formula in a list must be true.

    Parameters
    ----------
    fmas : list of formulas (expressed as And, Or, Not, or using a Bool Atom).
       Of this list, at least one expression must evaluate to true.

    Returns
    -------
    Formula
    """
    return AND([at_least_one(fmas), at_most_one(fmas)])


def variable(task, time_slot):
    """
    Creates an atom expressing that `task` should be preformed at `time_slot`

    This is just a wrapper to create a Bool variable (atom) with a string
    representing the particular `task` and `time_slot`

    Parameters
    ----------
    task: str
        Task name
    time_slot: int
        The time slot

    Returns
    -------
    ATOM
        Boolean variable (atom) to be used in formulas. If this variable is
        assigned by the value True, it means the task: `task` should be
        performed at: `time_slot`
    """
    return ATOM("{}@{}".format(task, time_slot))


def problem2fma(tasks, orders, resource_need, time_horizon):
    """
    Encodes a scheduling problem to a SAT problem

    Parameters
    ----------
    tasks: List[str]
        A list of strings representing the tasks to be scheduled
    orders: List[(str, str)]
        A list of pairs `(task_1,task_2)`, meaning that `task_1` must
        precede `task_2`
    resource_need: Dict[str, str]
        A dictionary. `resource_need[task] = resource` means that `task`
        needs the `resource`
    time_horizon: int
        An integer which defines the time horizon (the maximum time point)

    Returns
    -------
        The encoded logical formula
    """

    # Tasks must take place exactly once
    
    print(exactly_one([variable(tasks[0], time) for time in range(1, time_horizon+1)]))
    C1 = AND([exactly_one([variable(task, time) for time in range(1, time_horizon+1)]) for task in tasks])
    
    C2 = AND([OR([NOT(variable(x, t)), NOT(variable(y, t))]) for (x, y) in all_pairs(tasks) if resource_need[x] == resource_need[y] for t in range(1, time_horizon+1)])
    
    C3 = AND([OR([NOT(variable(i, x)), NOT(variable(j, y))]) for (i, j) in orders for x in range(1, time_horizon+1) for y in range(1, x+1)])
    


    return AND([C1, C2, C3])



