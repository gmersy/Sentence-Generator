#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 17:46:43 2019

@author: gabemersy
"""
class Random:
    def __init__(self, seed):
        self.num = seed
        # Setting variables for efficiency
        self.c1 = 16807
        self.c2 = 2147483648
    
    # Computed according to Parker-Miller Algorithm
    def next(self):
        self.num = (self.c1*self.num)%(self.c2 - 1)
        return self.num
    
    # Generate the next random number in the sequence and scale it using mod to be strictly less than the limit
    def choose(self, limit):
        rand = self.next()
        new = rand % limit
        return new
    
class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.count = 1
    
    def __repr__(self):
        finStr = ''
        finStr += str(self.count) 
        finStr += ' '
        finStr += self.left
        finStr += ' ->'
        for i in range(len(self.right)):
            finStr += ' ' 
            finStr += self.right[i]
        return finStr

class Grammar:
    def __init__(self, seed):
        self.n = Random(seed) 
        self.rules = {}
        
    def rule(self, left, right):
        # If the left side is in the keys of the dictionary, then append the rule to the end of the tuple 
        if left in self.rules.keys():
            self.rules[left] += (Rule(left, right),)
        # Otherwise, set the value at the key of left to the rule itself
        else:
            self.rules[left] = (Rule(left, right),)
        
    def generate(self):
        # If the start key is in rules, call generating
        if 'Start' in self.rules:
            return self.generating(('Start',))
        # Otherwise, raise an exception
        else:
            raise Exception('There is no Start')
    
    def generating(self, strings):
        result = ''
        for s in strings:
            # If the given string is in the rules, then call the methods that select the string, then add that to the result
            if s in self.rules:
                tStr = self.select(s)
                finStr = self.generating(tStr)
                result += finStr
            # If the given string is not in the rules, then add the string followed by a space
            else:
                result += s + ' '      
        return result
    
    def select(self, left):
        rules = self.rules[left]
        total = 0
        # Compute the total by summing up the counts
        for r in rules:
            total += r.count
        # Choose a random index according to the randomization algorithm
        index = self.n.choose(total)
        # Subtract the count for each rule from the index variable and once the index is less than 0, choose a rule and break the loop
        for r in rules:
            index -= r.count
            if index <= 0:
                chosen = r
                break 
        # If each rule is not the chosen, then incresae its count to increase the probability of its selection 
        for r in rules:
            if r != chosen:
                r.count += 1
        return chosen.right
            
# Test
G = Grammar(101) 
G.rule('Noun',   ('cat',))                                #  01 
G.rule('Noun',   ('boy',))                                #  02 
G.rule('Noun',   ('dog',))                                #  03 
G.rule('Noun',   ('girl',))                               #  04 
G.rule('Verb',   ('bit',))                                #  05 
G.rule('Verb',   ('chased',))                             #  06 
G.rule('Verb',   ('kissed',))                             #  07 
G.rule('Phrase', ('the', 'Noun', 'Verb', 'the', 'Noun'))  #  08 
G.rule('Story',  ('Phrase',))                             #  09 
G.rule('Story',  ('Phrase', 'and', 'Story'))              #  10 
G.rule('Story',  ('Phrase', 'but', 'Story'))              #  11 
G.rule('Start',  ('Story', '.'))                          #  12

# Printing the 5 strings
for i in range(5):
    print(G.generate())                    