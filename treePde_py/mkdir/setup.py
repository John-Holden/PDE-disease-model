import os, sys
import numpy as np


def mkdir(output_path):
    """

    :param output_path:
    :return:
    """

    if os.path.exists(output_path):
        return
    else:
        try:
            # Create folders to save hpc sims
            os.mkdir(output_path)
            os.mkdir(output_path + '/info')
            os.mkdir(output_path + '/infectious_field')
            os.mkdir(output_path + '/time_series/')
            return

        except FileExistsError:
            print("!! File {}, already exists !! ".format(output_path))

            return


def save_info(output_path, run_time, domain_settings, fd_settings, **kwargs):
    """
    Save simulation parameters and settings to file. Called in run_tree_scripts upon exit of hpc ensemble.
    :param output_path: str,
    :param kwargs: various simulation parameters and settings used.
    :return:
    """
    with open(output_path + "/info/ensemble_info.txt", "w+") as info_file:
        info_file.write("______Simulation Parameters_______" + "\n")
        for kw in domain_settings:
            info_file.write(kw + ' : ' + str(domain_settings[kw]) + '\n')
        for kw in fd_settings:
            info_file.write(kw + ' : ' + str(fd_settings[kw]) + '\n')
        for kw in kwargs:
            info_file.write(kw + ' : ' + str(kwargs[kw]) + '\n')

        info_file.write("physical run time : " + str(round(run_time, 2)) + ' (minutes) \n')
        info_file.write("Notes : '...' ")  # Note section to document results


    return


"""


        for kw in kwargs:
            if type(kwargs[kw]) == np.ndarray:
                np.save(output_path+'/info/'+kw, kwargs[kw])
                info_file.write(kw + ' : ' + str(kwargs[kw][0]) + ' - ' + str(kwargs[kw][-1]) + '\n')
            else:
                info_file.write(kw + ' : ' + str(kwargs[kw]) + '\n')
        


"""
