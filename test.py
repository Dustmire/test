import ctypes
import time
import subprocess

# 1. 加载 C 标准库以调用相同的 rand() 和 srand()
libc = ctypes.CDLL("libc.so.6")

# 模拟全局变量 seed，请根据实际二进制文件中的初始值修改（通常为 0）
global_seed = 0

def exp_rand(timestamp):
    global global_seed
    global_seed += 1
    # 核心预测逻辑：srand(v0 + seed * seed)
    # v0 是 time(0LL)
    new_seed = timestamp + (global_seed * global_seed)
    libc.srand(new_seed)
    return libc.rand() % 2

def predict_challenge():
    # 获取预测用的时间戳
    t = int(time.time())
    
    # 模拟 main 函数中的连续 5 次 rand_t() 调用
    # 注意：如果 rand_t 内部没有 srand，则取决于初始随机状态
    # 如果 rand_t 内部也有 srand(time(0))，此处需要先调用 libc.srand(t)
    v13 = libc.rand()
    v14 = libc.rand()
    v15 = libc.rand()
    v16 = libc.rand()
    v17 = libc.rand()

    # --- 开始模拟题目构建逻辑 ---
    
    # 第 1 步 (v4)
    v4 = exp_rand(t)
    op = "-" if v4 == 1 else "+"
    buf = f"((((({v13}){op}({v14}))"

    # 第 2 步 (v5)
    v5 = exp_rand(t)
    op = "-" if v5 == 1 else "+"
    buf += f"{op}({v15}))"

    # 第 3 步 (v6)
    v6 = exp_rand(t)
    op = "-" if v6 == 1 else "+"
    buf += f"{op}({v16}))"

    # 第 4 步 (v7)
    v7 = exp_rand(t)
    op = "-" if v7 == 1 else "+"
    buf += f"{op}({v17}))\n"

    return buf

# --- 执行与输出 ---

# 1. 预测当前秒产生的题目
predicted_str = predict_challenge()

print("="*40)
print(f"【预测题目内容】:\n{predicted_str}")
print("="*40)

# 2. 调用 /readflag 并显示结果
try:
    # 运行指定的命令并获取输出
    res = subprocess.run(["/readflag"], capture_output=True, text=True)
    print("\n【/readflag 输出】:")
    print(res.stdout if res.stdout else "无输出内容")
except FileNotFoundError:
    print("\n错误: 未找到 /readflag 文件，请确保路径正确。")
except Exception as e:
    print(f"\n运行出错: {e}")
