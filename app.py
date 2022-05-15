from __future__ import annotations

import ctypes
import pathlib as p
from multiprocessing import freeze_support
from securosurf_gui import application_admin_error
from securosurf_gui import application

########################################################################################################################

if __name__ == '__main__':
    freeze_support()

    simulation = False

    root = p.Path(__file__).parent

    if ctypes.windll.shell32.IsUserAnAdmin() or simulation:
        application.FUNC(root, simulation)
    else:
        application_admin_error.FUNC(root)
