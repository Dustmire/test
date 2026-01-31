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
p.stdin.write(str(result) + "\n")
p.stdin.flush()

# 读取所有剩余输出
out, err = p.communicate() # timeout留给系统，或者设置大一点

print("stdout内容:\n", out)
print("stderr内容:\n", err)

# 关键诊断
rc = p.returncode
print(f"程序退出代码: {rc}")

if rc == 255:
    print("【诊断】权限错误：程序无法打开 /flag 文件。请检查 /readflag 是否属于 root 用户 (chown root:root)。")
elif rc == -14:
    print("【诊断】超时被杀：1ms 闹钟触发了。SIGALRM 杀死了进程。")
else:
    print("【诊断】其他退出情况。")
