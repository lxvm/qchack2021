from typing import List, Tuple

import numpy as np
import cirq
import quantum_decomp


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
    circuit = circuit.transform_qubits(mapping)
    ops = circuit.all_operations()

    for op in ops:
        if type(op) == cirq.ops.controlled_operation.ControlledOperation:
            gate = op

            controls = gate.controls
            target = gate.sub_operation.qubits
            matrix = cirq.unitary(gate.sub_operation.gate)

            decomposed_temp = cirq.optimizers.decompose_multi_controlled_rotation(matrix, list(controls), target[0])

            decomp_ops.append(decomposed_temp)
        else:
            decomp_ops.append(op)

    converter = cirq.google.optimizers.ConvertToSycamoreGates()
    SycamoreGates = converter.convert(decomp_ops)
    
    return SycamoreGates, []
