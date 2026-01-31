import subprocess
import re
import time

p = subprocess.Popen(
    ["/readflag"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
    bufsize=0 # 无缓冲
)

# 1. 极速读取题目并计算
# 为了防止我们自己的 Python 代码太慢，这里用最简单的逻辑
try:
    content = ""
    # 循环读取直到找到算式，防止死锁
    while "((((" not in content:
        char = p.stdout.read(1)
        if not char: break
        content += char
    
    # 提取算式
    if "((((" in content:
        # 简单粗暴截取最后一行
        line = content.splitlines()[-1]
        # 提取数字和符号
        expr = "".join(x for x in line if x in "0123456789+-()")
        if expr:
            ans = eval(expr)
            # 发送答案
            p.stdin.write(f"{ans}\n")
            p.stdin.flush()
            
            # 2. 发送后，死等输出，看它到底吐出什么
            rest, err = p.communicate()
            print("\n--- 程序标准输出 (Stdout) ---")
            print(rest)
            print("\n--- 程序错误输出 (Stderr) ---")
            print(err)
            
except Exception as e:
    print(f"脚本执行出错: {e}")

# 3. 审判时刻：检查退出码
return_code = p.returncode
print("\n" + "="*30)
print(f"【进程退出码】: {return_code}")

if return_code == -14:
    print("【诊断结果】: 进程被 SIGALRM 信号杀死。")
    print("原因：虽然你答对了，但 fopen打开文件+读取+打印 这一系列操作耗时超过了 1ms。")
    print("这不是你的代码错，是服务器磁盘IO太慢或CPU太卡。")
elif return_code == 255 or return_code == 1:
    print("【诊断结果】: 进程返回异常错误码。")
    print("原因：可能是 fopen 打开文件失败（权限问题）导致程序走到了 return -1 分支。")
elif return_code == 0:
    print("【诊断结果】: 进程正常退出。")
    print("如果这时候没看到 flag，说明程序里根本没打印 flag。")
print("="*30)
