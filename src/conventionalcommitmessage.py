class ConventionalCommitMessage:
    def __init__(self, commit_hash, message_type, scope, is_breaking_change, subject, body, breaking_change_description):
        # type: (str, str, str, str, str, str, str) -> ConventionalCommitMessage
        self.hash = commit_hash
        self.type = message_type
        self.scope = scope
        self.is_breaking_change = bool(is_breaking_change)
        self.subject = subject
        self.body = body
        self.breaking_change_description = breaking_change_description
