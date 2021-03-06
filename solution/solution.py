from typing import List, Tuple

import numpy as np
import cirq
from solution.SingleQubit import single_qubit
from solution.TwoQubit import two_qubit
from solution.RandomMatrix import random_matrix


def matrix_to_sycamore_operations(
    target_qubits: List[cirq.GridQubit], matrix: np.ndarray
) -> Tuple[cirq.OP_TREE, List[cirq.GridQubit]]:
    """A method to convert a unitary matrix to a list of Sycamore operations.

    This method will return a list of `cirq.Operation`s using the qubits and (optionally) ancilla
    qubits to implement the unitary matrix `matrix` on the target qubits `qubits`.
    The operations are also supported by `cirq.google.gate_sets.SYC_GATESET`.

    Args:
        target_qubits: list of qubits the returned operations will act on. The qubit order defined by the list
            is assumed to be used by the operations to implement `matrix`.
        matrix: a matrix that is guaranteed to be unitary and of size (2**len(qs), 2**len(qs)).
    Returns:
        A tuple of operations and ancilla qubits allocated.
            Operations: In case the matrix is supported, a list of operations `ops` is returned.
                `ops` acts on `qs` qubits and for which `cirq.unitary(ops)` is equal to `matrix` up
                 to certain tolerance. In case the matrix is not supported, it might return NotImplemented to
                 reduce the noise in the judge output.
            Ancilla qubits: In case ancilla qubits are allocated a list of ancilla qubits. Otherwise
                an empty list.
        .
    """
    if np.all(matrix == np.eye(2**len(target_qubits))):
        return [], []
    if (len(target_qubits) == 1):
        return single_qubit(target_qubits, matrix)
    if (len(target_qubits) == 2):
        return two_qubit(target_qubits, matrix)
    if np.count_nonzero(matrix) == 2**len(target_qubits):
        # Either diagonal or increment
        if len(target_qubits) < 5:
            return random_matrix(target_qubits, matrix)
        elif len(target_qubits) < 7:
            return random_matrix(target_qubits, matrix, swap=False)
    if len(target_qubits) < 5:
        return random_matrix(target_qubits, matrix)
    elif len(target_qubits) < 5:
        return random_matrix(target_qubits, matrix, swap=False)

    return NotImplemented, []
