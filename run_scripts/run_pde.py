import os, sys
os.chdir('..')
from treePde_py.large_scale_model import fkpp  # i.e. fkpp model


# ---- finite difference parameters ---- #
# 1) tend : time-steps arb units
# 2) dx, dy : discrete spatial parameters in units (m)
# 3) CFL_max : condition for numerical stability

domain_settings = {"data": "Fex", "beta": 0.020, "ell": 25, "subset": True}  # set domain and epidemic
fd_settings = {"dx": 1000, "dy": 1000, "dt": 0.01}  # set finite difference solver

model = fkpp.Model(domain_settings, fd_settings)
model.run_fd_solver(tend=200)

#  todo  continue with paramters and scaling add in advection see why getting negatives...
#  todo make fucking sense of this ....?!