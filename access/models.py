"""Access Models"""


class User:
    """User Model"""
    name: str
    encrypted_pass: str

    def __init__(self, name: str, encrypted_pass: str):
        self.name = name
        self.encrypted_pass = encrypted_pass
