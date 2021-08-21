#!/usr/bin/env python3
import re
import sys
import warnings

import pandas

# Constants
COLUMNS_NAMES = [
    'timestamp', 'printable_date', 'uid', 'gid', 'size', 'hash', 'name'
]
DELIMITER_REGEX = r'(?<!\([0-9\-]{10})\s+'
IGNORED_PATHS_FILENAME = 'configuration/ignored_paths.txt'

# Disable all warnings
warnings.filterwarnings('ignore')

# Make pandas print long strings
pandas.set_option('display.max_colwidth', None)

# Check and get the arguments
if (len(sys.argv) != 3):
    print('[!] Usage: ./{} BASELINE_LOG_FILENAME ACTUAL_LOG_FILENAME'.format(
        sys.argv[0]))
    exit(0)
baseline_logfile = sys.argv[1]
actual_logfile = sys.argv[2]

# Read the ignored file
ignored_paths = open(IGNORED_PATHS_FILENAME, 'r').read().splitlines()
if ignored_paths:
    ignored_paths = [
        re.escape(path).replace('/', '\/') for path in ignored_paths
    ]
    ignored_paths_re = '|'.join(ignored_paths)

# Read the dataframe containing the baseline state of the filesystem
baseline_df = pandas.read_csv(baseline_logfile,
                              header=None,
                              delimiter=DELIMITER_REGEX,
                              error_bad_lines=False,
                              warn_bad_lines=False,
                              names=COLUMNS_NAMES)
if ignored_paths:
    baseline_df = baseline_df[~baseline_df['name'].str.
                              contains(ignored_paths_re)]
baseline_df['printable_date'] = baseline_df['printable_date'].str.strip('()')

# Read the dataframe containing the actual state of the filesystem
actual_df = pandas.read_csv(actual_logfile,
                            header=None,
                            delimiter=DELIMITER_REGEX,
                            error_bad_lines=False,
                            warn_bad_lines=False,
                            names=COLUMNS_NAMES)
if ignored_paths:
    actual_df = actual_df[~actual_df['name'].str.contains(ignored_paths_re)]
actual_df['printable_date'] = actual_df['printable_date'].str.strip('()')

# Get the differences between the baseline and the actual state
difference_df = baseline_df.merge(actual_df,
                                  how='outer',
                                  left_on='name',
                                  right_on='name',
                                  indicator=True,
                                  suffixes=['_baseline', '_actual'])

# Get the deleted files
deleted_df = difference_df.loc[lambda x: x['_merge'] == 'left_only']
if len(deleted_df) > 0:
    print('[+] The deleted files are: \n\n{}\n'.format(deleted_df[['name']]))

# Get the created files
created_df = difference_df.loc[lambda x: x['_merge'] == 'right_only']
if len(created_df) > 0:
    print('[+] The created files are: \n\n{}\n'.format(created_df[[
        'name', 'printable_date_actual', 'uid_actual', 'gid_actual',
        'size_actual', 'hash_actual'
    ]]))

# Get the modified files
common_df = difference_df.loc[lambda x: x['_merge'] == 'both']
different_hash_df = common_df.loc[
    lambda x: x['hash_baseline'] != x['hash_actual']]
if len(different_hash_df) > 0:
    print('[+] The files with modified content are: \n\n{}\n'.format(
        different_hash_df[[
            'name', 'hash_baseline', 'hash_actual', 'size_baseline',
            'size_actual'
        ]]))
different_uid_df = common_df.loc[
    lambda x: x['uid_baseline'] != x['uid_actual']]
if len(different_uid_df) > 0:
    print('[+] The files with changed owner are: \n\n{}\n'.format(
        different_uid_df[['name', 'uid_baseline', 'uid_actual']]))
different_gid_df = common_df.loc[
    lambda x: x['gid_baseline'] != x['gid_actual']]
if len(different_gid_df) > 0:
    print('[+] The files with changed owner group are: \n\n{}\n'.format(
        different_gid_df[['name', 'gid_baseline', 'gid_actual']]))
