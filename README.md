# Shakespearean AI: Generating Sonnets with Hidden Markov Models

In this project, I wanted to generate Shakespearean-style sonnets in python using Hidden Markov Models (HMM). HMMs are statistical models in which an outcome is dependent on previous series of events or occurences. To put it simply, they are an unsuperivsed machine learning model that aims to predict an outcome based on sequential data. Thus, they are widely used in scenarios that require some sort of pattern recognition, such as speech or text reconition. Using HMMs, I wanted to have some fun and see if I could train a model to produce contextually and linguistically relevant Shakespearean style text.

## Creating the Model
The training data we used in our model was a collection of 154 sonnets written by Shakespeare. A copy of the txt file can be found [here](https://github.com/yujinahn02/shakespeare/blob/main/sonnets.txt).

### Data Preprocessing
The first step I took was to make sure all the words in the training data were in lowercase. This was to ensure that the same word was not being recognized as two different words because one had a capital letter in it and the other one did not. **a = a.lower()**converts every character in the text to lowercase, ensuring that we have a consistent format across our dataset.

```
def Read( fname ):
    a = open( fname ).read()
    a = a.lower()
    return a
```
The **return a** function provides us back the newly, lower-cased text.

### Functions

I first created a function called **MakeDict()** to process a given string of text to identify patterns in letter sequences. Starting with an empty dictionary, it examines each letter or sequence, referred to as the 'key'. As it progresses through the text, the function checks the next letter, which we call the 'retral'. For each 'key', it keeps a tally of how often each 'retral' appears right after it. If a particular 'key-retral' pairing is encountered for the first time, it's added to the dictionary with a count of one. If the pairing has been seen before, the function simply updates its count. Once all pairings have been recorded, the function has an option to convert these tallies into probabilities. The end result is a comprehensive dictionary that captures the textual patterns of the input string.

```
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
    if retprobs:  # if you want to returb probabilities
        for i in K:
            vec = np.array( dct[i][1] )
            vec = vec/vec.sum()
            dct[i][1] = vec
    return dct
```
I also created another function called **BuildString()** which constructs a string using a dictionary derived from Shakespearean patterns. It begins by selecting a starting sequence randomly from our dictionary keys. As it progresses, it either appends the most probable next character based on previously observed patterns or improvises by adding a random character from the available alphabet if no match is found in the dictionary. 

```
def BuildString( dct, L, abet, WL ):
    # L is length of the output string
    # WL is word length in the dictionary
    # pick a starting string from the dictionary
    keys = list(dct.keys())
    stng = np.random.choice(keys)
    # build on this string
    for i in range( L ):
        preced = stng[-WL:] 
        if preced in dct:
            newlett = np.random.choice(dct[preced][0], p=dct[preced][1])
            stng += newlett
        else:
            r = int( np.random.ranf()*len(abet) )
            stng += abet[r]
    return stng
``` 
