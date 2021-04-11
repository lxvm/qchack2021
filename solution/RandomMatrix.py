from typing import List, Tuple

import numpy as np
import cirq
import quantum_decomp

def swap_to(
    source: cirq.GridQubit,
    target:cirq.GridQubit,
    converter:cirq.google.optimizers.ConvertToSycamoreGates = None
) -> List[cirq.GridQubit]:

    loc = (source.row, source.col)
    dx = [0, -1, 0, 1]
    dy = [1, 0, -1, 0]
    ops = []
    while loc[0] != target.row or loc[1] != target.col:
        best = (100, -1, -1)
        for dir in range(4):
            r = loc[0]+dx[dir]
            c = loc[1]+dy[dir]
            status = (abs(r-target.row)+abs(c-target.col), r, c)
            best = min(best, status)
        a = cirq.GridQubit(loc[0], loc[1])
        b = cirq.GridQubit(best[1], best[2])
        ops.append(cirq.SWAP(a,b))
        loc = (best[1], best[2])

    if converter:
        ops = converter.convert(ops)

    return ops


def do_swap(
    a: cirq.GridQubit, b: cirq.GridQubit
) -> Tuple[List[cirq.GridQubit], cirq.GridQubit]:
    dx = [0, -1, 0, 1]
    dy = [1, 0, -1, 0]
    best = (100, -1, -1)
    for dir in range(4):
        r = b.row+dx[dir]
        c = b.col+dy[dir]
        status = (abs(r-a.row)+abs(c-a.col), r, c)
        best = min(best, status)

    source = a
    target = cirq.GridQubit(best[1], best[2])

    return swap_to(source, target), target


def random_matrix(
    target_qubits: List[cirq.GridQubit], matrix: np.ndarray
) -> Tuple[cirq.OP_TREE, List[cirq.GridQubit]]:

    circuit = quantum_decomp.matrix_to_cirq_circuit(matrix)
    old_qubits = [(str(x), x) for x in circuit.all_qubits()]
    old_qubits = sorted(old_qubits)
    old_qubits = [x[1] for x in old_qubits]
    mapping = dict(zip(old_qubits, target_qubits))
    
    print(mapping)

    decomp_ops = []
    #circuit = circuit
    ops = circuit.all_operations()

    for op in ops:
        if type(op) == cirq.ops.controlled_operation.ControlledOperation:
            gate = op

            controls = gate.controls
            target = gate.sub_operation.qubits
            matrix = cirq.unitary(gate.sub_operation.gate)

            decomposed_temp = cirq.optimizers.decompose_multi_controlled_rotation(matrix, list(controls), target[0])

            decomp_ops.extend([x.transform_qubits(mapping) for x in decomposed_temp])
        else:
            decomp_ops.append(op.transform_qubits(mapping))

    swapped_ops = []
    for op in decomp_ops:
        if len(op.qubits) == 2:
            q0 = op.qubits[0]
            q1 = op.qubits[1]

            oplist, target = do_swap(q0, q1)
            adjacentop = op.transform_qubits({q0: target, q1: q1})
            revlist = swap_to(target, q0)

            swapped_ops.extend(oplist)
            swapped_ops.append(adjacentop)
            swapped_ops.extend(revlist)
        else:
            swapped_ops.append(op)


    converter = cirq.google.optimizers.ConvertToSycamoreGates()
    #SycamoreGates = converter.convert(decomp_ops)
    SycamoreGates = converter.convert(swapped_ops)
    SycamoreGates = cirq.google.optimized_for_sycamore(cirq.Circuit(SycamoreGates))
    #SycamoreGates = cirq.google.optimized_for_sycamore(cirq.Circuit(decomp_ops), optimizer_type='sycamore')
    
    return SycamoreGates, []
