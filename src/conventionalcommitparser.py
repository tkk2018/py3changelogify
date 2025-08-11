import sys
if sys.version_info >= (3, 5):
    from typing import Optional, Callable, Dict
import re
from .gitlogcommit import GitLogCommit
from .defaultconventionalcommittype import DefaultConventionalCommitMessageType
from .conventionalcommitmessage import ConventionalCommitMessage

class ConventionalCommitParser:
    def __init__(self, types = DefaultConventionalCommitMessageType):
        # type: (Optional[Dict[str, str]]) -> ConventionalCommitParser
        self.types = types
        self.conventional_commit_message_pattern = re.compile(r"^(\w+)(?:\(([^)]+)\))?(!)?:\s+(.+)")
        self.breaking_change_footer_pattern = re.compile(r"BREAKING[- ]CHANGE:\s*(.+)", re.IGNORECASE)

    def parses(self, commits, cb):
        # type: (list[GitLogCommit], Callable[[ConventionalCommitMessage], None]) -> None
        for commit in commits:
            conventional_commit_message = self.parse(commit=commit)
            cb(conventional_commit_message)

    def parse(self, commit: GitLogCommit) -> ConventionalCommitMessage:
        header = commit.oneline
        body = commit.body

        # type: Optional[str]
        message_type = None
        # type: Optional[str]
        scope = None
        # type: Optional[str]
        subject = None
        # type: Optional[str]
        breaking_change_description = None
        # type: bool
        is_breaking_change = False

        match = self.conventional_commit_message_pattern.match(header)
        if match:
            message_type = match.group(1)
            scope = match.group(2)
            bang = match.group(3)
            subject = match.group(4)
            is_breaking_change = bool(bang)

        if commit.body:
          footer_match = self.breaking_change_footer_pattern.search(body)
          if footer_match:
              breaking_change_description = footer_match.group(1)

        conventional_commit_message = ConventionalCommitMessage(
            commit_hash=commit.hash,
            message_type=message_type,
            scope=scope,
            is_breaking_change=is_breaking_change,
            subject=subject,
            body=body,
            breaking_change_description=breaking_change_description
        )

        return conventional_commit_message

    def parse_to_array(self, commits):
        # type: (list[GitLogCommit]) -> list[ConventionalCommitMessage]

        # type: list[ConventionalCommitMessage]
        result = []
        self.parses(commits, lambda c: result.append(c))
        return result

    def parse_to_group(self, commits):
        # type: (list[GitLogCommit]) -> Dict[str, list[ConventionalCommitMessage]]

        # type: Dict[str, list[ConventionalCommitMessage]]
        grouped = {}
        self.parses(commits, lambda c: grouped.setdefault(c.type or "other", []).append(c))
        return grouped

    def set_custom_types(self, custom_types: Dict[str, str]) -> None:
        # type: (Dict[str, str]) -> None
        self.types.update(custom_types)
