#!/usr/bin/env python
# coding: utf-8
#
# Copyright (c) 2017, Roman Miroshnychenko <romanvm@yandex.ua>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""
Script for generating xml and md5 files for a custom Kodi addons repository

It should work with both Python 2 and 3
"""
from __future__ import print_function

import hashlib
import os
import xml.dom.minidom as dom

this_dir = os.path.dirname(os.path.abspath(__file__))


def get_addon_dirs():
    for item in os.listdir(this_dir):
        full_path = os.path.join(this_dir, item)
        if os.path.isdir(full_path):
            yield full_path


def generate_addons_xml(dirs):
    doc = dom.Document()
    root = doc.createElement('addons')
    doc.appendChild(root)
    for item in dirs:
        addon_xml = os.path.join(item, 'addon.xml')
        if os.path.exists(addon_xml):
            xml = dom.parse(addon_xml)
            root.appendChild(xml.firstChild)
    contents = doc.toprettyxml(newl='', encoding='utf-8')
    with open('addons.xml', 'wb') as fo:
        fo.write(contents)
    with open('addons.xml.md5', 'w') as fo:
        fo.write(hashlib.md5(contents).hexdigest())


def generate_zip_md5s(dirs):
    for dir_item in dirs:
        for item in os.listdir(dir_item):
            if os.path.splitext(item)[1].lower() == '.zip':
                zip_file = os.path.join(dir_item, item)
                with open(zip_file, 'rb') as fo:
                    zip_contents = fo.read()
                with open(zip_file + '.md5', 'w') as fo:
                    fo.write(hashlib.md5(zip_contents).hexdigest())


def main():
    addon_dirs = list(get_addon_dirs())
    print('Generating addons.xml and md5...')
    generate_addons_xml(addon_dirs)
    print('Generating md5 for individual ZIPs...')
    generate_zip_md5s(addon_dirs)
    print('Repository updated successfully.')


if __name__ == '__main__':
    main()
