import math
import random
from graphviz import Digraph

#wrapper class that acts as a reversed linked list with added functionality for backpropagation 
class Value:
    def __init__(self, data, _children=(), _op='', label=''): #last operand in expression is op
        self.data=data
        self._prev=set(_children)
        self._op = _op
        self._backward = lambda: None
        self.label=label
        self.grad=0.0
    def __repr__(self):
        return f"Value(data={self.data} grad={self.grad})"

    # these __operation__ methods give Value objects the capacity to be operated together and to 
    # be operated on by integer and float literals
    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        def _backward():
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad      
        out._backward = _backward
        return out 
    def __sub__(self, other):
        out = self + (-other)
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out
    def __rmul__(self, other):
        return self*other
    def __truediv__(self, other):
        return self*(other**-1)
    def __rtruediv__(self, other):
        return other * self**-1
    def __radd__(self, other):
        return self+other

    # activation function - normalizes the output to fit non-linearly between -1 and 1
    def tanh(self):
        n= self.data
        t= (math.exp(2*n)-1)/(math.exp(2*n)+1)
        out = Value(t, (self, ), 'tanh')
        def _backward():
            self.grad += (1-t**2)*out.grad
        out._backward = _backward
        return out
    
    def __pow__(self, other):
        assert isinstance(other, (int, float))
        out = Value(self.data**other, (self,), f'**{other}')
        def _backward():
            self.grad += other*(self.data**(other-1)) * out.grad
        out._backward = _backward
        return out
            
    def exp(self):
        x = self.data
        out = Value(math.exp(x), (self, ), 'exp')
        def _backward():
            self.grad = out.data * out.grad
        out._backward = _backward
        return out
    
    def backward(self): 
      #topological sort implementation -> turns graph into a an array of nodes 
      #where each appears before all the nodes it points to
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        self.grad=1.0
        for node in reversed(topo):
            node._backward()


# graph visualizer
def trace(root):
    nodes, edges = set(), set()
    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in v._prev:
                edges.add((child, v))
                build(child)
    build(root)
    return nodes, edges

def draw_dot(root):
    dot = Digraph(format='svg', graph_attr={'rankdir': 'LR'}) # left to right
    
    nodes, edges = trace(root)
    for n in nodes:
        uid = str(id(n))
        dot.node(name=uid, label="{ %s | data %.4f | grad %.4f }" % (n.label, n.data, n.grad), shape='record')
        if n._op:
            dot.node(name=uid + n._op, label=n._op)
            dot.edge(uid + n._op, uid)
    for n1, n2 in edges:
        dot.edge(str(id(n1)), str(id(n2)) + n2._op)
    return dot

# builds 3 layers of abstraction for the neural network,
# Neurons hold Value types, multiple Neurons form a Layer,
# an interlinked set of layers forms a Multi-Layer Perceptron,
# which is suited for distinguishing data that don't follow
# a linear pattern

class Neuron:
    def __init__(self, nin):
        self.w = [Value(random.uniform(-1,1)) for _ in range(nin)]
        self.b = Value(random.uniform(-1,1))
    def __call__(self, x):
        act = sum((wi*xi for wi, xi in zip(self.w, x)), self.b)
        out = act.tanh()
        return out
    def parameters(self):
        return self.w + [self.b]
class Layer:
    def __init__(self, nin, nout):
        self.neurons = [Neuron(nin) for _ in range(nout)]
    def __call__(self, x):
        outs = [n(x) for n in self.neurons]
        return outs[0] if len(outs) == 1 else outs
    def parameters(self):
        return [p for neuron in self.neurons for p in neuron.parameters()]

class MLP:
    def __init__(self, nin, nouts):
        sz = [nin] + nouts
        self.layers=[Layer(sz[i], sz[i+1]) for i in range(len(nouts))]    
    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]