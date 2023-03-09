#!/usr/bin/python3
import logging
from os import getenv
from sys import exit
from time import sleep

from github import Github
from requests import put


logger = logging.getLogger("enable-workflow")
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


repos = ("kura/vaultwarden", "kura/uptime-kuma")


pat = getenv("PERSONAL_ACCESS_TOKEN", None)
if not pat:
    logger.error("Missing PERSONAL_ACCESS_TOKEN")
    exit(1)


def run():
    gh = Github(login_or_token=pat)
    logger.info("Running workflow updater")

    for repo in repos:
        gh_repo = gh.get_repo(repo)
        logger.info(f"Running for {gh_repo.full_name}")
        workflows = [workflow for workflow in gh_repo.get_workflows()]
        workflow, = workflows
        if workflow.state != "disabled_inactivity":
            logger.info("Workflow is not disabled, skipping")
        else:
            logger.info("Updating workflow")
            url = f"{workflow.url}/enable"
            headers = {"Authorization": f"Bearer {pat}"}
            put(url, headers=headers)


if __name__ == "__main__":
    while True:
        run()
        logger.info("Sleeping")
        sleep(3600)
