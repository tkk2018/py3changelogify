import sys
if sys.version_info >= (3, 5):
    from typing import Dict, Optional
from .defaultconventionalcommittype import DefaultConventionalCommitMessageType
from .conventionalcommitmessage import ConventionalCommitMessage

class ChangelogMarkdownFormatter:
    def __init__(self, types = DefaultConventionalCommitMessageType):
        # type: (Optional[Dict[str, str]]) -> ChangelogMarkdownFormatter
        self.types = types

    def format(self, version, date, commits):
        # type: (str, str, Dict[str, list[ConventionalCommitMessage]]) -> str

        output_lines = ["## {} ({})".format(version, date), ""]
        for key in self.types:
          if key in commits:
              output_lines.append("### {}\n".format(self.types[key]))
              for commit in commits[key]:
                  message = "- "
                  if commit.is_breaking_change:
                      message = message + "! "

                  if commit.scope:
                      message = message + "**{}**: {} (#{})".format(commit.scope, commit.subject, commit.hash)
                  else:
                      message = message + "{} (#{})".format(commit.subject, commit.hash)
                  output_lines.append(message)
              output_lines.append("")  # Extra newline after section

        changelog = "\n".join(output_lines)
        return changelog