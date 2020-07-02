"""
Support functions for regression exercises.
"""
# pylint: disable=invalid-name,too-many-arguments,too-many-locals
import numpy as np
from naginterfaces.library import rand

def gen_multivar_x(m, n, statecomm, dist_id="MN", sigma=2.0, rho=0.5):
    """
    Generate independent variables.

    Current options for dist_id are are
      "MN" for multivariate normal,
      "T3" for multivariate t with 3 degrees of freedom
    sigma determines the diagonal entries of the covariance matrix, i.e. variances of x
    rho   determines the off-diagonal entries of the covariance matrix
    """
    n = int(n)
    xmu = np.ones(m)
    c = np.zeros((m, m))
    for i in range(m):
        for j in range(m):
            c[i, j] = (sigma ** 2) * rho ** abs(i-j)

    # NAG arguments for multivar_XXX functions
    mode = 2
    r = np.zeros(m*(m+1) + 2)

    # call random sampling
    if dist_id == "MN":
        sorder = 1
        r, x = rand.multivar_normal(sorder, mode, n, xmu, c, r, statecomm)
    if dist_id == "T3":
        df = 3
        c_t = (float(df) - 2) / float(df) * c
        r, x = rand.multivar_students_t(mode, n, df, xmu, c_t, r, statecomm)

    return x

def gen_obs(x, statecomm):
    """
    Generate observations.
    """
    m = x.shape[1]
    n = x.shape[0]
    x = np.matrix(x)

    # set regression coefficients
    beta = np.matrix(np.ones((m, 1)))

    # sample observation noise
    epsilon = np.matrix(rand.dist_normal(n, 0.0, 9.0, statecomm)).reshape(n, 1)

    # define synthetic observations
    y = x * beta + epsilon

    return np.squeeze(np.asarray(y))
