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

(build_path / "errors").mkdir()

shutil.copytree(cwd / "errors", build_path / "errors")

_configs = [
    "session.normal.json",
    "session.solo.json",
    "session.lan.json",
    "session.dynamic.json"
]

for _config in _configs:
    _source = cwd / _config
    _destination = build_path / _config
    shutil.copyfile(_source, _destination)

zip_path = cwd / "build" / "zipped_build"
shutil.make_archive(str(zip_path), 'zip', build_path)
