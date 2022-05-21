from __future__ import annotations

import ctypes
from multiprocessing import freeze_support
from securosurf_gui import application_admin_error
from securosurf_gui import application

########################################################################################################################

if __name__ == '__main__':
    freeze_support()

    simulation = False

    if ctypes.windll.shell32.IsUserAnAdmin() or simulation:
        application.FUNC(simulation)
    else:
        application_admin_error.FUNC()
