#!/usr/bin/python3

from predlogic import *

# We use the Ply package for generating a lexer and a parser

#################### Lexer

# All tokens used in the grammaer

tokens = ('AND',
          'OR',
          'NOT',
          'SOME',
          'EVERY',
          'A',
          'THE',
          'NO',
          'IS',
          'OF',
          'THAT',
          'ID',
          'ivID',
          'tvID',
          'adjID',
          'roleID',
          'DOT',
          'SINGLEQUOTE',
          'S',
          'EQUALS'
)

# Tokens

t_SINGLEQUOTE = r"'"
t_DOT = r'.'
t_EQUALS = r'=+'

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

# Process characters that are not handled by the lexer
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Mapping from reserved words to tokens

keywords = {'and' : 'AND',
            'or' : 'OR',
            'not' : 'NOT',
            'implies' : 'IMPLIES',
            'some' : 'SOME',
            'every' : 'EVERY',
            'a' : 'A',
            's' : 'S',
            'the' : 'THE',
            'no' : 'NO',
            'is' : 'IS',
            'of' : 'OF',
            'that' : 'THAT'
}

# Different categories of verbs, adjectives, and nouns that
# express binary relations.

transitiveVerbs = { 'sees', 'knows', 'likes', 'hears' }
intransitiveVerbs = { 'sleeps', 'walks', 'runs', 'snores' }
adjectives = { 'small', 'young', 'happy', 'sad' }
binaryrelations = { 'mother', 'father', 'parent', 'sibling', 'sister', 'brother', 'cousin', 'grandparent', 'grandmother', 'grandfather', 'uncle', 'aunt', 'niece', 'nephew' }

# Recognize an alphanumeric ID, and if it is one of the words
# with a fixed meaning, then map it to the corresponding token
# like tvID, ivID, adjID or roleID. The rest are treated as
# names (constant symbols) or common nouns (unary predicates).

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.lower() in keywords:
        t.type = keywords[t.value.lower()]
    elif t.value.lower() in transitiveVerbs:
        t.type = 'tvID'
    elif t.value.lower() in intransitiveVerbs:
        t.type = 'ivID'
    elif t.value.lower() in adjectives:
        t.type = 'adjID'
    elif t.value.lower() in binaryrelations:
        t.type = 'roleID'
    return t
    
# Build the lexer with the Ply package

import ply.lex as lex
lexer = lex.lex()

sentences = []

####### Generation of new vars to be used in quantifications et cetera

varcnt = 0
varnames0 = ["x","y","z","u","v","w"]
varnames = varnames0 + [ v + str(i) for v in varnames0 for i in range(100) ]

def newX():
    global varcnt
    varcnt = varcnt+1
    return varnames[varcnt-1]

####### The grammar rules for a fragment of English

# Parsing rules

# Top-level definitions

def p_spec(t):
    '''spec : sentence0
            | sentence0 spec'''
    t[0] = 0

def p_sentence_separator(t):
    'sentence0 : EQUALS'
    global sentences
    t[0] = 0
    sentences = sentences + [0]

def p_sentence_top(t):
    'sentence0 : sentence DOT'
    global sentences
    global varcnt
    varcnt = 0
    t[0] = 0
    sentences = sentences + [t[1]]

def p_sentence(t):
    'sentence : NP VP'
    t[0] = (t[1])(t[2])

###
### IMPLEMENT THIS GRAMMAR RULE AND ITS SEMANTICS
###    
def p_sentence_or(t):
    'sentence : sentence OR sentence'
    t[0] = OR(t[1], t[3])

def p_NP_ID(t):
    'NP	: ID '
    IDstr = t[1] # Using t[1] below fails: ply does not bind t correctly!
    t[0] = (lambda P : P (Const(IDstr)))

def p_NP_DET_CN(t):
    'NP : DET CN'
    t[0] = (t[1])(t[2])

def p_NP_DET_RCN(t):
    'NP : DET RCN'
    t[0] = (t[1])(t[2])

def p_NP_DET_roleCNof(t):
    'NP : DET roleCNof'
    t[0] = (t[1])(t[2])

def p_DET_some(t):
    'DET : SOME'
    x = newX()
    t[0] = (lambda P : lambda Q : EXISTS(x,AND(P (Var(x)),Q (Var(x)))))

def p_DET_a(t):
    'DET : A'
    x = newX()
    t[0] = (lambda P : lambda Q : EXISTS(x,AND(P (Var(x)),Q (Var(x)))))

def p_DET_the(t): # Exactly the same as A
    'DET : THE'
    x = newX()
    t[0] = (lambda P : lambda Q : EXISTS(x,AND(P (Var(x)),Q (Var(x)))))

def p_DET_every(t):
    'DET : EVERY'
    x = newX()
    t[0] = (lambda P : lambda Q : FORALL(x,IMPL(P (Var(x)),Q (Var(x)))))

def p_DET_no(t):
    'DET : NO'
    x = newX()
    t[0] = (lambda P : lambda Q : FORALL(x,IMPL(P (Var(x)),NOT(Q (Var(x))))))

def p_roleCNofWITHs(t):
    'NP : ID SINGLEQUOTE S roleID'
    IDstr = t[1]
    roleIDstr = t[4]
    x = newX()
    t[0] = lambda Q : EXISTS(x,AND(ATOM(roleIDstr,[Var(x),Const(IDstr)]),Q (Var(x))))

###
### IMPLEMENT THIS GRAMMAR RULE AND ITS SEMANTICS
###    
def p_VP_and(t):
    'VP : VP AND VP'

    VPf = t[1]
    VPf2 = t[3]
    
    t[0] = (lambda x : AND(VPf(x), VPf2(x)))

def p_VP_ivID(t):
    'VP : ivID'
    ivIDstr = t[1]
    t[0] = (lambda x : ATOM(ivIDstr,[x]))

def p_VP_issame(t):
    'VP : IS NP'
    NPf = t[2]
    t[0] = (lambda x : NPf (lambda y : EQUAL(x,y)))

def p_VP_isnotsame(t):
    'VP : IS NOT NP'
    NPf = t[3]
    t[0] = (lambda x : NOT(NPf (lambda y : EQUAL(x,y))))

def p_VP_isADJ(t):
    'VP : IS adjID'
    adjIDstr = t[2]
    t[0] = lambda x : ATOM(adjIDstr,[x])

def p_VP_isADJnot(t):
    'VP : IS NOT adjID'
    adjIDstr = t[3]
    t[0] = lambda x : NOT(ATOM(adjIDstr,[x]))

def p_VP_TV_NP(t):
    'VP : TV NP'
    TVf = t[1]
    NPf = t[2]
    t[0] = (lambda x : NPf (lambda y : (TVf(y))(x)))

def p_TV_tvID(t):
    'TV : tvID'
    tvIDstr = t[1]
    t[0] = (lambda x : lambda y : ATOM(tvIDstr,[y,x]))

def p_RCN_CN_that_VP(t):
    'RCN : CN THAT VP'
    CNf = t[1]
    VPf = t[3]
    t[0] = (lambda x : AND(CNf(x),VPf(x)))

def p_RCN_CN_that_NP_TV(t):
    'RCN : CN THAT NP TV'
    CNf = t[1]
    NPf = t[3]
    TVf = t[4]
    t[0] = (lambda x : AND(CNf(x),NPf (lambda y : (TVf(y))(x))))

def p_roleCNof(t):
    'roleCNof : roleID OF NP'
    roleIDstr = t[1]
    NPf = t[3]
    t[0] = (lambda x : NPf (lambda y : ATOM(roleIDstr,[x,y])))

def p_CN_ID(t):
    'CN : ID'
    IDstr = t[1]
    t[0] = (lambda x : ATOM(IDstr,[x]))

###
### IMPLEMENT THIS GRAMMAR RULE AND ITS SEMANTICS
###    
def p_CN_ADJ_CN(t):
    'CN : adjID CN'
    print("T1: ", t[1])
    print("T2: ", t[2])
    adjID = t[1]
    CNf = t[2]
    t[0] = (lambda x: AND(ATOM(adjID,[x]), CNf(x)))

# Error rule

def p_error(t):
    print("Syntax error at '%s'" % t.value)
    print("On line " + str(t.lexer.lineno))

# Build the parser with the Ply package

import ply.yacc as yacc
parser = yacc.yacc()

# Read the whole input file, and parse it

def parsestring(s):
  global sentences
  sentences = []
  dummy = parser.parse(s)
  return sentences

def parseinputfile(filename):
    with open(filename, 'r') as f:
        allinput = f.read()
        result = parser.parse(allinput)
    global sentences
    if len(sentences) < 1:
        print("Must give one sentence.")
        exit(1)
    print("Parsed " + str(len(sentences)) + " sentences:")
    for i in range(len(sentences)):
        if sentences[i] == 0:
            return sentences[:i],[ s for s in sentences[i:] if s != 0 ]
    return sentences,[]

# Definitions of important concepts

u = Var("u")
x = Var("x")
y = Var("y")
z = Var("z")

# Functions to express atomic formulas more compactly
female = lambda x : ATOM("female",[x])
male = lambda x : ATOM("male",[x])
mother = lambda x,y : ATOM("mother",[x,y])
father = lambda x,y : ATOM("father",[x,y])
sister = lambda x,y : ATOM("sister",[x,y])
brother = lambda x,y : ATOM("brother",[x,y])
parent = lambda x,y : ATOM("parent",[x,y])
aunt = lambda x,y : ATOM("aunt",[x,y])
uncle = lambda x,y : ATOM("uncle",[x,y])
nephew = lambda x,y : ATOM("nephew",[x,y])
grandparent = lambda x,y : ATOM("grandparent",[x,y])
grandmother = lambda x,y : ATOM("grandmother",[x,y])
sibling = lambda x,y : ATOM("sibling",[x,y])
cousin = lambda x,y : ATOM("cousin",[x,y])

# Long ands expressed as a list

def chainAND(l):
  if l == []:
    return TRUE()
  elif len(l) == 1:
    return l[0]
  else:
    return AND(l[0],chainAND(l[1:]))

# Definitions of family relationships

# Mother, father, sister, brother, aunt, uncle, nephew, sibling, cousin
# in terms of parent, female, male

A1 = FORALL("x",FORALL("y",EQVI(mother(x,y),AND(female(x),parent(x,y)))))
A2 = FORALL("x",FORALL("y",EQVI(father(x,y),AND(male(x),parent(x,y)))))
A3 = FORALL("x",FORALL("y",EQVI(sister(x,y),AND(female(x),sibling(x,y)))))
A4 = FORALL("x",FORALL("y",EQVI(brother(x,y),AND(male(x),sibling(x,y)))))
A5 = FORALL("x",FORALL("y",EQVI(aunt(x,y),
                                AND(female(x),
                                    EXISTS("z",AND(sibling(x,z),
                                                   parent(z,y)))))))
A6 = FORALL("x",FORALL("y",EQVI(uncle(x,y),
                                AND(male(x),
                                    EXISTS("z",AND(sibling(x,z),
                                                   parent(z,y)))))))
A7 = FORALL("x",FORALL("y",EQVI(nephew(x,y),
                                AND(male(x),
                                    EXISTS("z",AND(sibling(y,z),
                                                   parent(z,x)))))))
A8 = FORALL("x",FORALL("y",EQVI(grandmother(x,y),
                                AND(female(x),
                                    grandparent(x,y)))))
A9 = FORALL("x",FORALL("y",EQVI(grandparent(x,y),
                                EXISTS("z",AND(parent(x,z),
                                               parent(z,y))))))
A10 = FORALL("x",FORALL("y",EQVI(sibling(x,y),
                                 EXISTS("z",chainAND([NOT(EQUAL(x,y)),
                                                      parent(z,x),
                                                      parent(z,y)])))))
A11 = FORALL("x",FORALL("y",EQVI(cousin(x,y),
                                 EXISTS("z",EXISTS("u",chainAND([parent(z,x),
                                                                 parent(u,y),
                                                                 sibling(z,u)]))))))

# Female and male mutually exclusive

A12 = FORALL("x",NOT(AND(female(x),male(x))))

#A420 = FORALL("x",FORALL("y", NOT(EQUAL(x, y))))

# Sibling relation is symmetric

A13 = FORALL("x",FORALL("y",EQVI(sibling(x,y),
                                 sibling(y,x))))

# Assumption: siblings have exactly the same parents

A14 = FORALL("x",FORALL("y",FORALL("z",IMPL(sibling(x,y),
                                            EQVI(parent(z,x),
                                                 parent(z,y))))))

# Only one mother and one father

A15 = FORALL("x",FORALL("y",FORALL("z",IMPL(AND(mother(x,y),mother(z,y)),
                                            EQUAL(x,z)))))
A16 = FORALL("x",FORALL("y",FORALL("z",IMPL(AND(father(x,y),father(z,y)),
                                            EQUAL(x,z)))))

familyrelations = [A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A14,A13,A15,A16]

# Show formulas and generate TPTP output

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        inputfilename = 'TEXT'
    else:
        inputfilename = sys.argv[1]
    if len(sys.argv) < 3:
        outputfilename = 'OUTPUT.TPTP'
    else:
        outputfilename = sys.argv[2]
    premises,conclusions = parseinputfile(inputfilename)
    for f in premises:
        print(str(f))
    print("===========================================")
    for f in conclusions:
        print(str(f))
    print("")
    tptpfile = open(outputfilename,"w")
    i = 0
    # Output everything, including the family relations to the TPTP file
    for f in familyrelations + premises:
        i = i+1
        tptpfile.write("fof(formula" + str(i) + ",axiom, (" + f.TPTP() + ")).\n")
    for f in conclusions:
        i = i+1
        tptpfile.write("fof(formula" + str(i) + ",conjecture, (" + f.TPTP() + ")).\n")
    tptpfile.close()
