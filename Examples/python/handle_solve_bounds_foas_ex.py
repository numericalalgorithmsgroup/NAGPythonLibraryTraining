#!/usr/bin/env python
"``naginterfaces.library.opt.handle_solve_bounds_foas`` Python Example."

# NAG Copyright 2018.

# pylint: disable=invalid-name,line-too-long

def main():
    """
    Example for :func:`naginterfaces.library.opt.handle_solve_bounds_foas`.

    Large-scale first order active set bound-constrained nonlinear programming.

    >>> main()
    naginterfaces.library.opt.handle_solve_bounds_foas Python Example Results.
    Minimizing a bound-constrained Rosenbrock problem.
     -------------------------------------------------------------------------------
      E04KF, First order method for bound contrained problems
     -------------------------------------------------------------------------------
     Begin of Options
    ...
     End of Options
    <BLANKLINE>
     Status: converged, an optimal solution was found
     Value of the objective             4.00000E-02
    ...
     """

    from naginterfaces.base import utils
    from naginterfaces.library import opt

    print(
        'naginterfaces.library.opt.handle_solve_bounds_foas '
        'Python Example Results.'
    )
    print('Minimizing a bound-constrained Rosenbrock problem.')

    # The initial guess: Interesting scenarios
    # x = [-1.5, 1.9]
    # x = [-1.5, -2.5]
    # x = [-0.5, -2.1]
    # x = [-0.5, 1.0]
    x = [-1.0, -1.5]
    # x = [-0.9, -1.5]
    # x = [-2.0, 1.5]

    # The Rosenbrock objective:
    objfun = lambda x, inform: (
        (1. - x[0])**2 + 100.*(x[1] - x[0]**2)**2, inform,
    )

    def objgrd(x, fdx, inform):
        """The objective's gradient."""
        fdx[:] = [
            2.*x[0] - 400.*x[0]*(x[1]-x[0]**2) - 2.,
            200.*(x[1]-x[0]**2),
        ]
        return inform

    steps = []
    def monit(x, inform, rinfo, stats, data=None):
        """The monitor function."""
        steps.append([x[0], x[1], rinfo[0]])
        return inform

    # Create a handle for the problem:
    nvar = len(x)
    handle = opt.handle_init(nvar)

    # Define the bounds:
    bl = [-1., -2.]
    bu = [0.8, 2.]
    opt.handle_set_simplebounds(
        handle,
        bl=bl,
        bu=bu,
    )

    # Define the nonlinear objective:
    opt.handle_set_nlnobj(handle, idxfd=list(range(1, nvar+1)))

    # Set some algorithmic options.
    for option in [
            'FOAS Print Frequency = 5',
            'Print Solution = yes',
            'FOAS Monitor Frequency = 1',
            'Print Level = 2',
            'Monitoring Level = 3',
    ]:
        opt.handle_opt_set(handle, option)

    # Use an explicit I/O manager for abbreviated iteration output:
    iom = utils.FileObjManager(locus_in_output=False)

    # Solve the problem:
    ret = opt.handle_solve_bounds_foas(handle, objfun, objgrd, x, monit=monit, io_manager=iom)

    # Destroy the handle:
    opt.handle_free(handle)
    
    # Add solution to step list
    steps.append([ret.x[0], ret.x[1], ret.rinfo[0]])


    # Evaluate the funtion over the domain
    import numpy as np
    x_m = np.linspace(bl[0]-0.5, bu[0]+0.5, 101)
    y_m = np.linspace(bl[1]-0.5, bu[1]+0.5, 101)
    z_m = np.empty((101,101))
    j = y_m[0]
    for i in range(0, 101):
        for j in range(0, 101):
            z_m[i,j], _inform = objfun([x_m[i], y_m[j]], 1)
    nb = 25
    x_box = np.linspace(bl[0], bu[0], nb)
    y_box = np.linspace(bl[1], bu[1], nb)
    box = np.array([np.concatenate([x_box,bu[0]*np.ones(nb),x_box[::-1],bl[0]*np.ones(nb)]),
           np.concatenate([bl[1]*np.ones(nb),y_box,bu[1]*np.ones(nb),y_box[::-1]])])
    z_box = np.empty(box[0].shape)
    for i in range(0, (box[0].size)):
        z_box[i], _inform = objfun([box[0][i], box[1][i]], 1)

    X, Y = np.meshgrid(x_m, y_m, indexing='ij')

    # Plot function and steps taken
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    fig = plt.figure()
    ax = Axes3D(fig)
    ax = fig.gca(projection='3d')
    ax.grid(False)
    ax.plot(box[0], box[1], z_box,'k-',linewidth=1.5)
    ax.plot([bl[0],bu[0],bu[0],bl[0],bl[0]],[bl[1],bl[1],bu[1],bu[1],bl[1]],-1.2*np.ones(5),'k-')
    ax.contour(X, Y, z_m, 15, offset=-1.2, cmap=cm.jet)
    ax.plot_surface(X, Y, z_m, cmap=cm.jet, alpha=0.5)
    ax.set_title('Rosenbrock Function')
    ax.set_xlabel(r'$\mathit{x}$')
    ax.set_ylabel(r'$\mathit{y}$')
    steps = np.column_stack(steps)
    ax.plot(steps[0], steps[1], steps[2], 'o-', color='magenta', markersize=2)
    ax.azim = 160
    ax.elev = 35
    plt.show()

if __name__ == '__main__':
#    import doctest
#    import sys
#    sys.exit(
#        doctest.testmod(
#            None, verbose=True, report=False,
#            optionflags=doctest.ELLIPSIS | doctest.REPORT_NDIFF,
#        ).failed
#    )
    main()
