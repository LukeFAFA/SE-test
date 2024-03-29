import subprocess
import sys

def is_interesting(command, subset):
    try:
        # 为了正确处理包含空格的命令（如"bash ./is-interesting.sh"），需要将命令分割
        cmd = command.split() + [str(s) for s in subset]
        result = subprocess.run(cmd, check=False, capture_output=True)
        return result.returncode == 1
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def reduce_set(command, current_set):
    if len(current_set) <= 1:
        return current_set
    # 尝试将集合一分为二
    mid = len(current_set) // 2
    set1 = current_set[:mid]
    set2 = current_set[mid:]
    
    # 检查两个子集是否有趣
    interesting1 = is_interesting(command, set1)
    interesting2 = is_interesting(command, set2)
    
    if interesting1:
        return reduce_set(command, set1)
    elif interesting2:
        return reduce_set(command, set2)
    
    return current_set

def delta_debugging(n, command):
    full_set = list(range(n))
    # 找到包含3和6的最小“有趣”子集
    return reduce_set(command, full_set)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python delta.py <size_n> <command>")
        sys.exit(1)
    
    n = int(sys.argv[1])
    command = sys.argv[2]
    
    minimal_interesting_subset = delta_debugging(n, command)
    print(minimal_interesting_subset)
