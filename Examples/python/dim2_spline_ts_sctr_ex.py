#!/usr/bin/env python
"``naginterfaces.library.fit.dim2_spline_ts_sctr`` Python Example."

# NAG Copyright 2017-2018.

# pylint: disable=invalid-name,too-many-locals

def main():
    """
    Example for :func:`naginterfaces.library.fit.dim2_spline_ts_sctr`.

    Spline approximation to a set of scattered data using a two-stage
    approximation method.

    >>> main()
    naginterfaces.library.fit.dim2_spline_ts_sctr Python Example Results.
    Fit a spline for the Franke function.
    Spline value at (0.00, 0.00) is 0.76.
    """

    import numpy as np

    from naginterfaces.library import fit, rand

    print(
        'naginterfaces.library.fit.dim2_spline_ts_sctr '
        'Python Example Results.'
    )
    print('Fit a spline for the Franke function.')

    # Generate some scattered (x,y) data;
    # 100 pseudorandom uniformly-distributed values
    # on (0,1] using the Wichmann-Hill I generator:
    statecomm = rand.init_repeat(genid=2, seed=[32958])
    n = 100
    x = rand.dist_uniform01(n, statecomm)
    y = rand.dist_uniform01(n, statecomm)
    # Ensure that the bounding box includes the
    # corners (0,0) and (1,1):
    x[0], y[0] = 0., 0.
    x[-1], y[-1] = 1., 1.

    # The Franke function values for that scattered data:
    f = (
        0.75*np.exp(
            -(
                (9.*x-2.)**2 +
                (9.*y-2.)**2
            )/4.
        ) +
        0.75*np.exp(
            -(9.*x+1.)**2/49. -
            (9.*y+1.)/10.
        ) +
        0.5*np.exp(
            -(
                (9.*x-7.)**2 +
                (9.*y-3.)**2
            )/4.
        ) -
        0.2*np.exp(
            -(9.*x-4.)**2 -
            (9.*y-7.)**2
        )
    )

    # The configuration for the spline fit.
    # Grid size:
    nxcels = 6
    nycels = 6
    # Global smoothing level:
    gsmoothness = 1
    # Parameters for the local fit:
    lsminp = 3
    lsmaxp = 100

    # Initialize the fitting routine and set some algorithmic options
    # for it:
    comm = {}
    for fit_opt in [
            'Initialize = dim2_spline_ts_sctr',
            'Global Smoothing Level = {:d}'.format(gsmoothness),
            'Averaged Spline = Yes',
            'Local Method = Polynomial',
            'Minimum Singular Value LPA = {:f}'.format(1./32.),
            'Polynomial Starting Degree = 3',
    ]:
        fit.opt_set(fit_opt, comm)

    # Compute the spline coefficients:
    fit.dim2_spline_ts_sctr(
        x, y, f, lsminp, lsmaxp, nxcels, nycels, comm,
    )

    # Evaluate the spline at a point (two vectors of singletons):
    x_eval = 0.
    y_eval = 0.
    print('Spline value at ({:.2f}, {:.2f}) is {:.2f}.'.format(
        x_eval, y_eval, fit.dim2_spline_ts_evalv([x_eval], [y_eval], comm)[0],
    ))

    x_m = np.linspace(0, 1, 101)
    y_m = np.linspace(0, 1, 101)
    z_m = fit.dim2_spline_ts_evalm(x_m, y_m, comm)

    X, Y = np.meshgrid(x_m, y_m, indexing='ij')

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.grid(False)
    ax.plot_wireframe(X, Y, z_m, color='red', linewidths=0.4)
    ax.scatter(x, y, f, c='blue')
    ax.contour(X, Y, z_m, 15, offset=-1.2, cmap=cm.jet)
    ax.set_title('Spline Fit of the Franke Function')
    ax.set_xlabel(r'$\mathit{x}$')
    ax.set_ylabel(r'$\mathit{y}$')
    ax.set_zlim3d(-1.2, 1.2)
    ax.azim = -20
    ax.elev = 20
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
