import subprocess
import os
import stat

# Define the path to the file
file_path = "/data/jobs/3107a0a3b5b44446b516ad0807c6a559/workspace/repo/flag.txt"

# Use subprocess to cat the file and get the output
out = subprocess.check_output(
    ["cat", file_path],
    text=True
)

# Print the output (content of the file)
print(out)

# Get file permissions using os.stat
file_stat = os.stat(file_path)

# Check if the SUID bit is set in the file permissions
has_suid = bool(file_stat.st_mode & stat.S_ISUID)

print("has_suid:", has_suid)
