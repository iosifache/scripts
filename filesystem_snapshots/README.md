# `filesystem_snapshots`

## Description 🖼️

`filesystem_snapshots` is a script for creating and comparing filesystem snapshots on Linux systems for extraction of useful information for further analysis:
- created files;
- deleted files;
- modified files, changes being detected via:
  - size;
  - MD5 hash;
  - owner's user identifier; and
  - owner's group identifier.

<a href="https://asciinema.org/a/U2BZyyL2hB5r0URlMAr6AdenX">
  <img src="https://asciinema.org/a/U2BZyyL2hB5r0URlMAr6AdenX.svg" alt="asciinema Demo" width="500"/>
</a>

## Setup 🔧

1. Install Python 3.
2. Install the required libraries: `pip3 install -r requirements.txt`.
3. Add an authorized key on the remote server to avoid the password prompting on each baseline creation (*optional*).
4. Insert a new line in the configuration file `configuration/ignored_paths.txt` for each file (for example, folders containing log files continuously changing) that needs to be ignored in the processing (*optional*).

## Usage 🧰

In the commands below, the IP address of the remote server is noted with `IP`, and the user used for login with `USER`.

1. Create a baseline snapshot: `./filesystem_snapshots.sh baseline IP USER`.
2. Create a new snapshot and compare it with the baseline one: `./filesystem_snapshots.sh compare IP USER`.