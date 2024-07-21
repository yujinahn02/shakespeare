#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#shakespeare.py
def Read(fname):
    a = open(fname, encoding = "IISO-8859-1").read()
    a = a.lower()
    return a


# In[ ]:


def MakeDict( instr, WL=1, retprobs=True ):
    # N is the word length
    L = len( instr )
    dct = {}
    for i in range( L-WL ):
        keyl = instr[i:i+WL]
        retral = instr[i+WL]
        if keyl in dct:
            if retral in dct[keyl][0]:
                ndx = dct[keyl][0].index( retral )
                dct[keyl][1][ndx] +=1
            else:
                dct[keyl][0].append( retral )
                dct[keyl][1].append( 1 )
        else:
            dct[keyl] = [[retral],[1]]
    K = list(dct.keys())
    if retprobs:
        for i in K:
            vec = np.array( dct[i][1] )
            vec = vec/vec.sum()
            dct[i][1] = vec
    return dct


# In[ ]:


def BuildString(dct, L, abet, WL):
    keys = list(dct.keys())
    stng = np.random.choice(keys)
    for i in range (L):
        preced = stng[-WL:]
        if preced in dct:
            newlett = np.random.choice(dct[preced][0], p = dct[preced][1])
            stng += newlett
        else:
            r = int(np.random.rang() * len(abet))
            stng += abet[r]
    return stng


# In[ ]:


import shakespeare
#Examining the output of the MakeDict function
sonnets = shakespeare.Read('sonnets.txt')
dct = shakespeare.MakeDict(sonnets)
print(dct['z'])


# In[ ]:


# testing out different word lengths
WL = 2
dct = shakespeare.MakeDict(sonnets, WL)
output = shakespeare.BuildString(dct, 700, 'abc', WL)
print(output)

WL = 5
dct = shakespeare.MakeDict(sonnets, WL)
output = shakespeare.BuildString(dct, 700, 'abcdefgh', WL)
print(output)

WL = 15
dct = shakespeare.MakeDict(sonnets, WL)
output = shakespeare.BuildString(dct, 700, 'abcdefghijklmnopqrs', WL)
print(output)

