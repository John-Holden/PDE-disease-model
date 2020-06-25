from treePde_py.plot.epidemic import PltStep
from treePde_py.large_scale_model import fkpp
import matplotlib.pyplot as plt
import numpy as np
import os, sys
domain_settings = {"data": "Fex", "beta": 0.020, "ell": 25, "subset": False}  # set domain and epidemic
fd_settings = {"dx": 1000, "dy": 1000, "dt": 0.1}  # set finite difference solver
model = fkpp.Model(domain_settings, fd_settings)

bcds = np.where(model.sea_bcd == 0)
plots = PltStep(bcd=bcds, domain=model.domain, save=os.getcwd())

sim_name = "/fkpp_Fex_b_0_02_ell_25_hpc_test"
frame = 9
u_uk = np.load(os.getcwd() + '/model_data' + sim_name+'/infectious_field/{}.npy'.format(frame))

plots.step(u_uk, c=frame, title=False, sim_plt=False)



