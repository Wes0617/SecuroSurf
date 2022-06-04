from __future__ import annotations

import ctypes
import pathlib as p
from multiprocessing import freeze_support
from securosurf.session_configuration_manager.json_tools import session_configuration_JSON_schema_generate_md
from securosurf_gui import application_admin_error
from securosurf_gui import application
from securosurf import information

########################################################################################################################

if __name__ == '__main__':
    freeze_support()

    simulation = False

    information.VAR = information.CLASS(p.Path(__file__).parent)

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(information.VAR.application_ID)

    session_configuration_JSON_schema_generate_md.FUNC()

    if ctypes.windll.shell32.IsUserAnAdmin() or simulation:
        application.FUNC(simulation)
    else:
        application_admin_error.FUNC()
