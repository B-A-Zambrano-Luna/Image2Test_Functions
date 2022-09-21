# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 15:56:52 2022

@author: LENOVO
"""

import numpy as np
import test_functions as test


class imate2test(object):
    def __init__(self, Image, Z_k, reduction=False):
        self.p = Z_k.get_prime()
        self.k = Z_k.get_radio()
        if not reduction:
            self.w, self.h = Image.shape
        else:
            k = Z_k.get_radio()
            p = Z_k.get_prime()
            self.w = p**(int(k/2))
            self.h = p**(k - int(k/2))
        self.test = []
        self.emmending = dict()
        self.leaves = [Image]
        self.image = Image
        self.Z_k = Z_k
        self.tree_temple = [np.ones((self.w, self.h))]

    def get_emmending(self):
        return self.emmending

    def get_image(self):
        return self.image

    def get_leaves(self):
        return self.leaves

    def fit(self):
        k = self.k
        p = self.p
        leaves = self.leaves
        tree_temple = self.tree_temple

        for level in range(1, k+1):
            # print("level", level)
            if level % 2 == 1:
                for leaf_index in range(p**(level-1)):
                    # print("leaf_index", leaf_index)
                    # print("leaves", leaves)
                    leaf = leaves.pop(0)
                    # print("leaf", leaf)
                    # print("split", np.array_split(leaf, p, axis=1))
                    leaves += np.array_split(leaf, p, axis=1)
                    # print("leaves after", leaves)
                    leaf_aux = tree_temple.pop(0)
                    tree_temple += \
                        np.array_split(leaf_aux, p, axis=1)
            elif level % 2 == 0:
                for leaf_index in range(p**(level-1)):
                    # print("leaf_index", leaf_index)
                    # print("leaves", leaves)
                    leaf = leaves.pop(0)
                    # print("leaf", leaf)
                    # print("split", np.array_split(leaf, p, axis=0))
                    leaves += np.array_split(leaf, p, axis=0)
                    # print("leaves after", leaves)
                    leaf_aux = tree_temple.pop(0)
                    tree_temple += \
                        np.array_split(leaf_aux, p, axis=0)
            Z_k = self.Z_k
            Zipleaves = zip(Z_k, leaves)
            self.emmending = dict(Zipleaves)

    def get_test(self):
        k = self.k
        p = self.p
        adds = []
        emmending = self.emmending
        for leaf in emmending:
            value_leaf = emmending[leaf].mean()
            adds.append(value_leaf *
                        test.char_function(leaf,
                                           -k, p))
        return test.test_function(adds)

    def get_values(self):
        adds = []
        emmending = self.emmending
        for leaf in emmending:
            # print("size", emmending[leaf].size)
            if emmending[leaf].size == 0:
                value_leaf = 0
            else:
                value_leaf = emmending[leaf].mean()
            # print("mean", value_leaf)
            adds.append(value_leaf)
        return np.array(adds)

    def inverse_transform(self, f):
        p = self.p
        k = self.k
        values = []
        try:
            if len(f) == p**k:
                values = f
        except:
            Z_k = self.Z_k
            for i in Z_k:
                values.append(f(i))
        # print("tample", self.tree_temple)
        copy_temple = self.tree_temple.copy()
        # print("copy_tample", copy_temple)
        level = k
        while level >= 1:
            # print("level", level)
            if level % 2 == 1:
                for node in range(p**(level-1)):
                    # print("node", node)
                    branch = []
                    for i in range(p):
                        # print("index", i)
                        leaf = copy_temple.pop(0)
                        # print("leaf", leaf)
                        if level == k:
                            leaf = values[i+node*p] * leaf
                        # print("leaf_values", leaf)
                        branch.append(leaf)
                    # print("concatenate", np.concatenate
                    #       (branch, axis=1))
                    copy_temple\
                        .append(np.concatenate
                                (branch, axis=1))
            elif level % 2 == 0:
                for node in range(p**(level-1)):
                    # print("node", node)
                    branch = []
                    for i in range(p):
                        # print("index", i)
                        leaf = copy_temple.pop(0)
                        # print("leaf", leaf)
                        if level == k:
                            leaf = values[i+node*p] * leaf
                        # print("leaf_values", leaf)
                        branch.append(leaf)
                    # print("concatenate", np.concatenate
                    #       (branch, axis=0))
                    copy_temple\
                        .append(np.concatenate
                                (branch, axis=0))
            # print("inverse", copy_temple)
            level = level - 1
        return copy_temple[0]
