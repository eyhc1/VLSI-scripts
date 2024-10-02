#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# small script to setup a cad assginment folder

import os, sys, tkinter, json, base64
from tkinter.filedialog import askdirectory
from tkinter import simpledialog
root = tkinter.Tk()
root.withdraw()

NAME = simpledialog.askstring(title="What's Your Name", prompt="Please enter your full name, with space in between first and last name (e.g. John Doe):").replace(" ", "_")
sys.stdout.write(f'Turnin name set to {NAME}\n')
DESIGN_LIB = simpledialog.askstring(title="Design Name", prompt="Please enter your cadence project name (e.g. cad0):")
sys.stdout.write(f'Project name set to {DESIGN_LIB}\n')
FOLDER_476 = "/home/projects/ee476"
USER = os.environ.get("USER")
CAD_FOLDER = f"{FOLDER_476}/{USER}/cadence"
if not os.path.isdir(CAD_FOLDER):
    CAD_FOLDER = askdirectory(title='Select your "cadence" Folder')

proj_path = os.path.join(FOLDER_476, USER, DESIGN_LIB)

sys.stdout.write(proj_path + "\n")

os.makedirs(proj_path, exist_ok=True)
os.system(f'cd {proj_path} && ln -s {CAD_FOLDER}')
os.makedirs(os.path.join(proj_path, "spice"), exist_ok=True)

# basic setup complete, now looking for specification.json, if exit in that directory
if os.path.exists("specifications.json"):
    sys.stdout.write('"specifications.json" found! creating part folders and renameing path\n')
    sys.path.insert(0, '/home/projects/ee476/common/scripts')  # assume check_spec is in script folder in common dir, and did not get deleted
    import check_spec as cks
    spec = json.loads(cks.json_minify("specifications.json"))
    curr_path = spec["path"]  # remembers what the current "path" line is written, we'll re-write that line later
    parts = spec["parts"]

    # TODO: this part assumes that the spec file always the format of 'cat#/part#/filename,  which may not exactly be the case
    # creat folders
    for k, v in parts.items():
        files = list(v["files"].keys())

        if len(files) <= 1 and 'none' in files:
            continue  # assume nothing to submit
        for i in files:
            spicedir = os.path.join(proj_path, "spice", i.split("/")[1])
            os.makedirs(spicedir, exist_ok=True)
            if ".ckt" in i:
                # create dummy control file for a circuit file
                ctl = i.split("/")[-1]
                open(os.path.join(spicedir, f'{ctl.replace(".ckt", "")}.ctl'), "w").write(f'* Starter control file\n.LIB "/home/projects/ee476.2022aut/common/cadence_setup/freepdk45.l" tt_lib\n.INCLUDE "{ctl}"\n* Start write your lines here\n')
                # generate makefile
                makefile = open(os.path.join(spicedir, "Makefile"), "w")
                makefile.write(f'DESIGN_LIB = {DESIGN_LIB}\nDESIGN = {ctl.replace(".ckt", "")}\n')
                makefile.write(f'DESIGN_DIR = {CAD_FOLDER}\n')
                makefile.write(
"""
# Do not edit anything beyond this point
COMMON_DIR = /home/projects/ee476/common
include $(COMMON_DIR)/scripts/freepdk45_top.mk
"""
                )


    # preload turnin folder
    sys.stdout.write(f'Copying check_spec.py to submission folder {os.path.join(proj_path, NAME)}\n')
    turnin = os.path.join(proj_path, NAME)
    os.makedirs(os.path.join(turnin, f'{os.path.split(proj_path)[-1]}_turnin'), exist_ok=True)
    os.popen(f'cp /home/projects/ee476/common/auto_grade/check_spec.py {os.path.join(turnin, "check_spec.py")}')
    # modify the spec json, assume that it has the line as this format: "path": "<Student_Name> /home/projects/ee476/<Student_ID>/<Path_To_Library>",
    specwrite = open(os.path.join(turnin, "specifications.json"), "w")
    for i in open("specifications.json", "r").read().splitlines():
        if curr_path in i:
            i = f'"path": "{NAME} {proj_path}",'
        specwrite.write(i + '\n')
else:
    sys.stdout.write(f'no specifications.json found in {os.getcwd()}! Skipping...\n')

