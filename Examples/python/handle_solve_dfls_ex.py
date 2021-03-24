#!/usr/bin/env python
"``naginterfaces.library.opt.handle_solve_dfls`` Python Example."

# NAG Copyright 2018.

# pylint: disable=invalid-name

def main():
    """
    Example for :func:`naginterfaces.library.opt.handle_solve_dfls`.

    Derivative-free solver for a nonlinear least squares objective function.

    >>> main()
    naginterfaces.library.opt.handle_solve_dfls Python Example Results.
    Minimizing the Kowalik and Osborne function.
    ...
      Status: Converged, small trust region size
    ...
      Value of the objective                    4.02423E-04
      Number of objective function evaluations           27
      Number of steps                                    10
    ...
     Primal variables:
       idx   Lower bound        Value      Upper bound
         1       -inf       1.81300E-01         inf
         2   2.00000E-01    5.90128E-01    1.00000E+00
         3       -inf       2.56929E-01         inf
         4   3.00000E-01    3.00000E-01         inf
    """

    from naginterfaces.base import utils
    from naginterfaces.library import opt
    from copy import deepcopy

    print(
        'naginterfaces.library.opt.handle_solve_dfls Python Example Results.'
    )
    print('Minimizing the Kowalik and Osborne function.')

    # The initial guess:
    x = [0.25, 0.39, 0.415, 0.39]

    # The Kowalik and Osborne function:
    y = [
        4., 2., 1., 0.5, 0.25, 0.167, 0.125, 0.1, 0.0833, 0.0714, 0.0625
    ]
    z = [
        0.1957, 0.1947, 0.1735, 0.1600, 0.0844, 0.0627, 0.0456, 0.0342,
        0.0323, 0.0235, 0.0246
    ]
    objfun = lambda x, _nres: z - x[0]*(y*(y+x[1]))/(y*(y+x[2]) + x[3])
    fit = lambda x, y: x[0]*(y*(y+x[1]))/(y*(y+x[2]) + x[3])
 
    steps = []
    def monit(x, rinfo, stats, data=None):
        """The monitor function."""
        pt = deepcopy(x)
        steps.append([pt, rinfo[0]])



    # Create a handle for the problem:
    handle = opt.handle_init(nvar=len(x))

    # Define the residuals structure:
    nres = 11
    opt.handle_set_nlnls(
        handle, nres,
        irowrd=None, icolrd=None,
    )

    # Define the bounds:
    opt.handle_set_simplebounds(
        handle,
        bl=[-1.e20, 0.2, -1.e20, 0.3],
        bu=[1.e20, 1., 1.e20, 1.e20],
    )

    # Set some algorithmic options.
    # Relax the main convergence criteria slightly:
    opt.handle_opt_set(handle, 'DFLS Trust Region Tolerance = 5.0e-6')
    # Turn off option printing:
    opt.handle_opt_set(handle, 'Print Options = NO')
    # Print the solution:
    opt.handle_opt_set(handle, 'Print Solution = YES')
    # Call Monitor at each step to log progress
    opt.handle_opt_set(handle, 'DFO Monitor Frequency = 1')


    # Use an explicit I/O manager for abbreviated iteration output:
    iom = utils.FileObjManager(locus_in_output=False)

    # Solve the problem:
    ret = opt.handle_solve_dfls(handle, objfun, x, nres, monit=monit, 
            io_manager=iom)

    # Destroy the handle:
    opt.handle_free(handle)

    

    import numpy as np
    m_y = np.linspace(y[0], y[-1])
    m_z = fit(x, m_y) 

    import matplotlib.pyplot as plt
    from matplotlib import cm
    
    cols = cm.jet(range(0,240,20))
    plt.grid(True)
    # plot initial guess (parameters x)
    i = 0
    plt.plot(m_y, m_z, '-', color=cols[i][0:3])

    # plot intermediary fits
    for s in steps:
        i = i + 1
        m_z = fit(s[0], m_y)
        plt.plot(m_y, m_z, '-', color=cols[i][0:3],
                label=r'LSE: {:.3e}'.format(s[1]))

    # plot optimised/fitted parameters ret.x)
    m_z = fit(ret.x, m_y)
    plt.plot(m_y, m_z, '-', color=cols[-1][0:3], linewidth=3, label=r'LSE: {:.3e}'.format(ret.rinfo[0]))
    plt.plot(y, z, 'gx', markersize=7, label='Observations')

    plt.xlabel('$y$')
    plt.ylabel('$z=p(y,t=x)$')
    plt.legend(loc='lower right')
    plt.title(
        'DFO NLLS fit for the Kowalik and Osborne function'
    )

    plt.show()


if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(
        doctest.testmod(
            None, verbose=True, report=False,
            optionflags=doctest.ELLIPSIS | doctest.REPORT_NDIFF,
        ).failed
    )
