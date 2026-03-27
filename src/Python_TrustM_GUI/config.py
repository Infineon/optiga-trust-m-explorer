# SPDX-FileCopyrightText: 2025 Infineon Technologies AG
#
# SPDX-License-Identifier: MIT

import os


def find_bin_directory(start_path):
    for root, dirs, files in os.walk(start_path):
        if "bin" in dirs:
            return os.path.basename(root)
    return None


# Get the current directory where the script (config.py) is located
current_directory = os.path.dirname(os.path.realpath(__file__))

dirname = find_bin_directory(current_directory)
EXEPATH = os.path.dirname(os.path.realpath(__file__)) + "/" + dirname
CERT_PATH = EXEPATH + "/scripts/certificates"
IMAGEPATH = os.path.dirname(os.path.realpath(__file__))
