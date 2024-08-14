#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2024 Enrique Maravilla
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.


import datetime
import logging
import typing
import argparse
import os
import yaml
import msvcrt as m


class Logbook:

    def __init__(self):
        self.parser = self.build()
        self.cwd = os.getcwd()
        self.args = None
        self.uwd = None
        self.config_set = False
        self.user = None
        self.classes = []

    def forward(self) -> None:

        if not self.config_set:
            self.run_setup()
            self.wait()
            self.show_help()
        else:
            pass
        self.args = self.parser.parse_args()

    @staticmethod
    def valid_path(path) -> bool:
        return os.path.exists(path)

    @staticmethod
    def wait() -> None:
        m.getche()

    def get_config(self) -> yaml:
        try:
            with open('config.yml', 'r') as file:
                config = yaml.safe_load(file)

        except FileNotFoundError as e:
            print(e.strerror + ": " + e.filename)
            print("\nWould you like to run first-time setup ? [Y/n]")
            up = self.get_yesno()
            if up:
                config = self.user_run_setup()
            if not up:
                print(logging.warning(msg="Exiting without performing setup."))
                exit(2)

        return config

    def user_run_setup(self) -> yaml:
        print("Performing first time setup..")
        name = input("Input your name (used for headers)\n")
        classes = []
        rein = True
        while rein:
            group = input("Input your class\nExample: 6A, or 6A Coding\n")
            classes.append(group)
            print("Enter another class ? [Y/n]")
            rein = self.get_yesno()

            with open('config.yaml', 'w') as file:
                yaml.dump(classes, file)

        return None

    def get_yesno(self) -> bool:
        ans = m.getche()
        if ans == b"y" or ans == b"Y":
            return True
        if ans == b"n" or ans == b"N":
            return False
        else:
            print("Invalid input detected.\n[Y/n]?")
            self.get_yesno()

    def run_setup(self) -> None:
        config = self.get_config()
        pass

    def build(self) -> argparse.ArgumentParser:

        parser = argparse.ArgumentParser(description="Log creation toolkit")
        parser.add_argument("--setup")
        parser.add_argument("-o", "--open", type=str, nargs=1,
                            metavar="file_name", default=None,
                            help="Manually open the specified log file.\n"
                                 "usage: --open [filename]")
        parser.add_argument("-s", "--save", type=str, nargs=1,
                            default=None,
                            help="Manually save file.\n"
                                 "Everything Logbook automatically saves every 10 minutes.\n"
                                 "usage: --save [filename]")
        parser.add_argument("-r", "--rename", type=str, nargs=2,
                            metavar="file_name", default=None,
                            help="Renames the specified log file to provided name.\n"
                                 "usage: --rename [filename](default current) [newname]")
        parser.add_argument("-d", "--delete", type=str, nargs=1,
                            metavar="file_name", default=None,
                            help="Deletes the specified log file. Use with care.\n"
                                 "usage: --delete [filename]")
        parser.add_argument("-g", "--groups",  action="store_const", const=True,
                            default=None,
                            help="List registered groups for your user.\n")
        parser.add_argument("-l", "--list",  action="store_const", const=True,
                            default=None,
                            help="List files in current working directory.\n")
        parser.add_argument("-v", "--verbose", action="store_true")
        parser.add_argument("-q", "--quiet", action="store_true")
        parser.add_argument("-e", "--export")

        return parser

    def show_help(self) -> None:
        self.parser.print_help()


def welcome() -> None:
    print("ITJ Everything Logbook v0.1\n")
    print(" (\\ ")
    print(" \\ '\\ ")
    print("  \\ '\\     __________  ")
    print("  / '|   ()_________)")
    print("  \\ '/    \\ ~~~~~~~~ \\ ")
    print("   \\       \\ ~~~~~~   \\ ")
    print("   ==).      \\__________\\ ")
    print("  (__)       ()__________)")
    print("\nMade by Enrique Maravilla 2024")
    print("\nThis program is free software under the")
    print("GNU General Public License v3.0")
    print("see <https://www.gnu.org/licenses/gpl-3.0.en.html> for more information.\n\n")


if __name__ == '__main__':
    welcome()
    active_book = Logbook()
    active_book.forward()
