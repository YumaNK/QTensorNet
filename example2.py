import jax.numpy as np
import numpy as onp
from qtensornetwork.circuit import Circuit
from qtensornetwork.components import Gate, Measurement
from qtensornetwork.util import data_to_qubits
from qtensornetwork.gate import *
from sklearn.datasets import load_iris
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

onp.random.seed(0)

def generate_iris_binary_dataset():
    iris_dataset = load_iris()
    xtrain, xtest, ytrain, ytest = train_test_split(iris_dataset['data'], iris_dataset['target'], random_state=0)
    mm = preprocessing.MinMaxScaler()
    xtrain = mm.fit_transform(xtrain)
    xtest = mm.fit_transform(xtest)

    xtr, ytr, xte, yte = [], [], [], []

    for i in range(len(xtrain)):
        if ytrain[i] == 0:
            xtr.append(xtrain[i])
            ytr.append([1, 0])
        if ytrain[i] == 1:
            xtr.append(xtrain[i])
            ytr.append([0, 1])

    for i in range(len(xtest)):
        if ytest[i] == 0:
            xte.append(xtest[i])
            yte.append([1, 0])
        if ytest[i] == 1:
            xte.append(xtest[i])
            yte.append([0, 1])

    xtrain = np.array(xtr)
    xtest = np.array(xte)
    ytrain = np.array(ytr)
    ytest = np.array(yte)

    return xtrain, ytrain, xtest, ytest

xtrain, ytrain, xtest, ytest = generate_iris_binary_dataset()

circuit = Circuit(4)

RYgate = RY(0,0)
for q in range(4):
    circuit.add_gate(Gate([q], params=None, func=RYgate.func, train_idx=[q]))

n = 3

def circuit1():
    gates = []
    gates.append(RX(0,onp.random.randn()))
    gates.append(RX(1,onp.random.randn()))
    gates.append(RX(2,onp.random.randn()))
    gates.append(RX(3,onp.random.randn()))
    gates.append(RZ(0,onp.random.randn()))
    gates.append(RZ(1,onp.random.randn()))
    gates.append(RZ(2,onp.random.randn()))
    gates.append(RZ(3,onp.random.randn()))
    gates.append(CNOT([3,2]))
    gates.append(CNOT([2,1]))
    gates.append(CNOT([1,0]))
    gate = combine_gates(gates)
    return gate

for i in range(n):
    gate = circuit1()
    gate.is_updated = True
    circuit.add_gate(gate)

m = np.array([[1, 0],[0,0]])
measurement = Measurement([0], m)
circuit.add_measurement(measurement)

circuit.show_circuit_structure()

circuit.classify(None, xtrain, ytrain, None, xtest, ytest, optimizer="adam", epoch=10)