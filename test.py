import subprocess

path = "/readflag"

# 1. 使用 .strip() 去掉末尾的换行符
out = subprocess.check_output(
    ["ls", "-la", path],
    text=True
).strip()

# 逻辑判断
perm = out.split()[0]
# 确保检查位存在
has_suid = len(perm) > 3 and perm[3] in ("s", "S")

# 2. 【关键】在一行内输出所有信息，防止被工具截断
print(f"File: {out}  |||  Has_SUID: {has_suid}")
