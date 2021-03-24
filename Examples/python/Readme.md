# Instructions to run demos

```
python3 -m venv ni3dev
. ni3dev/bin/activate
python -m pip install --extra-index-url https://www.nag.com/downloads/py/naginterfaces_mkl naginterfaces
```

## Activate environment:
. ~/ni3dev/bin/activate

## Example: DFO least square fitting data to the Kowalik and Osborne function (Mk 26.1)
python handle_solve_dfls_ex.py

## Example: Rosenbrock FOAS Optimisation (Mk 27)
python handle_solve_bounds_foas_ex.py

## Example: Fit 2D spline (Mk 26)
python dim2_spline_ts_sctr_ex.py

## Example: Multiple quantile linear regression
python quantile_linreg_ex.py

## Example: Global optimisation
python bnd_mcs_solve_ex.py

