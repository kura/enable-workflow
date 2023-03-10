#!/usr/bin/python3
import json
import logging
from os import getenv
from sys import exit
from time import sleep

from github import Github
from requests import put


logger = logging.getLogger("enable-workflow")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s  %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


repos = getenv("REPOS", None)
if repos:
    repos = [r.strip() for r in repos.split(",")]
else:
    logger.error("Missing REPOS")
    exit(1)


pat = getenv("PERSONAL_ACCESS_TOKEN", None)
if not pat:
    logger.error("Missing PERSONAL_ACCESS_TOKEN")
    exit(1)


def run():
    gh = Github(login_or_token=pat)

    for repo in repos:
        gh_repo = gh.get_repo(repo)
        for workflow in gh_repo.get_workflows():
            if workflow.state != "disabled_inactivity":
                logger.info(
                    f"Skipping '{workflow.name}' on '{gh_repo.full_name}' because it's still active"
                )
            else:
                url = f"{workflow.url}/enable"
                headers = {"Authorization": f"Bearer {pat}"}
                r = put(url, headers=headers)
                if r.status_code >= 200 and r.status_code <= 299:
                    logger.info(f"Enabled '{workflow.name}' on '{gh_repo.full_name}'")
                else:
                    logger.error(
                        f"""Failed to enable '{workflow.name}' on '{gh_repo.full_name}': """
                        f"""{json.loads(r.text)["message"]}"""
                    )


if __name__ == "__main__":
    while True:
        run()
        sleep_time = getenv("SLEEP", 3600)
        logger.info(f"Sleeping for {sleep_time}")
        sleep(sleep_time)
