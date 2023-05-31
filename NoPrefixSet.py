#!/bin/python3

# Solving the problem: https://www.hackerrank.com/challenges/one-week-preparation-kit-no-prefix-set/problem

import math
import os
import random
import re
import sys

#
# Complete the 'noPrefix' function below.
#
# The function accepts STRING_ARRAY words as parameter.
#

def checkIsPrefix(a, b):
    # if (len(a) > len(b)):
    #     return a[:len(b)] == b
    # elif (len(a) == len(b)):
    #     return a == b
    # else:
    #     return b[:len(a)] == a
    if len(b) >= len(a):
        return b[:len(a)] == a
    return False

def noPrefix(words):
    for i in range(0, len(words)):
        for j in range(0, len(words)):
            if i != j:
                if checkIsPrefix(words[i], words[j]):
                    print("BAD SET")
                    if (len(words[i]) <= len(words[j])):
                        print(words[j])
                    else:
                        print(words[i])
                    return
    print("GOOD SET")        
    
def prefixFilter(filter_word, word):
    if len(filter_word) <= len(word):
        if re.search("^" + filter_word, word) is not None:
            return True
    return False
    
def noPrefixFilter(words):
    if len(words) < 2:
        return
        print("GOOD SET")
    for i in range(0, len(words)):
        if (i == 0):
            other_words = words[1:]
        elif (i == len(words)):
            other_words = words[:len(words) - 1]
        else:
            other_words = words[:i] + words[i+1:]
        remaining = list(filter(lambda s: prefixFilter(words[i], s), other_words))
        if len(remaining) > 0:
            print("BAD SET")
            print(remaining[0])
            return
    print("GOOD SET")

class Node:
    def __init__(self, val):
        # Val is the character this node represents
        self.val = val
        # has_leaf indicates whether another string has terminated here
        self.has_leaf = False
        # whether this is part of a path to another word
        self.on_path = False
        # Children are non-leaf child nodes, ordered alphabetically
        self.children = [None] * 10
    
    def checkChildren(self, c):
        num = ord(c) - 97
        if self.children[num] is None:
            return -1
        else:
            return num
        
    def addChild(self, s):
        leaf_present = self.has_leaf
        if not leaf_present:
            if len(s) > 0:
                self.on_path = True
                i = self.checkChildren(s[0])
                if i > -1:
                    return self.children[i].addChild(s[1:])
                else:
                    self.children[ord(s[0]) - 97] = Node(s[0])
                    return self.children[ord(s[0]) - 97].addChild(s[1:])
            else:
                if (self.on_path):
                    return True
                self.has_leaf = True
                return False
        else:
            return True
    
    # When adding children the first time we can miss prefixes if the prefix is added after
    # the longer string it is a prefix for. However we will have caught cases where
    # prefixes have the same length, so no need to check all the way
    def checkPrefixTree(self, s):
        leaf_present = self.has_leaf
        if not leaf_present:
            if len(s) > 1:
                return self.children[ord(s[0]) - 97].checkPrefixTree(s[1:])
            else:
                return False
        else:
            return True  

def wordLen(w):
    return len(w)
            
def prefixTree(words):
    # words.sort(key=wordLen)
    root = Node("")
    for i in range(0, len(words)):
        prefix_detected = root.addChild(words[i])
        if (prefix_detected):
            print("BAD SET")
            print(words[i])
            return
    for i in range(0, len(words)):
        prefix_detected = root.checkPrefixTree(words[i])
        if (prefix_detected):
            print("BAD SET")
            print(words[i])
            return
    print("GOOD SET")

import heapq

def prefixHeap(words):
    heapq.heapify(words)
    if len(words) < 2:
        return True
    prev = heapq.heappop(words)
    while len(words) > 1:
        print(prev)
        current = heapq.heappop(words)
        print(current)
        if prefixFilter(prev, current):
            print("BAD SET")
            print(current)
            return
        if prefixFilter(current, prev):
            print("BAD SET")
            print(prev)
            return
        prev = current
    print("GOOD SET")
            
    
    
if __name__ == '__main__':
    n = int(input().strip())

    words = []

    for _ in range(n):
        words_item = input()
        words.append(words_item)

    prefixTree(words)
