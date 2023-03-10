#! /usr/bin/env python
import subprocess
import os
import math
from graph_visualizer import draw_dot

class Val:

    def __init__(self, data, _children=(), _op='', label=''):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None
        self.prev = set(_children)
        self._op = _op
        self.label = label

    def valObjWrapper(self, z):
        z = z if isinstance(z, Val) else Val(z)
        return z

    def __repr__(self):
        return f"Val(data={self.data},grad={self.grad})"

    def __add__(self, other):
        other = self.valObjWrapper(other)
        res = Val(self.data + other.data, (self, other), '+')

        def _backward():
            #NOTE: Acumulate gradients to avoid override bug(doing the same on other ops)
            #Given f(x,y) = x + y, df/dx is just 1, the same is true with df/dy,
            #with this observation the sum op can be thought of as some kind of "floodfill" to leaf nodes.
            self.grad += 1.0 * res.grad
            other.grad += 1.0 * res.grad
        res._backward = _backward

        return res

    def __mul__(self, other):
        other = self.valObjWrapper(other)
        res = Val(self.data * other.data, (self, other), '*')

        def _backward():
            self.grad += other.data * res.grad
            other.grad += self.data * res.grad
        res._backward = _backward

        return res

    def tanh(self):
        x = self.data
        t = (math.exp(2*x) - 1)/(math.exp(2*x) + 1)
        res = Val(t, (self, ), 'tanh')

        def _backward():
            # tanh derivative
            self.grad += (1 - t ** 2) * res.grad
        res._backward = _backward

        return res

    def backpropagation(self):
        topo = []
        visited = set()

        def build_topological(node):
            if node not in visited:
                visited.add(node)

                for child in node.prev:
                    build_topological(child)

                topo.append(node)

        build_topological(self)

        self.grad = 1.0
        for i in reversed(topo):
            i._backward()
        print(topo)

x1 = Val(2.0, label='x1')
x2 = Val(0.0, label='x2')

w1 = Val(-3.0, label='w1')
w2 = Val(1.0, label='w2')

b = Val(6.8813735870195432, label='bias')

x1w1 = x1 * w1; x1w1.label = 'x1 * w1'
x2w2 = x2 * w2; x2w2.label = 'x2 * w2'

x1w1x2w2 = x1w1 + x2w2; x1w1x2w2.label = 'x1 * w1 + x2 * w2'
n = x1w1x2w2 + b; n.label = 'n'
o = n.tanh(); o.label = 'o'
o.backpropagation()
draw_dot(o)



