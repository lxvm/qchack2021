from typing import List, Tuple

import numpy as np
import cirq

def two_qubit(
    target_qubits: List[cirq.GridQubit], matrix: np.ndarray
) -> Tuple[cirq.OP_TREE, List[cirq.GridQubit]]:
    G = cirq.MatrixGate(matrix)(target_qubits[0], target_qubits[1])
    converter = cirq.google.optimizers.ConvertToSycamoreGates()
    SycamoreGates = converter.convert(G)
    return SycamoreGates, []
