import os
import re
import json
import requests

GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

LABEL_PATTERN = re.compile(r"(\d{4})-R(\d+)")

def get_all_issues():
    issues = []
    page = 1
    while True:
        response = requests.get(API_URL, headers=HEADERS, params={"state": "all", "per_page": 100, "page": page})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch issues: {response.status_code} - {response.text}")
        page_issues = response.json()
        if not page_issues:
            break
        issues.extend(page_issues)
        page += 1
    return issues


def parse_issue(issue):
    label_info = next((LABEL_PATTERN.match(label["name"]) for label in issue["labels"] if LABEL_PATTERN.match(label["name"])), None)
    if not label_info:
        return None

    year, round_number = label_info.groups()
    labels = [label["name"] for label in issue["labels"]]

    body = issue["body"]
    project_match = re.search(r"(?i)Project\s*[\n\r]+(.+?)(?=\n\S|$)", body, re.DOTALL)
    project_name = project_match.group(1).strip() if project_match else ""

    amount_match = re.search(r"(?i)Amount requested\s*[\n\r]+(.+?)(?=\n\S|$)", body, re.DOTALL)
    awarded_amount = 0
    if "awarded" in [l.lower() for l in labels] and amount_match:
        try:
            awarded_amount = int(re.sub(r"[^\d]", "", amount_match.group(1)))
        except ValueError:
            awarded_amount = 0

    return {
        "accepted": "accepted" in [l.lower() for l in labels],
        "year": int(year),
        "round_number": int(round_number),
        "awarded_amount": awarded_amount,
        "project_name": project_name
    }


def main():
    issues = get_all_issues()
    sdg_issues = []
    for issue in issues:
        result = parse_issue(issue)
        if result:
            sdg_issues.append(result)
    print(json.dumps(sdg_issues, indent=2))


if __name__ == "__main__":
    main()
