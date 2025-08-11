#!/usr/bin/python3

import argparse
import datetime
import os
from src.conventionalcommitparser import ConventionalCommitParser
from src.gitlogfetcherbysubprocess import GitLogFetcherBySubprocess
from src.changelogmarkdownformatter import ChangelogMarkdownFormatter

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        description="Generate a changelog between two Git commits (uses Conventional Commits format)",
        epilog=
        "Examples:\n" +
        "  cli.py -v 1.2.0 -s abc123 -e def456\n" +
        "  cli.py --version 1.2.0 --start abc123 --end def456 --date 2025-08-08 --filename CHANGELOG.md\n",
        formatter_class=argparse.RawTextHelpFormatter
    )
    arg_parser.add_argument("-v", "--version", required=True, help="Release version (e.g., 1.0.0)")
    arg_parser.add_argument("-d", "--date", required=False, default=datetime.date.today().isoformat(), help="Release date (default: " + datetime.date.today().isoformat() + ")")
    arg_parser.add_argument("-s", "--start", required=True, metavar="HASH", help="Inclusive start commit hash (e.g., 123456)")
    arg_parser.add_argument("-e", "--end", required=True, metavar="HASH", help="Inclusive end commit hash (e.g., abcdef)")
    arg_parser.add_argument("-o", "--filename", required=False, default="CHANGELOG.md", help="Output filename (default: CHANGELOG.md)")
    arg_parser.add_argument("--cwd", required=False, default=None, help="Workspace (default: .)")

    # Parse arguments
    args = arg_parser.parse_args()

    release_version = args.version
    release_date = args.date
    hash_start = args.start
    hash_end = args.end
    changelog_filename = args.filename
    cwd = args.cwd

    # Fetch git logs
    git_logs = GitLogFetcherBySubprocess(hash_start, hash_end, cwd).fetch()

    commit_parser = ConventionalCommitParser()
    grouped = commit_parser.parse_to_group(git_logs)

    latest_changelog = ChangelogMarkdownFormatter().format(release_version, release_date, grouped)

    changelog_path = os.path.join(cwd, changelog_filename) if cwd else changelog_filename

    if os.path.exists(changelog_path):
        with open(changelog_path, "r") as old_f:
            existing = old_f.read()
        with open(changelog_path, "w") as f:
            f.write(latest_changelog + "\n" + existing.lstrip())
    else:
        with open(changelog_path, "w") as f:
            f.write("# Changelog\n\n")
            f.write(latest_changelog)
