import subprocess
import re
import os

# 初始化探测计数器
probes_counter = 0

def get_coverage(test_files):
    global probes_counter
    # 每次探测时递增计数器
    probes_counter += 1
    
    # 调用 Bash 脚本运行测试并获取覆盖率
    subprocess.run(['./run_coverage.sh'] + test_files, stdout=subprocess.PIPE)

    # 解析 gcov 的输出来获取覆盖率
    coverage_output = subprocess.check_output(["gcov", "-s", TEST_DIR, "*.c"], universal_newlines=True)
    coverage_percentage = re.search(r'Lines executed:(\d+.\d+)% of \d+', coverage_output)
    if coverage_percentage:
        return float(coverage_percentage.group(1))
    else:
        raise RuntimeError("Unable to find coverage percentage in gcov output.")

def delta_debug(tests, target_coverage):
    global probes_counter
    if len(tests) <= 1:
        # 如果测试集只有一个测试，这就是最小的有趣测试集
        return tests

    # 将测试集一分为二
    split_point = len(tests) // 2
    first_half = tests[:split_point]
    second_half = tests[split_point:]

    # 在第一半测试集上进行探测
    coverage_1 = get_coverage(first_half)
    if coverage_1 >= target_coverage:
        return delta_debug(first_half, target_coverage)
    
    # 在第二半测试集上进行探测
    coverage_2 = get_coverage(second_half)
    if coverage_2 >= target_coverage:
        return delta_debug(second_half, target_coverage)

    # 如果两半分开都没有达到目标覆盖率，合并它们
    combined_coverage = get_coverage(first_half + second_half)
    if combined_coverage >= target_coverage:
        return delta_debug(first_half + second_half, target_coverage)
    
    return first_half + second_half

if __name__ == "__main__":
    test_files = os.listdir('/path/to/png/test/dir')  # 替换为你的测试文件夹
    target_coverage = 39.66  # 目标覆盖率
    minimal_test_set = delta_debug(test_files, target_coverage)
    print("Found minimal interesting test set:", minimal_test_set)
    print("Number of probes needed:", probes_counter)
