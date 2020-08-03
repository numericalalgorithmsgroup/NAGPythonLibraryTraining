from naginterfaces._primitive.lapacklin import dgesv as dgesv_primitive
from naginterfaces.base import utils
import numpy as np
import pandas as pd
import timeit
import ctypes

def call_dgesv_primitive(A,b,N,ipiv,info):
    N_c = utils.EngineIntCType(N)
    one_c = utils.EngineIntCType(1)
    A_c = A.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    ipiv_c = ipiv.ctypes.data_as(ctypes.POINTER(utils.EngineIntCType))
    b_c = b.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

    dgesv_primitive(N_c, one_c ,A_c ,N_c ,ipiv_c, b_c, N_c,info)

    r = np.ctypeslib.as_array(b_c,(N,1))
    return(r)

def compare_solvers(N,number=5,res_form='raw',verbose=False,fortran_order=False):
    if verbose:
        print(N)
    timeit_setup = "".join([
    "from scipy.linalg import toeplitz;",
    "from naginterfaces.library.lapacklin import dgesv;",
    "from naginterfaces.library.lapacklin import dsgesv;",
    "from naginterfaces.base.lapacklin import dgesv as dgesv_base;",
    "from naginterfaces.base.lapacklin import dsgesv as dsgesv_base;",
    "from naginterfaces.base import utils;",
    "from numpy.random import rand,seed;",
    "import numpy as np;",
    "import scipy as sp;",
    "import ctypes;",
    "from compare_solvers import call_dgesv_primitive;",
    #"A = toeplitz(rand({0}), rand({0}));".format(N),
    "seed(2);",
    "A = rand({0},{0});".format(N),
    "b = rand({0},1);".format(N),
    "ipiv = np.zeros({0},dtype='int64');".format(N),
    "info = utils.EngineIntCType(0);",
    "N={0};".format(N),
    "x = np.zeros(({0},1));".format(N)
    ])

    if(fortran_order):
        timeit_setup = timeit_setup + "A = np.asfortranarray(A);"

    scipy_computation = 'x = sp.linalg.solve(A,b);'
    if verbose:
        print('scipy')
        scipy_computation = scipy_computation + 'print(x);'
    scipy = timeit.timeit(scipy_computation, setup=timeit_setup, number=number)

    nag_dgesv_computation = '[a,ipiv,x] = dgesv(A, b);'
    if verbose:
        print('nag_dgesv')
        nag_dgesv_computation = nag_dgesv_computation + 'print(x);'
    nag_dgesv = timeit.timeit(nag_dgesv_computation, setup=timeit_setup,number=number)

    nag_dsgesv_computation = '[a,ipiv,x,itera] = dsgesv(A, b);'
    if verbose:
        print('nag_dsgesv')
        nag_dsgesv_computation = nag_dsgesv_computation + 'print(x);'
    nag_dsgesv = timeit.timeit(nag_dsgesv_computation, setup=timeit_setup,number=number)

    nag_dgesv_base_computation = 'dgesv_base(N,1,A,ipiv,b);'
    if verbose:
        print('nag_dsgesv_base')
        nag_dgesv_base_computation = nag_dgesv_base_computation + 'print(b);'
    nag_dgesv_base = timeit.timeit(nag_dgesv_base_computation, setup=timeit_setup, number=number)

    nag_dgesv_primitive_computation = 'call_dgesv_primitive(A,b,N,ipiv,info);'
    if verbose:
        print('nag_dsgesv_primitive')
        nag_dgesv_primitive_computation = nag_dgesv_primitive_computation + 'print(b);'
    nag_dgesv_primitive = timeit.timeit(nag_dgesv_primitive_computation, setup=timeit_setup, number=number)

    nag_dsgesv_base_computation = 'dsgesv_base(N, 1, A, ipiv, b, x);'
    if verbose:
        print('nag_dsgesv_base')
        nag_dsgesv_base_computation = nag_dsgesv_base_computation + 'print(x);'
    nag_dsgesv_base = timeit.timeit(nag_dsgesv_base_computation, setup=timeit_setup, number=number)

    #Return the average time taken for each calculation
    result = np.array([N,scipy/number,nag_dgesv/number,nag_dgesv_base/number,nag_dgesv_primitive/number,nag_dsgesv/number,nag_dsgesv_base/number])
    if res_form=='raw':
        pass

    #Set numpy speed for each numpycalculation to 1 and scale NAG results accordingly
    #A result of 2 would mean that numpy was twice as fast as NAG
    #A result of 0.5 would mean that NAG was twice as fast as numpy
    if res_form=='scaled':
        result[1:] = result[1:] / (scipy/number)

    return(result)
