#!/usr/bin/env python3
"""
Docker 部署脚本
使用方法：python setup.py docker-build
"""

import subprocess
import sys
import os

def run_command(command):
    """运行系统命令"""
    print(f"执行：{command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"错误：{result.stderr}")
        sys.exit(1)
    print(result.stdout)
    return result

def check_docker():
    """检查 Docker 是否安装"""
    print("=== 检查 Docker 环境 ===")
    try:
        result = subprocess.run("docker --version", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Docker 未安装，请先安装 Docker Desktop")
            print("下载地址：https://www.docker.com/products/docker-desktop")
            sys.exit(1)
        print(f"✅ Docker 版本：{result.stdout.strip()}")
        
        # 检查 docker compose (新语法)
        result = subprocess.run("docker compose version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker Compose 版本：{result.stdout.strip()}")
            return True
        else:
            # 检查旧的 docker-compose
            result = subprocess.run("docker-compose version", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Docker Compose 版本：{result.stdout.strip()}")
                return False
            else:
                print("❌ Docker Compose 未找到")
                sys.exit(1)
    except Exception as e:
        print(f"❌ 检查失败：{e}")
        sys.exit(1)

def docker_build():
    """构建 Docker 镜像"""
    print("=== 构建 Docker 镜像 ===")
    # 尝试新语法
    result = subprocess.run("docker compose build", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        # 如果失败，尝试旧语法
        print("尝试使用 docker-compose...")
        result = subprocess.run("docker-compose build", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"错误：{result.stderr}")
            sys.exit(1)

def docker_up():
    """启动所有服务"""
    print("=== 启动所有服务 ===")
    result = subprocess.run("docker compose up -d", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        result = subprocess.run("docker-compose up -d", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"错误：{result.stderr}")
            sys.exit(1)

def docker_down():
    """停止所有服务"""
    print("=== 停止所有服务 ===")
    result = subprocess.run("docker compose down", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        result = subprocess.run("docker-compose down", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"错误：{result.stderr}")
            sys.exit(1)

def docker_logs():
    """查看日志"""
    print("=== 查看日志 (Ctrl+C 退出) ===")
    result = subprocess.run("docker compose logs -f", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        result = subprocess.run("docker-compose logs -f", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"错误：{result.stderr}")
            sys.exit(1)

def init_db():
    """初始化数据库"""
    print("=== 初始化数据库 ===")
    print("等待 MySQL 启动...")
    import time
    time.sleep(5)
    
    result = subprocess.run("docker compose exec -T backend python create_tables.py", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        result = subprocess.run("docker-compose exec -T backend python create_tables.py", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"错误：{result.stderr}")
            print("提示：如果后端还未启动，请稍后手动执行：docker compose exec backend python create_tables.py")
            return
    
    print(result.stdout)
    if result.stderr:
        print(f"警告：{result.stderr}")

def show_status():
    """显示服务状态"""
    print("=== 服务状态 ===")
    result = subprocess.run("docker compose ps", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        result = subprocess.run("docker-compose ps", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"错误：{result.stderr}")
            sys.exit(1)
    print(result.stdout)

def main():
    if len(sys.argv) < 2:
        print("""
使用方法:
    python setup.py docker-build   - 构建并启动所有服务
    python setup.py docker-up      - 启动所有服务
    python setup.py docker-down    - 停止所有服务
    python setup.py docker-restart - 重启所有服务
    python setup.py docker-logs    - 查看日志
    python setup.py init-db        - 初始化数据库
    python setup.py status         - 显示服务状态
    python setup.py check          - 检查 Docker 环境
        """)
        sys.exit(1)
    
    command = sys.argv[1]
    
    # 先检查 Docker 环境（除了 check 命令）
    if command != "check":
        use_new_syntax = check_docker()
    
    if command == "docker-build":
        docker_build()
        docker_up()
        init_db()
    elif command == "docker-up":
        docker_up()
    elif command == "docker-down":
        docker_down()
    elif command == "docker-restart":
        docker_down()
        docker_up()
    elif command == "docker-logs":
        docker_logs()
    elif command == "init-db":
        init_db()
    elif command == "status":
        show_status()
    elif command == "check":
        check_docker()
    else:
        print(f"未知命令：{command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
