import subprocess


token = "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"

command = f"huggingface-cli login --token {token}"


subprocess.run(command, shell=True)
