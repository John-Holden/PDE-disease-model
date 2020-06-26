import datetime
import os
import sys
from timeit import default_timer as timer

from treePde_py.large_scale_model import fkpp  # i.e. fkpp model
from treePde_py.mkdir.setup import save_info


# ---- finite difference parameters ---- #
# 1) tend : time-steps arb units
# 2) dx, dy : discrete spatial parameters in units (m)
# 3) v, d, g_factors : change the ratio of diffusion to growth


def run_sim(date, job):
    """
    :param date:
    :param job:
    :return:
    """
    domain_settings = {"data": "Fex", "beta": 0.020, "ell": 25, "subset": False}  # set domain and epidemic
    fd_settings = {"dx": 1000, "dy": 1000, "dt": 0.1,
                   "v_factor": 1, "d_factor": 1, "g_factor": 1}  # set fd solver

    model = fkpp.Model(domain_settings, fd_settings, epi_c=[700, 400])
    animate = False
    freq = 30
    tend = 10*365 + 1
    start = timer()
    # ---- start simulation ---- #
    print("Simulation Start @ time {}  @".format(datetime.datetime.now()))
    model.run_fd_solver(tend=tend, animate=animate, freq=freq)   # HPC mode animate = False
    print('Simulation finished @ time {}'.format(datetime.datetime.now()))
    # ---- end simulation ---- #
    save_info(output_path=model.out_dir, run_time=((timer() - start) / 60),
              domain_settings=domain_settings, fd_settings=fd_settings,
              tend=tend, animate=animate, freq=freq, epicenter=model.epi_c)
    return


if __name__ == "__main__":
    os.chdir('..')
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    run_sim(date, job="1")
    sys.exit()
