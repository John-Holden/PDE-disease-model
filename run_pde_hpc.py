import sys, os
import datetime
from run_scripts.run_pde import run_sim

job_id = sys.argv[1:][0]

date = datetime.datetime.today().strftime('%Y-%m-%d')
run_sim(date, job=job_id)