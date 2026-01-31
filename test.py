import subprocess

# 方案1: 正确的 find 命令
out = subprocess.check_output(
    ["find", "/data/jobs/", "-name", "flag.txt"],
    text=True
)
print(out)
