
from treePde_py.plot.epidemic import PltStep
from treePde_py.large_scale_model import fkpp
import matplotlib.pyplot as plt
import numpy as np
import os, sys
os.chdir('..')


sim_name = "/fkpp_Fex_b_0_02_ell_25_naieve"
sim_name = "/fkpp_Fex_b_0_02_ell_25_g_0_5_d_500"
# load fd settings

with open(os.getcwd() + '/model_data/'+sim_name+'/info/ensemble_info.txt', mode='r') as file:
    for line in file:
        if line.split()[0] == "dt":
            dt = float(line.split()[-1])
        if line.split()[0] == "dx":
            dx = float(line.split()[-1])
        if line.split()[0] == "dy":
            dy = float(line.split()[-1])
        if line.split()[0] == "v_factor":
            v_fact = float(line.split()[-1])
        if line.split()[0] == "g_factor":
            g_fact = float(line.split()[-1])
        if line.split()[0] == "d_factor":
            d_fact = float(line.split()[-1])
        if line.split()[0] == "freq":
            freq = float(line.split()[-1])

domain_settings = {"data": "Fex", "beta": 0.020, "ell": 25, "subset": False}  # set domain and epidemic
fd_settings = {"dx": 1000, "dy": 1000, "dt": dt, "g_factor":
    g_fact, "d_factor": d_fact, "v_factor": v_fact}  # set finite difference solver
model = fkpp.Model(domain_settings, fd_settings)

try:  # make animations folder to save in
    os.mkdir(os.getcwd() + '/model_data' + sim_name + '/animations')
except FileExistsError:
    print("file {} exists...".format(os.getcwd() + '/model_data' + sim_name + '/animations'))


plots = PltStep(bcd=np.where(model.sea_bcd == 0), domain=model.domain, vmap=model.velocity_map,
                save=os.getcwd() + '/model_data' + sim_name + '/animations')

# frames = [31, 33]
frames = range(1, 11, 1)
for i, frame in enumerate(frames):
    print('i = {} : T step = {}'.format(i, frame * freq))
    u_uk = np.load(os.getcwd() + '/model_data' + sim_name + '/infectious_field/{}.npy'.format(frame))
    plots.step(u_uk, c=i, title=frame*freq, sim_plt=False, show=True, ext='.pdf')
#




