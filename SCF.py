"""
SCF.py is a module that contains all of the functions
for the HF SCF Procedure
"""

import numpy as np
import scipy as sp


def calc_nuclear_repulsion_energy(mol_):
    """
    calc_nuclear_repulsion_energy - calculates the n-e repulsion energy of a
                                    molecule

    Arguments:
        mol_: the PySCF molecule data structure created from Input

    Returns:
        Enuc: The n-e repulsion energy
    """

    charges = mol_.atom_charges() #charge of atom
    coords = mol_.atom_coords() #position of atom
    Enuc = 0 
    distance_matrix = np.zeros((3, 3), dtype=np.double) #calculates distance matrix between all atoms

    #calculate distance matrix between all atoms
    for x in range (len(coords)):
        for y in range (len(coords[x])):
            distance_matrix[x][y]=np.linalg.norm(coords[x]-coords[y])

    #print(distance_matrix.shape)
    #0print(distance_matrix)
    
    #loop over atoms and calculate Enuc
    for x in range(len(coords)):
        for y in range(len(coords[x])):
            if y>x:
                Enuc+= ((charges[x] * charges[y]) / distance_matrix[x][y])
    return Enuc
        

    """
    Replace with your implementation

    Step 1. calcuate (3x3) distance matrix between all atoms
    Step 2. Loop over atoms and calculate Enuc from formulat in Readme
    """


def calc_initial_density(mol_):
    """
    calc_initial_density - Function to calculate the initial guess density

    Arguments
        mol_: the PySCF molecule data structure created from Input

    Returns:
        Duv: the (mol.nao x mol.nao) Guess Density Matrix
    """

    num_aos = mol_.nao  # Number of atomic orbitals, dimensions of the mats
=======
    Duv=np.zeros((num_aos, num_aos), dtype=np.double) #using a matrix of zeros as initial guess

    return Duv


def calc_hcore_matrix(Tuv_, Vuv_):
    """
    calc_hcore_matrix - Computes the 1 electron core matrix

    Arguments:
        Tuv_: The Kinetic Energy 1e integral matrix
        Vuv_: The Nuclear Repulsion 1e integrals matrix

    Returns:
        h_core: The one electron hamiltonian matrix
    """

    h_core=Tuv_ + Vuv_ 

    return h_core


def calc_fock_matrix(mol_, h_core_, er_ints_, Duv_):
    """
    calc_fock_matrix - Calculates the Fock Matrix of the molecule

    Arguments:
        mol_: the PySCF molecule data structure created from Input
        h_core_: the one electron hamiltonian matrix
        er_ints_: the 2e electron repulsion integrals
        Duv_: the density matrix

    Returns:
        Fuv: The fock matrix

    """

    Fuv = h_core_.copy()  # Takes care of the Huv part of the fock matrix
    num_aos = mol_.nao    # Number of atomic orbitals, dimension of the mats
    for u in range(num_aos):
        for v in range(num_aos):
            Fuv[u, v] = Fuv[u, v] + (Duv_ * er_ints_[u, v]).sum() - (0.5*Duv_ * er_ints_[u, :, v]).sum()

    """
    Replace with your implementation

    Here you will do the summation of the last two terms in the Fock matrix
    equation involving the two electron Integrals

    Hint: You can do this with explicit loops over matrix indices, whichwill
          have many for loops.

    This can also be done with numpy aggregations, bonus points if you
    implement this with only two loops.

    For example, the first term can be implemented like the following:
    (er_ints[mu,nu]*Duv).sum()
    """

    return Fuv


def solve_Roothan_equations(Fuv_, Suv_):

    mo_energies, mo_coeffs=sp.linalg.eigh(Fuv_, Suv_) #mo_energies is eigenvector & mo_coeffs is eigenvalues

    """
    solve_Roothan_equations - Solves the matrix equations to determine
                              the MO coefficients

    Arguments:
        Fuv_: The Fock matrix
        Suv_: The overlap matrix

    Returns:
        mo_energies: an array that contains eigenvalues of the solution
        mo_coefficients: a matrix of the eigenvectors of the solution

    """

    """
    Replace with your implementation

    The Roothan Equations, which are of the form FC=SCe can be solved
    directly from the proper use of scipy.linalg.eigh since this is a
    symmetric hermitian matrix. Take a look at the documentation for that
    function and you can implement this in one line.
    """

    return mo_energies.real, mo_coeffs.real


def form_density_matrix(mol_, mo_coeffs_):
    """
    form_dentsity_matrix - forms the density matrix from the eigenvectors

    Note: the loops are over the number of electrons / 2, not all of the
    atomic orbitals

    Arguments:
        mol_: the PySCF molecule data structure created from Input
        mo_coefficients: a matrix of the eigenvectors of the solution

    Returns:
        Duv: the density matrix
    """

    nelec = mol_.nelec[0]  # Number of occupied orbitals
    num_aos = mol_.nao  # Number of atomic orbitals, dimensions of the mats
    Duv = np.zeros(mol_.nao, mol_.nao, dtype=np.double)

    for u in range(num_aos):
        for v in range(num_aos):
            for i in range(nelec):
                Duv[u][v]= Duv[u][v] + 2*(mo_coeffs_[u][i] * mo_coeffs_[v][i])
    """
    Replace with your implementation

    This involves basically a computation of each density matrix element
    that is a sum over the produces of the mo_coeffs.

    """

    return Duv


def calc_total_energy(Fuv_, Huv_, Duv_, Enuc_):
    """
    calc_total_energy - This function calculates the total energy of the
    molecular system

    Arguments:
        Fuv_: the current Fock Matrix
        Huv_: the core Hamiltonian Matrix
        Duv_: the Density Matrix that corresponds to Fuv_
        Enuc: the Nuclear Repulsion Energy

    Returns:
        Etot: the total energy of the molecule
    """
    Etot= 0.5*(Duv_ * (Huv_+Fuv_)).sum()+ Enuc_
    print (Etot)
   
    """
    Replace with your implementation

    Should be able to implement this in one line with matrix arithmatic

    """


    return Etot