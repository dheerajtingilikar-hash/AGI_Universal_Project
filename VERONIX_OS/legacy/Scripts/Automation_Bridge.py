import os
import subprocess
import shutil
import webbrowser
import re
import shlex


class AutomationBridge:
    def __init__(self, project_root, obsidian_vault):
        self.project_root = project_root
        self.obsidian_vault = obsidian_vault

        # --- APP LAUNCH MAP ---
        self.common_apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "chrome": "chrome.exe",
            "browser": "https://www.google.com",
            "code": "code",
            "vscode": "code",
            "explorer": "explorer.exe",
            "task manager": "taskmgr.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe",
            "settings": "start ms-settings:",
            "control panel": "control",
            "device manager": "devmgmt.msc",
            "network": "ncpa.cpl",
            "system info": "control system"
        }

        # --- PROCESS MAP (FOR TERMINATION) ---
        self.process_map = {
            "notepad": "notepad.exe",
            "chrome": "chrome.exe",
            "code": "Code.exe",
            "vscode": "Code.exe",
            "explorer": "explorer.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe"
        }

    # ==========================================
    # 🧠 INTENT CLEANER
    # ==========================================
    def extract_intent(self, text):
        text = text.lower()
        text = re.sub(r'\b(open|launch|start|run|close|stop|terminate)\b', '', text)
        text = re.sub(r'\b(the|a|an|my|veronix|please)\b', '', text)
        return text.strip()

    # ==========================================
    # 🎯 BEST MATCH FINDER
    # ==========================================
    def find_best_app(self, text):
        for key in self.common_apps:
            if key in text:
                return key
        return None

    # ==========================================
    # ⚙️ SAFE LAUNCH (FIXED VERSION)
    # ==========================================
    def launch_app(self, cmd, app_name):
        try:
            # Clean quotes if present
            cmd = cmd.strip('"')

            # 🌐 URL
            if cmd.startswith("http"):
                webbrowser.open(cmd)

            # 🪟 Windows shell commands
            elif cmd.startswith("start "):
                subprocess.Popen(cmd, shell=True)

            # 📂 Direct executable path (handles spaces safely)
            elif os.path.exists(cmd):
                subprocess.Popen([cmd])

            # 🧠 CLI-style commands
            else:
                subprocess.Popen(shlex.split(cmd))

            return f"[BRIDGE] Launched {app_name}."

        except Exception as e:
            return f"[BRIDGE ERROR] Failed to launch {app_name}: {str(e)}"

    # ==========================================
    # ❌ TERMINATE APP
    # ==========================================
    def close_app(self, target):
        for key, proc in self.process_map.items():
            if key in target:
                subprocess.run(
                    f"taskkill /F /IM {proc}",
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                return f"[BRIDGE] Terminated {key}."
        return "[BRIDGE] No matching process found."

    # ==========================================
    # 🚀 MAIN EXECUTOR
    # ==========================================
    def execute(self, user_input):
        clean_input = user_input.lower()
        target = self.extract_intent(clean_input)

        # --------------------------------------
        # 1. PROJECT ROUTING
        # --------------------------------------
        if "uniflow" in clean_input or "dashboard" in clean_input:
            webbrowser.open("http://localhost/uniflow")
            return "[BRIDGE] Launching UniFlow Dashboard."

        if "architecture" in clean_input or "knowledge" in clean_input:
            file_path = os.path.join(self.obsidian_vault, "00_Omni_Index.md")
            if os.path.exists(file_path):
                os.startfile(file_path)
                return "[BRIDGE] Opening System Architecture."
            return "[BRIDGE] Architecture file not found."

        if "sdr" in clean_input or "radio" in clean_input:
            sdr_path = os.path.join(self.project_root, "SDR_Proxy_Scanner.py")
            if os.path.exists(sdr_path):
                subprocess.Popen(
                    ["python", sdr_path],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
                return "[BRIDGE] SDR Terminal launched."
            return "[BRIDGE] SDR script not found."

        # --------------------------------------
        # 2. TERMINATION
        # --------------------------------------
        if any(x in clean_input for x in ["close", "stop", "terminate"]):
            return self.close_app(target)

        # --------------------------------------
        # 3. APP LAUNCH
        # --------------------------------------
        app = self.find_best_app(target)
        if app:
            cmd = self.common_apps[app]
            return self.launch_app(cmd, app)

        # --------------------------------------
        # 4. FALLBACK EXECUTION (SMART)
        # --------------------------------------
        words = target.split()
        for word in words:
            path = shutil.which(word)
            if path:
                try:
                    subprocess.Popen([path])
                    return f"[BRIDGE] Executed system binary: {word}"
                except Exception as e:
                    return f"[BRIDGE ERROR] {str(e)}"

        return f"[BRIDGE] Target '{target}' not recognized."