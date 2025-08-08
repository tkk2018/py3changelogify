class GitLogCommit:
    def __init__(self, commit_hash, oneline, body = None):
        # type: (str, str, str) -> GitLogCommit
        self.hash = commit_hash
        self.oneline = oneline
        self.body = body
