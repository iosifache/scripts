#!/usr/bin/env python3
"""Script for monitoring Checkmk and sending emails when an anomaly is detected.

This is used by the cronjob set up by the installation script.
"""

import logging
import os
import typing
from enum import Enum

import requests
import yaml

# Constants
CONFIGURATION_FULL_NAME = "/opt/checkmk_alert/configuration.yaml"
LOCK_FULL_FILENAME = "/tmp/.checkmk-alert-lock"


class State(Enum):
    DOWN = "DOWN"
    UP = "UP"
    OTHER = "OTHER"


def logging_setup() -> None:
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')


def read_configuration(filename: str) -> typing.Any:
    with open(filename, "r") as stream:
        try:
            logging.info("Configuration was loaded.")

            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.critical("Could not load the configuration.")

            return None


def get_data(checkmk_api_url, checkmk_username,
             checkmk_secret) -> typing.List[typing.List]:
    # Build the API URL
    formatted_url = checkmk_api_url.format(username=checkmk_username,
                                           secret=checkmk_secret)

    # Get the data
    data = requests.get(formatted_url)
    data = data.json()[1:]

    # Get and convert the states of the hosts
    for host in data:
        state = host[0]
        host[0] = State[state] if hasattr(State, state) else State.OTHER

    return data


def mail_person(template: str, name: str, email: str, count: int,
                threshold: int, names: typing.List[str]) -> None:
    # Create the HTML list items
    name_items = ["<li>{}</li>".format(name) for name in names]
    name_items = "".join(name_items)

    # Send the mail
    message = template.format(name=name,
                              email=email,
                              count=count,
                              threshold=threshold,
                              name_items=name_items)
    command = "echo '{}' | /usr/sbin/sendmail -t".format(message)
    os.system(command)

    logging.info("{} was alerted via email.".format(name))


def main() -> None:
    # Set up the logging
    logging_setup()

    # Get the configuration
    configuration = read_configuration(CONFIGURATION_FULL_NAME)
    checkmk_api_url = configuration["checkmk"]["api_url"]
    checkmk_username = configuration["checkmk"]["username"]
    checkmk_secret = configuration["checkmk"]["secret"]
    mail_template = configuration["alerting"]["template"]
    mailing_list = configuration["alerting"]["mailing_list"]
    relevant_hosts = configuration["alerting"]["relevant_hosts"]
    ignored_hosts = configuration["alerting"]["ignored_hosts"]
    down_hosts_threshold = configuration["alerting"]["down_hosts_threshold"]

    # Get the data
    data = get_data(checkmk_api_url, checkmk_username, checkmk_secret)

    # Get the states
    down_hosts = [
        host for host in data if ((host[0] == State.DOWN) and (
            host[1] not in ignored_hosts) and (host[1] in relevant_hosts))
    ]

    # Detect if an alert is needed
    down_hosts_count = len(down_hosts)
    lock_exists = os.path.isfile(LOCK_FULL_FILENAME)
    if ((down_hosts_count >= down_hosts_threshold) and not lock_exists):
        # Create the lock file
        open(LOCK_FULL_FILENAME, "w").close()

        host_names = [hosts[1] for hosts in down_hosts]

        for receiver in mailing_list:
            mail_person(mail_template, receiver[0], receiver[1],
                        down_hosts_count, down_hosts_threshold, host_names)
    elif ((down_hosts_count < down_hosts_threshold) and lock_exists):
        # Remove the lock file
        os.remove(LOCK_FULL_FILENAME)

        logging.info("The lock file was deleted due "
                     "to the decrease of the number of down hosts.")
    else:
        logging.info("No action was taken.")


if __name__ == "__main__":
    main()
