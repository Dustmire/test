import subprocess

path = "/flag"

out = subprocess.check_output(
    ["cat", path],
    text=True
)

print(out)
