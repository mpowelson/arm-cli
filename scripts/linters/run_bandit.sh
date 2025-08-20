#!/bin/bash
# run_bandit.sh - Runs Bandit and prints a summary, failing only on HIGH severity

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

bandit -r arm_cli/ -f json -o bandit-report.json || true

if [ -f bandit-report.json ]; then
    python3 - <<'EOF'
import json, sys

with open("bandit-report.json") as f:
    data = json.load(f)

high_issues = []
medium_issues = []
low_issues = []

for issue in data.get("results", []):
    sev = issue.get("issue_severity", "").upper()
    if sev == "HIGH":
        high_issues.append(issue)
    elif sev == "MEDIUM":
        medium_issues.append(issue)
    elif sev == "LOW":
        low_issues.append(issue)

all_issues = high_issues + medium_issues + low_issues

if all_issues:
    print("\033[1;33mBandit security summary:\033[0m")
    for issue in all_issues:
        sev = issue.get("issue_severity")
        conf = issue.get("issue_confidence")
        file = issue.get("filename")
        line = issue.get("line_number")
        text = issue.get("issue_text")
        print(f"[{sev}/{conf}] {file}:{line} {text}")
    print("")

if high_issues:
    print(f"\033[0;31mFound {len(high_issues)} HIGH severity issues - failing!\033[0m")
    sys.exit(1)
else:
    print("\033[0;32mNo HIGH severity issues found.\033[0m")
EOF
fi
