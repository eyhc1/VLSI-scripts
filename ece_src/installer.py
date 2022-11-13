#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys

if len(sys.argv) < 3 or "install" not in sys.argv:
    sys.stdout.write('Usage: installer install <package name> (optional) install_only\n')
    sys.exit(0)

PACKAGE_NAME = sys.argv[2]
file_dir = PACKAGE_NAME
os.makedirs(file_dir, exist_ok=True)

os.system(f'cd {file_dir} && yumdownloader --resolve {PACKAGE_NAME}\n')
if 'install_only' in sys.argv:
    sys.exit(0)
files = os.listdir(file_dir)
for i in files:
    if i.endswith(".rpm"):
        os.system(f'cd {file_dir} && rpm2cpio {i} | cpio -idv\n')
        os.unlink(os.path.join(file_dir, i))
