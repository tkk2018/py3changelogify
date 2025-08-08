import subprocess
from .gitlogfetcher import GitLogFetcher
from .gitlogcommit import GitLogCommit

class GitLogFetcherBySubprocess(GitLogFetcher):
    def __init__(self, inclusive_start_hash, inclusive_end_hash, workspace = None):
        # type: (str, str, str) -> GitLogFetcherBySubprocess
        self.start_hash = inclusive_start_hash
        self.end_hash = inclusive_end_hash
        self.workspace = workspace

    def fetch(self):
        # type: () -> list[GitLogCommit]
        cmd = [
            "git", "log", self.start_hash + ".." + self.end_hash,
            "--pretty=format:%h|%s",
            # "--pretty=format:%h|%B", # TODO: parse footer
            "--no-merges"
        ]
        print(" ".join(cmd))

        try:
            output = subprocess.check_output(cmd, cwd=self.workspace).decode("utf-8")
            # {hash1}|{oneline-message}\n
            # {hash2}|{oneline-message}\n
            print(output)
        except subprocess.CalledProcessError:
            print("Error running git log.")
            exit(1)

        # type list[GitLogCommit]
        commits = []
        for entry in output.strip().split("\n"):
            if "|" not in entry:
                # TODO: parse the body and footer
                continue
            commit_hash, oneline_message = entry.split("|", 1)
            commits.append(GitLogCommit(commit_hash, oneline_message, None))
        return commits
