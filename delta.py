import subprocess
import sys

def is_interesting(command, subset):
    try:
        # 运行命令并传入子集作为参数
        result = subprocess.Popen(
            command.split() + list(map(str, subset)), 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        result.communicate()  # 等待命令执行完成
        # 如果返回值为1，则子集“有趣”
        return result.returncode == 1
    except subprocess.CalledProcessError as e:
        print("Error running command: {}".format(e), file=sys.stderr)
        return False

def DD(command, P, C):
    n = len(C)
    if n == 1:
        return C
    mid = n // 2
    P1 = C[:mid]
    P2 = C[mid:]
    if is_interesting(command, P + P1):
        return DD(command, P, P1)
    elif is_interesting(command, P + P2):
        return DD(command, P, P2)
    else:
        return DD(command, P + P2, P1) + DD(command, P + P1, P2)

def main(n, command):
    # 创建一个从0到n-1的列表
    full_set = list(range(n))
    # 调用DD函数，并对结果排序，去除重复项
    minimal_interesting_subset = sorted(set(DD(command, [], full_set)))
    print(minimal_interesting_subset)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: {} <size_n> <command>".format(sys.argv[0]))
        sys.exit(1)
    
    size_n = int(sys.argv[1])
    command_to_run = sys.argv[2]
    main(size_n, command_to_run)
