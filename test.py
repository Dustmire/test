import re
import subprocess

p = subprocess.Popen(
    ["/readflag"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
    bufsize=1 # 使用行缓冲
)

expr = None
# 1. 持续读取直到找到算术表达式
while True:
    line = p.stdout.readline()
    if not line: break
    print("DEBUG:", line.strip())
    
    # 修改正则以匹配更复杂的负数和括号
    m = re.search(r'[\(\)\d\+\-]+', line)
    if m and any(op in line for op in '+-'): # 确保不仅仅是提示文字
        expr = m.group()
        break

if expr:
    # 2. 计算并发送
    result = eval(expr)
    print(f"计算出的答案: {result}")
    p.stdin.write(f"{result}\n")
    p.stdin.flush()

    # 3. 关键：发送后，读取剩余的所有输出
    # 既然程序在输出 flag 后会退出，这里可以用 read()
    final_output = p.stdout.read()
    print("--- 最终输出 ---")
    print(final_output)
    
p.wait()
