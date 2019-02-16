# -*- coding: utf-8 -*-

import os
import sys
import re
import urllib


def persist_md(md_file_path, output_dir, new_img_prefix):
    url_downloader = urllib.URLopener()
    change = False
    md_lines = []
    with open(md_file_path, 'r') as md_file:
        md_lines = md_file.readlines()
        for i in range(0, len(md_lines)):
            md_line = md_lines[i]
            match_obj = re.match(r'(!\[(\w*)\]\((http.*/(.*\.(\w+)))\))', md_line)
            if match_obj:
                origin_img = match_obj.group(1)
                img_tag = match_obj.group(2)
                origin_img_url = match_obj.group(3)
                origin_img_name = match_obj.group(4)
                print(img_tag)
                print(origin_img)
                print(origin_img_url)
                print(origin_img_name)
                new_img_file_name = "new-" + "-" + origin_img_name;
                url_downloader.retrieve(origin_img_url, output_dir + "/" + new_img_file_name)
                new_img = "![" + img_tag + "](" + new_img_prefix + new_img_file_name + ")"
                md_line = md_line.replace(origin_img, new_img)
                md_lines[i] = md_line
                change = True
    if change:
        with open(md_file_path, 'w') as md_file_write:
            md_file_write.writelines(md_lines)
            md_file_write.flush()


def main():
    search_dir = sys.argv[1]
    img_output_dir = sys.argv[2]
    new_img_prefix = sys.argv[3]
    for root, dirs, files in os.walk(search_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = (os.path.join(root, file))
                persist_md(md_file_path=file_path, output_dir=img_output_dir, new_img_prefix=new_img_prefix)


if __name__ == "__main__":
    main()
