# qchack2021

## Quickstart

### Local installation (for git collaboration)

[Install Python!](https://www.python.org/downloads/)
(This can also be done with a package manager.)

Create and activate a virtual environment for all things qiskit:

```
# Do this outside the repository
# or add the venv to the .gitignore
python3 -m venv qiskit
. qiskit/bin/activate
# and activate the environment in new terminals
```

(This can also be done with conda.)

Download qiskit packages:

```
# core library
python3 -m pip install qiskit 
# for using jupyter and visualizations
python3 -m pip install "qiskit[visualization]" jupyterlab
```

### Cloud setup (with IBM)

Go to https://quantum-computing.ibm.com
and log in with github or create an account.
Verify email address, etc ...

This gives access to the IBM quantum cloud:
- IBM Quantum Composer (for interactive circuit design)
- IBM Quantum Lab (a qiskit jupyter environment)
- Compute on IBM's quantum servers (with API tokens)

## Links

- [Hackathon!](https://www.qchack.io/)
- [qiskit](https://qiskit.org/)
- [qiskit start guide](https://qiskit.org/documentation/getting_started.html)
- [learn qiskit](https://qiskit.org/learn)
- [qiskit textbook](https://qiskit.org/textbook)
