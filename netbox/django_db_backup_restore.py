#!/usr/bin/env python


import argparse
import datetime
import os
import sys
import tempfile
from pathlib import Path
from subprocess import call, check_call, CalledProcessError

from django.conf import settings

# from my_project.my_app.utils import MyCustomError


# global variables
# work on a copy ENV in-case I can't or don't want to change global settings
ENV = os.environ.copy()
TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
# TODO: Perhaps refactor and read from the manage.py file to determine this next environ line?
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "netbox.settings")
# rel = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
# BACKUP_DIR = rel('backups/')
BACKUP_DIR = Path(__file__).resolve(strict=True).parent.parent




def perform_backup(db_backend):
        # figure out the cmds for backing up the specific db...

    if 'postgres' in db_backend:

        print("backing up a postgres db...")

        backup_file = os.path.join(BACKUP_DIR, "backup_{0}_{1}.sql.tgz".format(db_conf.get("NAME"), TIMESTAMP))
        backup_cmd = "/usr/bin/pg_dump"

        # note the use of "-O" which does not constrain table ownership
        # however, the docs of pg_dump state:
        #  <snip>
        #  This option is only meaningful for the plain-text format.
        #  For the archive formats, you can specify the option when you call pg_restore.
        #  </snip>

        # HOST =

        backup_args = [
            "-Ft",
            "-v",
            "-b",
            "-c",
            "-O",
            "-h{0}".format(db_conf.get("HOST")),
            "-p{0}".format(db_conf.get("PORT")),
            "-U{0}".format(db_conf.get("USER")),
            "-w",
            "-f{0}".format(backup_file),
            db_conf.get("NAME"),
        ]

        # Bypass manually inputting the pwd by using '-w' flag
        # w/ an ENV variable
        ENV["PGPASSWORD"] = db_conf.get("PASSWORD")

    elif "sqlite" in db_backend:
        print("backing up a sqlite db...")
        msg = "you don't need a fancy script to backup sqlite; just copy the file"
        # raise MyCustomError(msg)
        sys.exit(1)

    elif "mysql" in db_backend:
        print("backing up a mysql db...")
        msg = "this script cannot handle mysql yet"
        # raise MyCustomError(msg)
        sys.exit(1)

    else:
        msg = "unknown db backend: '{0}'".format(db_backend)
        # raise MyCustomError(msg)
        sys.exit(1)

    backup_args.insert(0, backup_cmd)

    # open the logfile and perform the backup

    with open(os.path.join(BACKUP_DIR, "log.txt"), 'a') as log_file:
        try:
            check_call(backup_args, env=ENV)
            msg = "successfully created '{0}'".format(backup_file)
            print(msg)
            log_file.write(TIMESTAMP + ": " + msg)
        except OSError:
            msg = "unable to find {0}".format(backup_cmd)
            # raise MyCustomError(msg)
            sys.exit(1)
        except CalledProcessError as e:
            msg = "error creating '{0}'".format(backup_file)
            print(msg)
            log_file.write(TIMESTAMP + ": " + msg)

    # clean up
    log_file.closed

    # hooray, you're done
    print("[*] Backup operation complete")
    return


def perform_restore(db_backend, restore_file):
    """ From provided restore_file, attempt to restore data into database. """

    if 'postgres' in db_backend:
        print("Restoring postgres db from backup file")

        restore_cmd = "/usr/bin/pg_restore"

        # pg_restore may fail when trying to re-create the _entire_ db b/c of issues
        # w/ "plpgsql" tables. This is a known issue:
        # - [http://www.postgresql.org/message-id/201110220712.30886.adrian.klaver@gmail.com]
        #
        # To fix it, remove the offending lines from the db dump as follows:
        # `pg_restore -l $BACKUP_FILE | grep -vi plpgsql > $TMPFILE`
        # and then run the same restore command as below w/ the addition of "-L $TMPFILE"
        #
        # Technically, this is a bad solution b/c of the "shell=True" argument
        # so, perhaps we should just ignore the errors (by never including the "-e" flag)
        (tmpfile, tmpfile_path) = tempfile.mkstemp(dir=os.getcwd())
        call(
            "{0} -l {1} | grep -vi plpgsql > {2}".format(restore_cmd, restore_file, tmpfile_path),
            shell=True
        )

        # Note the use of "-O" which does not try to match ownership of the original backed-up db
        # However, "-U -W" ensures users still must be authenticated against the db being changed
        restore_args = [
            "-c",
            "-v",
            "-L{0}".format(tmpfile_path),
            "-d{0}".format(db_conf.get("NAME")),
            "-O",
            "-h{0}".format(db_conf.get("HOST")),
            "-p{0}".format(db_conf.get("PORT")),
            "-U{0}".format(db_conf.get("USER")),
            "-W",
            restore_file,
        ]

    elif "sqlite" in db_backend:
        # print("restoring a sqlite db...")
        msg = "you don't need a fancy script to restore sqlite; just copy the file"
        print(msg)
        # raise MyCustomError(msg)
        sys.exit(1)

    elif "mysql" in db_backend:
        # print("restoring a mysql db...")
        msg = "this script cannot handle mysql yet"
        print(msg)
        # raise MyCustomError(msg)
        sys.exit(1)

    else:
        msg = "Unknown db backend: '{0}'".format(db_backend)
        print(msg)
        # raise MyCustomError(msg)
        sys.exit(1)

    restore_args.insert(0, restore_cmd)

    # perform the actual restore
    try:
        # note, unlike the db_backup script, I do not pass an "env" argument b/c I do not
        # have to deal w/ sensitive passwords b/c this script is meant to be run interactively
        check_call(restore_args)
        msg = "successfully restored '{0}".format(restore_file)
        print(msg)
    except OSError as e:
        msg = "unable to find {0} -- Error: {1}".format(restore_cmd, e)
        print(msg)
        # raise MyCustomError(msg)
        sys.exit(1)
    except CalledProcessError as e:
        msg = "error restoring '{0}'".format(restore_file)
        print(msg)
        sys.exit(1)

    # clean up the filesystem, just in-case
    try:
        os.unlink(tmpfile_path)
    except:
        pass

    print("[*] End of restore operation")
    return





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Utility to backup or restore a django database")
    parser.add_argument('mode', help='Specify mode, backup or restore')
    parser.add_argument('-f', '--restore-file', required=False,
                        help='backup file to restore')
    args = parser.parse_args()

    # get db details
    # sys.path.insert(0, )
    # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'netbox')))
    try:
        db_conf = settings.DATABASES["default"]
    except ModuleNotFoundError:
        pass
    except KeyError:
        msg = "unable to find valid database configuration"
        # raise MyCustomError(msg)
        sys.exit(1)

    db_backend = db_conf.get("ENGINE")


    if args.mode == 'backup':
        perform_backup(db_backend)

    elif args.mode == 'restore':
        if not args.restore_file:
            parser.print_usage()
            sys.exit(1)
        restore_file = args.restore_file
        if not os.path.isfile(restore_file):
            msg = "unable to locate '{0}'".format(restore_file)
            # raise MyCustomError(msg)
            sys.exit(1)

        perform_restore(db_backend, restore_file)

    else:
        print("[ERR] You didn't pass a valid mode, must be 'backup' or 'restore'")
        sys.exit(1)
