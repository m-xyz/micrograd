#! /usr/bin/env python
import subprocess
import os
from graph_visualizer import draw_dot

class Val:

    def __init__(self, data, _children=(), _op='', label=''):
        self.data = data
        self.prev = set(_children)
        self._op = _op
        self.label = label

    def __repr__(self):
        return f"Val(data={self.data})"

    def __add__(self, other):
        res = Val(self.data + other.data, (self, other), '+')
        return res

    def __mul__(self, other):
        res = Val(self.data * other.data, (self, other), '*')
        return res


a = Val(5,label='a')
b = Val(7,label='b')
c = a + b
c.label = 'c'
#d = Val(3,label='d')
z = Val(100, label='z')
x = Val(10, label='x')
d = z * x
d.label = 'd'
e = c * d
e.label = 'e'
f = Val(11, label='f')
L = e * f
L.label = 'L'
draw_dot(L)



