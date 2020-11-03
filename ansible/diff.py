#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import re

PACKAGES = ["cmake", "meson", "gcc"]
INSTALLED = [
    "Installed: libmpc-1.1.0-8.fc32.x86_64",
    "Installed: libpkgconf-1.6.3-3.fc32.x86_64",
    "Installed: mkpasswd-5.5.6-1.fc32.x86_64",
    "Installed: binutils-2.34-4.fc32.x86_64",
    "Installed: binutils-gold-2.34-4.fc32.x86_64",
    "Installed: vim-filesystem-2:8.2.1551-1.fc32.noarch",
    "Installed: whois-nls-5.5.6-1.fc32.noarch",
    "Installed: libgomp-10.2.1-1.fc32.x86_64",
    "Installed: meson-0.55.1-1.fc32.noarch",
    "Installed: kernel-headers-5.8.6-200.fc32.x86_64",
    "Installed: isl-0.16.1-10.fc32.x86_64",
    "Installed: cmake-3.17.4-1.fc32.x86_64",
    "Installed: cmake-data-3.17.4-1.fc32.noarch",
    "Installed: rhash-1.3.8-3.fc32.x86_64",
    "Installed: cmake-filesystem-3.17.4-1.fc32.x86_64",
    "Installed: cmake-rpm-macros-3.17.4-1.fc32.noarch",
    "Installed: pkgconf-1.6.3-3.fc32.x86_64",
    "Installed: pkgconf-m4-1.6.3-3.fc32.noarch",
    "Installed: libxcrypt-4.4.17-1.fc32.x86_64",
    "Installed: pkgconf-pkg-config-1.6.3-3.fc32.x86_64",
    "Installed: libxcrypt-devel-4.4.17-1.fc32.x86_64",
    "Installed: glibc-devel-2.31-2.fc32.x86_64",
    "Installed: glibc-headers-2.31-2.fc32.x86_64",
    "Installed: elfutils-debuginfod-client-0.179-2.fc32.x86_64",
    "Installed: gcc-10.2.1-1.fc32.x86_64",
    "Installed: libuv-1:1.38.0-2.fc32.x86_64",
    "Installed: ninja-build-1.10.1-2.fc32.x86_64",
    "Installed: cpp-10.2.1-1.fc32.x86_64",
    "Installed: libgcc-10.2.1-1.fc32.x86_64",
    "Removed: libgomp-10.1.1-1.fc32.x86_64",
    "Removed: cmake-3.14.2-1.fc30.x86_64",
    "Removed: cmake-rpm-macros-3.14.2-1.fc30.noarch",
    "Removed: libgcc-10.1.1-1.fc32.x86_64",
    "Removed: libxcrypt-4.4.16-3.fc32.x86_64"
]


def main():
    for package in PACKAGES:
        reinstalled = re.compile("Installed: {0}-\\d".format(package))
        reremoved = re.compile("Removed: {0}-\\d".format(package))

        installed = list(filter(reinstalled.match, INSTALLED))
        removed = list(filter(reremoved.match, INSTALLED))
        if installed:
            print("+{0}".format(installed[0]).replace("Installed: ", ""))
        if removed:
            print("-{0}".format(removed[0]).replace("Removed: ", ""))


if __name__ == '__main__':
    main()
