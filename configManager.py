import json
import os

class ConfigManager:
    def __init__(self, configPath):
        self.configPath = configPath
        self.config = self.loadConfig()

    def loadConfig(self):
        with open(self.configPath, "r", encoding="utf-8") as f:
            return json.load(f)
