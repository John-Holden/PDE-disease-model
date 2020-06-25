import os, sys
from treePde_py.large_scale_model import fkpp  # i.e. fkpp model
import datetime
from timeit import default_timer as timer
from treePde_py.mkdir.setup import save_info


# ---- finite difference parameters ---- #
# 1) tend : time-steps arb units
# 2) dx, dy : discrete spatial parameters in units (m)
# 3) CFL_max : condition for numerical stability


def run_sim(date, job):
    """
    :param date:
    :param job:
    :return:
    """
    domain_settings = {"data": "Fex", "beta": 0.020, "ell": 25, "subset": False}  # set domain and epidemic
    fd_settings = {"dx": 1000, "dy": 1000, "dt": 0.1}  # set finite difference solver
    model = fkpp.Model(domain_settings, fd_settings, epi_c=[700, 550])
    animate = False
    freq = 30
    tend = 2000
    start = timer()
    # ---- start simulation ---- #
    print("Simulation Start @ time {}  @".format(datetime.datetime.now()))
    model.run_fd_solver(tend=tend, animate=animate, freq=freq)   # HPC mode animate = False
    print('Simulation finished @ time {}'.format(datetime.datetime.now()))
    # ---- end simulation ---- #
    save_info(output_path=model.out_dir, run_time=((timer() - start) / 60),
              domain_settings=domain_settings, fd_settings=fd_settings,
              velocity_multipler=model.v_factor, diffusion_multiplier=model.d_factor,
              growth_multiplier=model.g_factor, tend=tend, animate=animate, freq=freq)
    return


if __name__ == "__main__":
    os.chdir('..')
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    run_sim(date, job="1")
    sys.exit()
