import re
import subprocess
import base64

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
    print("题目行:", line)
    
    # 匹配数字+加减括号
    m = re.search(r'[-+()0-9]+', line)
    if m:
        expr = m.group()
        break

if expr is None:
    raise ValueError("没有找到算术表达式！")

# 计算结果
result = eval(expr)
print("答案:", result)

# 发回程序
p.stdin.write(str(result) + "\n")
p.stdin.flush()

out, err = p.communicate(input=str(result) + "\n", timeout=2)
print("stdout:", out)
print("stderr:", err)
print("returncode:", p.returncode)
