#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# small script to setup a cad assginment folder

import os, sys, tkinter, json, base64
from tkinter.filedialog import askdirectory
from tkinter import simpledialog
root = tkinter.Tk()
root.withdraw()

NAME = simpledialog.askstring(title="What's Your Name", prompt="Please enter your full name, with space in between first and last name (First Second):").replace(" ", "_")
sys.stdout.write(f'Turnin name set to {NAME}\n')
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
    sys.path.insert(0, '/home/projects/ee476/common/scripts')  # assume check_spec is in script folder in common dir, and did not get deleted
    import check_spec as cks
    spec = json.loads(cks.json_minify("specifications.json"))
    curr_path = spec["path"]  # remembers what the current "path" line is written, we'll re-write that line later
    parts = spec["parts"]
    make = b'Q09NTU9OX0RJUiA9IC9ob21lL3Byb2plY3RzL2VlNDc2LjIwMjJhdXQvY29tbW9uCkRFU0lHTl9ESVIgPSAvaG9tZS9wcm9qZWN0cy9lZTQ3Ni4yMDIyYXV0LyQoVVNFUikKTkVUTElTVF9ESVIgPSAkKHNoZWxsIHJlYWxwYXRoIC4uL25ldGxpc3RzKQpYTkVUTElTVCA9ICR7Q09NTU9OX0RJUn0vc2NyaXB0cy94bmV0bGlzdC5weQpTUElDRVNFVFVQID0gJHtDT01NT05fRElSfS9zY3JpcHRzL3NwaWNlU2V0dXAucHkKR0VORVJBVEVNRUFTVEFCTEUgPSAke0NPTU1PTl9ESVJ9L3NjcmlwdHMvZ2VuZXJhdGVNZWFzVGFibGUucHkKU1RETElCU0VUVVAgPSAke0NPTU1PTl9ESVJ9L3NjcmlwdHMvc3Rkc2V0dXAucHkKSFNQSUNFID0gaHNwaWNlIC1tdCAyIC1ocHAKCgphbGw6IGhzcGljZQoKJChERVNJR04pLmNrdDokKERFU0lHTl9ESVIpLyQoREVTSUdOX0xJQikvJChERVNJR04pL3NjaGVtYXRpYy9zY2gub2EKCSQoWE5FVExJU1QpIC1sICQoREVTSUdOX0xJQikgLWMgJChERVNJR04pIC12IHNjaGVtYXRpYyAtZCAkKERFU0lHTl9ESVIpL2NhZGVuY2UgLW4gJChORVRMSVNUX0RJUikgIy0tdG9wc3ViCgkkKFNQSUNFU0VUVVApIC1pICQoTkVUTElTVF9ESVIpLyQoREVTSUdOKS9oc3BpY2VEL3NjaGVtYXRpYy9uZXRsaXN0L2lucHV0LmNrdCAtbyAkKERFU0lHTikuY2t0CgpuZXRsaXN0OiQoREVTSUdOX0RJUikvJChERVNJR05fTElCKS8kKERFU0lHTikvc2NoZW1hdGljL3NjaC5vYQoJJChYTkVUTElTVCkgLWwgJChERVNJR05fTElCKSAtYyAkKERFU0lHTikgLXYgc2NoZW1hdGljIC1kICQoREVTSUdOX0RJUikvY2FkZW5jZSAtbiAkKE5FVExJU1RfRElSKSAjLS10b3BzdWIKCSQoU1BJQ0VTRVRVUCkgLWkgJChORVRMSVNUX0RJUikvJChERVNJR04pL2hzcGljZUQvc2NoZW1hdGljL25ldGxpc3QvaW5wdXQuY2t0IC1vICQoREVTSUdOKS5ja3QKCmhzcGljZTogJChERVNJR04pLmN0bCAkKERFU0lHTikuY2t0CgkkKFNURExJQlNFVFVQKSAtYyAkKERFU0lHTikuY3RsIC1iIDAgLWwgJChDT01NT05fRElSKS9jYWRlbmNlX3NldHVwL2ZyZWVwZGs0NS5sIC0tY29ybmVyIHR0X2xpYgoJaHNwaWNlICQoREVTSUdOKS5jdGwgLW8gJChERVNJR04pLmxpcwoJLSQoR0VORVJBVEVNRUFTVEFCTEUpIC1pICQoREVTSUdOKS5tdDAgLW8gJChERVNJR04pX21lYXMuY3N2IC12IHInKicKCS0kKEdFTkVSQVRFTUVBU1RBQkxFKSAtaSAkKERFU0lHTikubXMwIC1vICQoREVTSUdOKV9tZWFzLmNzdiAtdiByJyonCgpsYXlvdXQ6JChERVNJR05fRElSKS8kKERFU0lHTl9MSUIpLyQoREVTSUdOKS9sYXlvdXQvbGF5b3V0Lm9hCgkkKFhORVRMSVNUKSAtbCAkKERFU0lHTl9MSUIpIC1jICQoREVTSUdOKSAtdiBsYXlvdXQgLWQgJChERVNJR05fRElSKS9jYWRlbmNlIC1uICQoTkVUTElTVF9ESVIpIC0tdG9wc3ViCgkkKFNQSUNFU0VUVVApIC1pICQoTkVUTElTVF9ESVIpLyQoREVTSUdOKS9oc3BpY2VEL2xheW91dC9uZXRsaXN0L2lucHV0LmNrdCAtbyAkKERFU0lHTikuY2t0CglsbiAtc2YgJChERVNJR05fRElSKS9jYWRlbmNlLyQoREVTSUdOKS5kcmMuc3VtbWFyeQoJbG4gLXNmICQoREVTSUdOX0RJUikvY2FkZW5jZS8kKERFU0lHTikubHZzLnJlcG9ydAoJbG4gLXNmICQoREVTSUdOX0RJUikvY2FkZW5jZS8kKERFU0lHTikucGV4Lm5ldGxpc3QKCWxuIC1zZiAkKERFU0lHTl9ESVIpL2NhZGVuY2UvJChERVNJR04pLnBleC5uZXRsaXN0LnBleAoJbG4gLXNmICQoREVTSUdOX0RJUikvY2FkZW5jZS8kKERFU0lHTikucGV4Lm5ldGxpc3QuJChzaGVsbCBYPSIke0RFU0lHTn0iOyBlY2hvICQke1heXn0pLnB4aQoKY2xlYW46CglybSAtcmYgJChERVNJR04pLmNrdAoJcm0gLXJmICQoREVTSUdOKS5ja3QKCXJtIC1yZiAkKERFU0lHTikucyoKCXJtIC1yZiBzeCoKCXJtIC1yZiAkKERFU0lHTikubGlzCglybSAtcmYgJChERVNJR04pLiowCglybSAtcmYgJChERVNJR04pX21lYXMuY3N2CglybSAtcmYgbG9nRmlsZQoJcm0gLXJmIHN0ZExpYnMuY3RsCglybSAtcmYgZnJlZXBkazQ1LmwKCXJtIC1yZiAqLnN1bW1hcnkKCXJtIC1yZiAqLnJlcG9ydAoJcm0gLXJmICoucGV4LioK'

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
                open(os.path.join(spicedir, f'{ctl.replace(".ckt", "")}.ctl'), "w").write(f'*\n.INCLUDE "{ctl}"')
                # generate makefile
                makefile = open(os.path.join(spicedir, "Makefile"), "wb")
                makefile.write(f'DESIGN_LIB ?= {os.path.split(proj_path)[-1]}\nDESIGN ?= {ctl.replace(".ckt", "")}\n'.encode('utf-8'))
                makefile.write(base64.b64decode(make))


    # preload turnin folder
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


