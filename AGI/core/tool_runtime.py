# AGI/core/tool_runtime.py

import os
import subprocess
import webbrowser

class ToolRuntime:
    def __init__(self):
        self.allowed_dirs = ["D:\\AGI_Universal_Project"]

    def safe_write(self, path, content):
        if any(path.startswith(d) for d in self.allowed_dirs):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return "written"
        return "blocked"

    def safe_read(self, path):
        if any(path.startswith(d) for d in self.allowed_dirs):
            return open(path, "r", encoding="utf-8").read()
        return "blocked"

    def open_web(self, url):
        webbrowser.open(url)
        return "opened"

    def run_cmd(self, cmd):
        # SAFE MODE: only echo commands
        return f"blocked execution: {cmd}"