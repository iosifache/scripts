# `checkmk_alert`

## Description 🖼️

`checkmk_alert` is a system for sending alerting emails via a local SMTP server when an anomaly is observed into the Checkmk's dashboard with servers statuses. In this context, an anomaly consists in an exceeding of a set threshold by the number of down hosts (considering only the ones mentioned in a list of relevant or all not mentioned in a list of ignored ones).

## Setup 🔧

1. Install Python 3.
2. Install the required libraries: `pip3 install -r requirements.txt`.
3. Set up an SMTP server. For Postfix on CentOS, check this [tutorial](https://netcorecloud.com/tutorials/install-centos-postfix/).
4. Set up the forwarding of the emails via Gmail's SMTP server. You can follow [this](https://tonyteaches.tech/postfix-gmail-smtp-on-ubuntu/) tutorial.
5. Modify the YAML configuration file with a text editor, filling out the details about your Checkmk instance and about alerting.
6. Install the alerting script by running the commands below.

    ```
    chmod +x setup.sh
    ./setup.sh
    ```