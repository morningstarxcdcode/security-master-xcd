import argparse
import yaml
import os

from scanner.vuln_scanner import VulnerabilityScanner
from scanner.fix_suggester import FixSuggester
from actions.pr_creator import PRCreator
from reporting.issue_reporter import IssueReporter
from utils.error_handling import humanized_error

def main():
    parser = argparse.ArgumentParser(description="Run security scan.")
    parser.add_argument("--config", type=str, required=True, help="Path to configuration file.")
    args = parser.parse_args()

    if not os.path.exists(args.config):
        humanized_error(f"Configuration file not found at: {args.config}")
        return

    try:
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        humanized_error(f"Error parsing YAML configuration: {e}")
        return

    project_root = os.getcwd() # Assuming run_scan.py is run from project root

    scanner = VulnerabilityScanner(config.get("scanner", {}))
    suggester = FixSuggester(config.get("autofix", {}))
    pr_creator = PRCreator(config.get("github", {}))
    reporter = IssueReporter(project_root)

    print(f"Running scan with config: {config}\n")

    # Placeholder for actual codebase path (e.g., current directory or specified in config)
    codebase_to_scan = project_root # For demonstration, scanning current directory

    vulnerabilities = scanner.scan(codebase_to_scan)

    if not vulnerabilities:
        print("No vulnerabilities detected. Your codebase looks secure!\n")
        return

    print("\n--- Detected Vulnerabilities ---\n")
    for vuln in vulnerabilities:
        print(reporter.format_vulnerability_report(vuln))

        if config.get("autofix", {}).get("enable_suggestions", False):
            fix_suggestion = suggester.suggest_fix(vuln)
            if fix_suggestion:
                print(f"\nAutomated Fix Suggestion for {vuln['title']}:\n")
                print(f"  File: {os.path.relpath(fix_suggestion['file'], project_root)}")
                print(f"  Line: {fix_suggestion['line']}")
                print(f"  Suggestion:\n{fix_suggestion['suggestion']}")
                print(f"  Description: {fix_suggestion['description']}\n")

                if config.get("autofix", {}).get("enable_auto_pr", False):
                    print("Attempting to create an automatic Pull Request...")
                    pr_creator.create_pr(fix_suggestion)
                else:
                    print("Auto-PR is disabled. Please apply the fix manually or enable auto_pr in config.\n")
            else:
                print("No automated fix suggestion available for this vulnerability.\n")

        if vuln.get("autofix") == "N/A (manual intervention)":
            print(reporter.format_manual_fix_guidance(vuln))

    print("\nScan complete. Review the reports above.\n")

if __name__ == "__main__":
    main()