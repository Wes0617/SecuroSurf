import os
import sys
import shutil
import pathlib as p
from cx_Freeze import setup, Executable
from securosurf import information

########################################################################################################################

information.VAR = information.CLASS(p.Path(__file__).parent)

# ----------------------------------------------------------------------------------------------------------------------

_build_directory_filename = f"exe.win-amd64-{sys.version_info.major}.{sys.version_info.minor}"
build_path = information.VAR.path / "build" / _build_directory_filename
if os.path.exists(build_path):
    shutil.rmtree(build_path)

# ----------------------------------------------------------------------------------------------------------------------

build_exe_options = {
    "optimize": 2,
    'build_exe': build_path
}

_executable_name = information.VAR.application_name + ".exe"
setup(
    name=information.VAR.application_name,
    version=information.VAR.application_version,
    options=dict(build_exe=build_exe_options),
    executables=[Executable("app.py", targetName=_executable_name, icon=information.VAR.icon_path, base="Win32GUI")],
    packages=["securosurf", "securosurf_gui", "securosurf_gui_toolkit"],
)

# ----------------------------------------------------------------------------------------------------------------------

for _asset_directory_filename in information.VAR.asset_directories_filenames:
    _source = information.VAR.path / _asset_directory_filename
    _dest = build_path / _asset_directory_filename
    if _source.is_dir():
        shutil.copytree(_source, _dest)
    _dest.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------------------------------------------------

zip_path = information.VAR.path / "build" / "zipped_build"
shutil.make_archive(str(zip_path), 'zip', build_path)
