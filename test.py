import subprocess
import time
import os
import re

# 1. 准备 flag.txt
filename = "flag.txt"
if os.path.exists(filename):
    os.remove(filename)

# 以 "w+b" 模式打开文件：既能让程序写，我们也能同时读
# buffering=0 确保 Python 读取时没有延迟
out_file = open(filename, "w+b", buffering=0)

print(f"[*] 启动进程，输出重定向至 {filename}...")

# 2. 启动进程，stdout 直接对接文件句柄
p = subprocess.Popen(
    ["/readflag"],
    stdin=subprocess.PIPE,
    stdout=out_file,  # <--- 关键：直接写入文件，不经过 Python 管道
    stderr=subprocess.PIPE,
    bufsize=0         # stdin 无缓冲
)

# 3. 监控文件内容（代替读取 stdout）
try:
    equation_found = False
    
    while True:
        # 检查进程是否已退出
        if p.poll() is not None:
            break

        # 移动指针到文件开头读取最新内容
        out_file.seek(0)
        content = out_file.read().decode('utf-8', errors='ignore')

        # A. 找算式
        if not equation_found and "((((" in content:
            # 提取最后出现的算式
            lines = content.splitlines()
            for line in reversed(lines):
                if "((((" in line:
                    # 简单清洗
                    clean_expr = "".join(c for c in line if c in "0123456789+-()")
                    try:
                        ans = eval(clean_expr)
                        print(f"[*] 算式: {clean_expr}")
                        print(f"[*] 答案: {ans}")
                        
                        # 极速写入答案
                        p.stdin.write(f"{ans}\n".encode())
                        p.stdin.flush()
                        equation_found = True
                    except:
                        pass
                    break
        
        # B. 找 Flag
        if "flag" in content or "{" in content:
            print("\n" + "="*30)
            print("SUCCESS! Flag captured in file:")
            print(content)
            print("="*30)
            p.terminate()
            break
            
        # 极短的休眠避免 CPU 100% 空转，给文件写入留点时间
        # 如果还是拿不到，可以注释掉这行
        # time.sleep(0.0001) 

except Exception as e:
    print(e)
finally:
    out_file.close()
    p.terminate()

# 最后再次打印文件内容确认
if os.path.exists(filename):
    with open(filename, 'r') as f:
        print("\n[Final File Content]:")
        print(f.read())
