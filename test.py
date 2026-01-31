import re
import subprocess

p = subprocess.Popen(
    ["/readflag"],   
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True
)

expr = None
while True:
    line = p.stdout.readline()
    if not line:
        break
    line = line.strip()
    
    # 匹配数字+加减括号
    m = re.search(r'[-+()0-9]+', line)
    if m:
        expr = m.group()
        break

if expr is None:
    raise ValueError("没有找到算术表达式！")

# 计算结果
result = eval(expr)

# 发回程序
p.stdin.write(str(result) + "\n")
p.stdin.flush()

# 读取输出
output = p.stdout.read()

# 【核心修改】写入 /tmp 目录
with open("./flag.txt", "w") as f:
    f.write(output)

print("Output saved to ./flag.txt")
