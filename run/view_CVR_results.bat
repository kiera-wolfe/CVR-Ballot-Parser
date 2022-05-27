@echo off

cd "C:\CVR_Reader\src"
echo %__CD__%
echo Welcome to the 2021 Senior Design Team 19 Project.
echo Verify the CVR you wish to use is located in the - CVR Folder -.
pause

echo Ensure the config.yaml file matches the CVR you are using and your desired display settings.
pause

rem arg 1 = repository root directory
rem * since we CD into the src directory, %__CD__%\.. should be the repo root path
rem arg 2 = configuration file directory relative to repo-root or absolute
rem arg 3 = CVR directory path relative to repo-root or absolute
bokeh serve ^
      --show display.py ^
      --args %__CD__%\.. run run\cvr
