#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# small script to setup a cad turnin directories
import os, sys, tkinter, json
import warnings
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showwarning
sys.path.insert(0, '/home/projects/ee476/common/scripts')  # assume check_spec is in script folder in common dir, and did not get deleted
import check_spec as cks
root = tkinter.Tk()
root.withdraw()

spec = json.loads(cks.json_minify('specifications.json'))  # take advantage of the public resource not really explicitly provided in the class

dest, src = spec["path"].split()
parts = spec["parts"]
filelst = []

# extract files info from the spec
for k, v in parts.items():
    files = list(v["files"].keys())
    if len(files) <= 1 and 'none' in files:
            continue  # assume nothing to submit
    filelst = filelst + files

turnin = os.path.join(src, dest)
os.makedirs(turnin, exist_ok=True)
missingfiles = []

for i in filelst:
    dpath, dname = os.path.split(i)  # destination dir and the file to look and copy
    parts = os.path.join(turnin, dpath)
    os.makedirs(parts, exist_ok=True)

    # lookup files
    # METHOD1: assume user used same folder names as spec json, with correct directory standard
    srcdir = os.path.join(src, 'spice', os.path.split(dpath)[-1], dname)
    if os.path.exists(srcdir):
        sys.stdout.write("[INFO]: trying to looking for default folder name\n")
        os.popen(f'cp {srcdir} {parts}/{dname}')
    elif os.path.exists(os.path.join(src, "cadence", dname)):
        # METHOD2: files are in the cadence director, with correct directory standard
        sys.stdout.write("[INFO]: no default folder found, looking into cadence directory\n")
        os.popen(f'cp {os.path.join(src, "cadence", dname)} {parts}/{dname}')
    else:
        # METHOD3: no more ways to find files, ask for an input
        filetype = os.path.splitext(dname)[-1]
        srcdir = askopenfilename(title=f'select file named "{dname}" for "{i}"',
                                 filetypes=((f"{filetype} files", f"*{filetype}"),))
        if srcdir:
            os.popen(f'cp {srcdir} {parts}/{dname}')
        else:
            warnings.warn(f'file "{dname}" not selected!')
            missingfiles.append(f'missing {dname} for {i}')

if missingfiles:
    open("missingfiles.txt", "w").write("\n".join(missingfiles))
    warnings.warn("some of your files are missing! details in 'missingfiles.txt'")
    showwarning("Missing file(s)", f'some of your files are missing! details in "missingfiles.txt" in directory "{os.getcwd()}"!')

