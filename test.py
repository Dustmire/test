import subprocess
import re
import base64
import sys

print("=== 开始诊断 ===")

# 1. 启动进程
try:
    p = subprocess.Popen(
        ["/readflag"],  # 确保路径对，如果在当前目录就是 ./readflag
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True, # 文本模式
        bufsize=0
    )
except Exception as e:
    print(f"启动失败: {e}")
    sys.exit(1)

# 2. 读取题目
# 读取前 100 个字符通常足够包含算式
raw_out = p.stdout.read(100)
print(f"[调试] 题目读取片段: {raw_out.strip()}")

m = re.search(r'(\({1,}[\d\-\+()]+)', raw_out)
if not m:
    print("错误: 未找到算式，可能输出完全被缓冲或格式不对")
    p.kill()
    sys.exit(1)

expr = m.group(1)
result = eval(expr)
print(f"[调试] 计算结果: {result}")

# 3. 发送答案
p.stdin.write(str(result) + "\n")
p.stdin.flush()

# 4. 获取剩余所有输出 (关键诊断步骤)
# 使用 communicate 等待程序自然结束
rest_out, err_out = p.communicate()

# 5. 打印诊断报告
rc = p.returncode

print("\n" + "="*30)
print(f"【诊断结果报告】")
print(f"退出码 (Return Code): {rc}")
print("-" * 20)

if rc == 0:
    print("结论: ✅ 程序正常运行结束。如果没看到 flag，那就是被截断了。")
elif rc == 255:
    print("结论: ❌ 程序主动报错退出 (return -1)。原因是 fopen('/flag') 失败。")
elif rc == -14:
    print("结论: ⏰ 程序超时被杀 (SIGALRM)。速度太慢。")
else:
    print(f"结论: ❓ 异常退出，代码 {rc}")

print("-" * 20)
print(f"标准错误 (stderr): {err_out}")
print("-" * 20)

# 6. 终极验证：Base64 打印
# 如果上面说是 0，但在 raw text 里看不见 flag，就把下面这串拿去解码
b64_content = base64.b64encode((raw_out + rest_out).encode()).decode()
print(f"完整输出 (Base64编码，防截断):\n{b64_content}")
print("="*30)
