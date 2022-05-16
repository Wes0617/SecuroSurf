import os
import sys
import shutil
import pathlib
from cx_Freeze import setup, Executable
from securosurf import information

########################################################################################################################

cwd = pathlib.Path(__file__).parent
_build_directory_filename = f"exe.win-amd64-{sys.version_info.major}.{sys.version_info.minor}"
build_path = cwd / "build" / _build_directory_filename
icon_path = cwd / "images" / "icon.ico"

if os.path.exists(build_path):
    shutil.rmtree(build_path)

_executable_name = information.VAR.application_name + ".exe"
setup(
    name=information.VAR.application_name,
    version=information.VAR.application_version,
    options=dict(build_exe=dict(optimize=2)),
    executables=[Executable("app.py", targetName=_executable_name, icon=icon_path, base="Win32GUI")],
    packages=["securosurf", "securosurf_gui", "securosurf_gui_toolkit"],
)

shutil.copytree(cwd / "images", build_path / "images")

shutil.copytree(cwd / "errors", build_path / "errors")

_session_configuration_builtin_names = ["normal", "solo", "lan", "dynamic", "crew.Example Crew"]
for _name in _session_configuration_builtin_names:
    _source = cwd / f"session.{_name}.json"
    _destination = build_path / f"session.{_name}.json"
    shutil.copyfile(_source, _destination)
