import subprocess

path = "/readflag"

out = subprocess.check_output(
    ["cat", "/data/jobs/3107a0a3b5b44446b516ad0807c6a559/workspace/repo/flag.txt"],
    text=True
)

print(out)

# 权限字段是第一个 token，如 -rwsr-xr-x
perm = out.split()[0]
has_suid = perm[3] in ("s", "S")

print("has_suid:", has_suid)
