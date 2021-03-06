#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

__author__ = "Benjamin Feder"

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """

    puzzle_urls = []  # create empty list for puzzle URLS to go into
    server_name = "https://" + filename.split("_")[1]  # find server name from
    # filename

    with open(filename, "r") as puzzle_file:
        """
        Read each line in the file and
        append the image URL to the list of puzzle URLs, each preceded by
        the server name from the filename to get an accurate list of URLs
        """
        pattern = r"\S+puzzle+\S+"
        for line in puzzle_file:
            url_path_find = re.search(pattern, line)  # find where
            if url_path_find:
                path = url_path_find.group()
                puzzle_urls.append(server_name + path)

        unique_urls = {}  # create dict to determine unique urls

        for url in puzzle_urls:
            unique_urls[url] = url

        sorted_urls = sorted(unique_urls, key=lambda u: u[-8:])

        return sorted_urls


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    with open(f"{dest_dir}/index.html", "w") as web_file:
        web_file.write("<html><body>")

        for i, url in enumerate(img_urls):
            filename = f"{dest_dir}/img{i}"
            urllib.request.urlretrieve(url, filename=filename)
            web_file.write(f'<img src="img{i}">')

        web_file.write("</body></html>")


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
