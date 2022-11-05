#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# small script to setup a cad assginment folder

import os, sys, tkinter, json
from tkinter.filedialog import askdirectory
root = tkinter.Tk()
root.withdraw()

NAME = "<FirstName_LastName>"  # TODO: replace this with your name
FOLDER_476 = "/home/projects/ee476"
USER = os.environ.get("USER")
CAD_FOLDER = f"/home/projects/ee476/{USER}/cadence"
if not os.path.isdir(CAD_FOLDER):
    CAD_FOLDER = askdirectory(title='Select your "cadence" Folder')
proj_path = askdirectory(title='Select CAD Folder')

sys.stdout.write(proj_path + "\n")

os.system(f'cd {proj_path} && ln -s {CAD_FOLDER}')
os.makedirs(os.path.join(proj_path, "spice"), exist_ok=True)
os.makedirs(os.path.join(proj_path, "spice", "netlists"), exist_ok=True)

# basic setup complete, now looking for specification.json, if exit in that directory
if os.path.exists("specifications.json"):
    sys.stdout.write('"specifications.json" found! creating part folders and renameing path\n')
    specfile = open("specifications.json", "r").read()
    sys.path.insert(0, '/home/projects/ee476/common/scripts')  # assume check_spec is in script folder in common dir, and did not get deleted
    import check_spec as cks
    spec = json.loads(cks.json_minify(specfile))
    curr_path = spec["path"]  # remembers what the current "path" line is written, we'll re-write that line later
    parts = spec["parts"]

    # TODO: this part assumes that the spec file always the format of 'cat#/part#/filename,  which may not exactly be the case
    # creat folders
    for k, v in parts.items():
        files = list(v["files"].keys())
        if len(files) <= 1 and 'none' in files:
            continue  # assume nothing to submit
        for i in files:
            os.makedirs(os.path.join(proj_path, "spice", i.split("/")[1]), exist_ok=True)


    # modify the spec json, assume that it has the line as this format: "path": "<Student_Name> /home/projects/ee476/<Student_ID>/<Path_To_Library>",
    specwrite = open(os.path.join(proj_path, "specifications.json"), "w")
    for i in specfile.splitlines():
        if curr_path in i:
            i = f'"path": "{NAME} {proj_path}",'
        specwrite.write(i + '\n')


