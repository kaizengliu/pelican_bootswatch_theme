# -*-coding: utf-8-*-
# author: liukaizeng

import os
import sys
import argparse

from shutil import copy2, Error, copystat, WindowsError


def get_theme_directory(args):
    parser = argparse.ArgumentParser(description="pelican theme install", add_help=True)

    parser.add_argument('-t', dest="theme", help="theme directory")

    cmd_args = parser.parse_args(args)

    theme_directory = cmd_args.theme

    if not os.path.isdir(theme_directory):
        raise "theme directory doesn't exist"

    return cmd_args.theme


def install_theme(theme_directory):
    try:
        import pelican
    except ImportError:
        raise "Please install pelican first, example: pip install peclian"

    sep = os.sep

    theme_directory = theme_directory.rstrip(sep)
    theme_name = theme_directory.split(sep)[-1]

    pelican_path = pelican.__path__[0].rstrip(sep)

    theme_path = sep.join([pelican_path, "themes", theme_name])

    copytree(theme_directory, theme_path)

def copytree(src, dst, symlinks=False, ignore=None):
    """
     复制一个文件夹内到所有文件到目标路径
    """

    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    if not os.path.exists(dst):
        os.makedirs(dst)

    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error as err:
            errors.extend(err.args[0])
    try:
        copystat(src, dst)
    except WindowsError:
        # can't copy file access times on Windows
        pass
    except OSError as why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise Error(errors)


def main():
    theme_directory = get_theme_directory(sys.argv[1:])
    install_theme(theme_directory)


if '__main__' == __name__:
    main()