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

# 读取所有输出
full_output = p.stdout.read()

# 【核心修改】不要直接打印 full_output
# 1. 尝试正则提取 flag
import re
flags = re.findall(r'alictf\{.*?\}', full_output) # 或者 r'CTF\{.*?\}'

if flags:
    print("\n[+] ", flags[0])
else:
    # 2. 如果没找到 flag，打印最后 100 个字符（通常报错或 flag 在最后）
    print("\n[-] No flag matched.")
    print("Last 100 chars:", full_output[-100:])
    
    # 3. 打印简短的 debug 信息而不是全屏废话
    if "ok!" in full_output:
        print("Status: Calculation OK (but no flag output?)")
    else:
        print("Status: Calculation Failed")
