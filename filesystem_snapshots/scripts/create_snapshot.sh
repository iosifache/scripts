#!/bin/bash
#
# Script for listing information about all files found in the filesystem

# The stored information are:
# - last status change time, in seconds since 01.01.1970 00:00 GMT and
# in the "YYYY-MM-DD HH:MM:SS.MMMM" format;
# - owner's user ID;
# - owner's group ID;
# - file size in bytes;
# - MD5 hash; and
# - filename.
find / -xdev -type f -printf "%C@ (%CY-%Cm-%Cd %CT) %U %G %s "\
 -exec md5sum {} \;