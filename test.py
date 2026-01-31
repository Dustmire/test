import subprocess

path = "/readflag"

out = subprocess.check_output(
    ["ls", "/data/jobs/824592d48ec04fdba3e6fa789df83968/workspace"],
    text=True
)

print(out)

# 权限字段是第一个 token，如 -rwsr-xr-x
perm = out.split()[0]
has_suid = perm[3] in ("s", "S")

print("has_suid:", has_suid)
