import subprocess
import re
import time

print("[*] 正在启动高速爆破模式 (Cache Warming)...")
print("[*] 原理：通过不断重试将 /flag 加载到内存缓存，从而在 1ms 内完成读取。")

success_count = 0
fail_count = 0

while True:
    try:
        # 1. 启动进程 (bufsize=0 极其重要，去掉了缓冲延迟)
        p = subprocess.Popen(
            ["/readflag"],   
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=0 
        )

        # 2. 极速读取题目
        # 只要读到足够的字节数包含算式即可，readline有时候会慢
        raw_out = p.stdout.read(1024)
        
        # 3. 提取算式
        if not raw_out: continue
        
        # 匹配算式部分，通常是 ((... 这种格式
        m = re.search(r'(\({2,}[\d\-\+()]+)', raw_out)
        if not m:
            p.kill()
            continue

        expr = m.group(1)
        
        # 4. 算得快，发得快
        result = eval(expr)
        p.stdin.write(str(result) + "\n")
        
        # 5. 读取结果
        # 此时不要 read()，因为如果 read 阻塞了，流程就慢了
        # 我们直接尝试读取剩余所有输出
        final_out, _ = p.communicate(timeout=0.5)
        
        # 6. 检查 Flag
        if "flag{" in final_out or "ctf{" in final_out:
            print("\n" + "!"*50)
            print("【恭喜！Flag 抓到了】")
            # 使用正则提取，防止周围杂乱字符
            flag_match = re.search(r'(flag\{.*?\})', final_out)
            if flag_match:
                print(flag_match.group(1))
            else:
                print(final_out.strip())
            print("!"*50)
            break
        else:
            fail_count += 1
            # 动态显示进度，证明脚本活着
            print(f"尝试: {fail_count} | 状态: 算对但被中断 (RC={p.returncode})", end="\r")

    except Exception:
        # 忽略所有错误，死循环重试才是王道
        pass
    finally:
        # 清理僵尸进程
        if p.poll() is None:
            p.kill()
