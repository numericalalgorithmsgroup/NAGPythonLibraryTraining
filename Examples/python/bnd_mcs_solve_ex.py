#!/usr/bin/env python
"``naginterface.library.glopt.bnd_mcs_solve`` Python Example."

# NAG Copyright 2017-2018.

# pylint: disable=invalid-name,too-many-locals

def main():
    """
    Example for :func:`naginterfaces.library.glopt.bnd_mcs_solve`.

    Global optimization by multi-level coordinate search.

    >>> main()
    naginterfaces.library.glopt.bnd_mcs_solve Python Example Results.
    Global optimization of the Peaks objective function.
    Final objective value is -6.55113
    Global optimum is (0.22828, -1.62553)
    """

    from math import exp
    from naginterfaces.library import glopt
    from matplotlib.patches import Rectangle
    from matplotlib.collections import PatchCollection
    from matplotlib import cm
    import matplotlib.pyplot as plt
    import numpy as np

    boxes = []
    def monit(
        _ncall, _xbest, _icount, _inlist, _numpts,
        _initpt, _xbaskt, boxl, boxu, _nstate,):
        boxes.append(Rectangle(boxl, *(boxu - boxl)))

    print('naginterfaces.library.glopt.bnd_mcs_solve Python Example Results.')
    print('Global optimization of the Peaks objective function.')

    # Initialize the communication structure for the solver:
    comm = glopt.bnd_mcs_init()

    # The problem configuration:
    n = 2
    objfun = lambda x, _nstate: (
        3.*(1. - x[0])**2*exp(-x[0]**2 - (x[1] + 1.)**2)
        - (10.*(x[0]/5. - x[0]**3 - x[1]**5)*exp(-x[0]**2 - x[1]**2))
        - 1./3.0*exp(-(x[0] + 1.)**2 - x[1]**2)
    )
    ibound = 0
    bl = [-3.]*n
    bu = [3.]*n

    # Set some algorithmic parameters:
    glopt.bnd_mcs_optset_int('Function Evaluations Limit', 100000, comm)
    glopt.bnd_mcs_optset_real('Local Searches Tolerance', 1.e-10, comm)
    glopt.bnd_mcs_optset_int('Splits Limit', 20, comm)
    glopt.bnd_mcs_optset_int('Static Limit', 8, comm)
    glopt.bnd_mcs_optset_int('Local Searches Limit', 40, comm)
    glopt.bnd_mcs_optset_char('Local Searches', 'On', comm)

#   mcs_soln = glopt.bnd_mcs_solve(objfun, ibound, bl, bu, comm)
    mcs_soln = glopt.bnd_mcs_solve(objfun, ibound, bl, bu, comm, monit=monit);

    delta = 0.025
    x = np.arange(bl[0], bu[0], delta)
    y = np.arange(bl[1], bu[1], delta)
    X, Y = np.meshgrid(x, y)
    Z = np.empty((len(X), len(Y)))
    for i, x_i in enumerate(x):
        for j, y_j in enumerate(y):
            Z[j, i] = objfun([x_i, y_j], None)

    start_x = [0.]*n
    min_x = [0.23, -1.63]
    boxes_col = PatchCollection(boxes,
    edgecolor='b', facecolor='none', linewidth=0.2,)

    print('Final objective value is {:.5f}'.format(mcs_soln.obj))
    print(
        'Global optimum is (' +
        ', '.join(['{:.5f}'.format(xi) for xi in mcs_soln.x]) +
        ')'
    )

    ax = plt.axes()
    ax.contour(X, Y, Z,
        levels=[-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 6, 8],
        cmap=cm.jet,)
    ax.plot(start_x[0], start_x[1], 'rx')
    ax.plot(min_x[0], min_x[1], 'go')
    ax.legend(('Start', 'Glob. min.'), loc='upper right')
    ax.add_collection(boxes_col)
    ax.axis(xmin=bl[0], ymin=bl[1], xmax=bu[0], ymax=bu[1])
    ax.set_title(r'The Peaks Function and MCS Search Boxes')
    plt.show()


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(
        doctest.testmod(
            None, verbose=True, report=False,
            optionflags=doctest.REPORT_NDIFF,
        ).failed
    )
