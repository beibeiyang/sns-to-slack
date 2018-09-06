# -*- coding: utf-8 -*-

'''
Follow these steps to configure the webhook in Slack:
  1. Navigate to https://<your-team-domain>.slack.com/apps, click "Build" on top right
  2. Search for and select "Incoming WebHooks".
  3. Choose the default channel where messages will be sent and click "Add Incoming WebHooks Integration".
  4. Copy the webhook URL from the setup instructions and paste it into lambda.cfg
'''

import configparser
import logging
import os
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import json


class LambdaConfig:
    """
    Class to read user-provided configurations (such as Lambda and AWS )
    from @configFile

    To initialize:
        config = LambdaConfig(configFile="PATH_TO_YOUR_CONFIG_FILE")

    To access Snowflake Database Name for example, simply call:
        config.sf_dbname
    """

    def __init__(self, configfile, logger):
        try:
            logger.info("{}{}{}".format("#" * 10, "READ LAMBDA CONFIG", "#" * 10))
            logger.info("Reading config from file: {}".format(configfile))
            cp = configparser.ConfigParser()
            cp.read(configfile)

            # read BOX FTP config
            self.slack_host = cp.get("SLACK", "hostname")
            self.slack_port = cp.get("SLACK", "port")
            self.slack_endpoint = cp.get("SLACK", "endpoint")
            self.slack_channel = cp.get("SLACK", "channel")
            self.slack_username = cp.get("SLACK", "username")
            self.slack_icon_emoji = cp.get("SLACK", "icon_emoji")

            # log BOX FTP config
            logger.info("Slack host: {}".format(self.slack_host))
            logger.info("Slack port: {}".format(self.slack_port))
            logger.info("Slack endpoint: {}".format(self.slack_endpoint))
            logger.info("Slack channel: {}".format(self.slack_channel))
            logger.info("Slack username: {}".format(self.slack_username))
            logger.info("Slack icon emoji: {}".format(self.slack_icon_emoji))

            logger.info("#" * 30)

        except Exception as e:
            logger.exception("Error parsing the user-provided config file. Script will terminate. {}".format(repr(e)))
            sys.exit(-1)


def handler(event, context):
    # Set logging level
    log_level = os.environ.get('LOG_LEVEL', 'DEBUG').upper()
    logger = logging.getLogger()
    logger.setLevel(log_level)
    config = LambdaConfig(configfile="lambda.cfg", logger=logger)

    logger.debug("Received event: {}".format(event))
    logger.info("{} SNS to Slack process starts {}".format("*" * 10, "*" * 10))

    try:
        message = event["Records"][0]["Sns"]["Message"]
        logger.info("From SNS: {}".format(message))
    except TypeError as e:
        logger.exception("Unable to retrieve message from event", repr(e))
        return

    post_data = {
        "channel": config.slack_channel,
        "username": config.slack_username,
        "text": "*{}*".format(event["Records"][0]["Sns"]["Subject"]),
        "icon_emoji": config.slack_icon_emoji
    }

    # SNS message body must start with ERROR, WARNING or SUCCESS
    if message.startswith("ERROR"):
        severity = "danger"
    elif message.startswith("WARNING"):
        severity = "warning"
    else:
        severity = "good"

    post_data["attachments"] = [
        {
            "color": severity,
            "text": message
        }
    ]

    hook_url = "https://{}:{}{}".format(config.slack_host, config.slack_port,
                                        config.slack_endpoint)
    logger.info("Slack Hook URL: {}".format(hook_url))

    logger.info("post_data: {}".format(post_data))

    try:
        data = json.dumps(post_data).encode("utf-8")
        req = Request(hook_url, data=data, method="POST")

        req.add_header(
            "Content-Type",
            "application/x-www-form-urlencoded"
        )

        logger.debug("data: {}".format(data))
        response = urlopen(req)
        logger.info("Message posted to channel {}".format(config.slack_channel))
        logger.info("Response: {}".format(response.read()))
    except HTTPError as e:
        logger.exception("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.exception("Server connection failed: %s", e.reason)
    except Exception as e:
        logger.exception("Unknown exception: %s", repr(e))
