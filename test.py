import subprocess
import re

# 启动进程
p = subprocess.Popen(
    ["/readflag"], 
    stdin=subprocess.PIPE, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE,
    universal_newlines=True
)

# 循环读取，直到找到算式
while True:
    # 注意：不要用readlines()一次读完，因为没有EOF会卡死
    # 逐行读取，读到算式立刻处理
    line = p.stdout.readline()
    if not line: break
    
    # 检测是否包含算式（特征：有数字且有括号）
    if '(' in line and re.search(r'\d', line):
        # 1. 立刻计算 (去掉换行符)
        expr = line.strip()
        result = eval(expr)
        
        # 2. 立刻发送！不要打印 debug 信息，不要等提示符！
        # 直接把答案塞入管道，这样当程序运行到 scanf 时可以零延迟读取
        p.stdin.write(str(result) + "\n")
        p.stdin.flush()
        break

# 3. 此时答案已发，程序应该正在吐出 flag
# 我们一次性读取剩余所有输出
print("--- 最终输出 ---")
final_output = p.stdout.read() 
print(final_output)
