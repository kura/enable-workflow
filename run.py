#!/usr/bin/python3
from os import getenv
from sys import exit
from time import sleep

from github import Github
from requests import put


repos = ("kura/vaultwarden", "kura/uptime-kuma")


pat = getenv("PERSONAL_ACCESS_TOKEN", None)
if not pat:
    print("Missing PERSONAL_ACCESS_TOKEN")
    exit(1)


def run():
    gh = Github(login_or_token=pat)
    print("Running workflow updater")

    for repo in repos:
        gh_repo = gh.get_repo(repo)
        print(f"Running for {gh_repo.full_name}")
        workflows = [workflow for workflow in gh_repo.get_workflows()]
        workflow, = workflows
        if workflow.state != "disabled_inactivity":
            print("Workflow is not disabled, skipping")
        else:
            print("Updating workflow")
            url = f"{workflow.url}/enable"
            headers = {"Authorization": f"Bearer {pat}"}
            put(url, headers=headers)

while True:
    run()
    print("Sleeping")
    sleep(3600)
