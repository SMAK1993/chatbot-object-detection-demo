import json


class SyncConfig:
    def __init__(self, filename):
        self.cv = False
        self.chat = False
        self.filename = filename

    def load_config(self):
        with open(self.filename, 'r') as f:
            config = json.loads(f.read())
            self.cv = config.get('cv_enabled')
            self.chat = config.get('chat_enabled')

    def save_config(self, cv, chat):
        self.cv = cv
        self.chat = chat
        with open(self.filename, 'w') as f:
            f.write(json.dumps({
                "cv_enabled": cv,
                "chat_enabled": chat
            }))

    def __str__(self):
        return f"{{cv={self.cv}, chat={self.chat}}}"
