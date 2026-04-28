import subprocess

ALLOWED = ["echo", "dir", "type"]

def run_tool(command: str):
    try:
        base = command.split()[0]

        if base not in ALLOWED:
            return "BLOCKED: unsafe command"

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout

    except Exception as e:
        return str(e)