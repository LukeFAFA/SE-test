import subprocess
import re
import os

# 测试文件夹路径和脚本路径
TEST_DIR = '/path/to/hwtest'
SCRIPT_DIR = '/path/to/libpng-1.6.34'

# 初始化探测计数器
probes_counter = 0

def run_coverage(test_files):
    global probes_counter
    # 调用 Bash 脚本运行测试并获取覆盖率
    command = [os.path.join(SCRIPT_DIR, 'run_coverage.sh')] + test_files
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    probes_counter += 1  # 每次探测时递增计数器

def get_coverage():
    # 这里需要正确解析 gcov 输出的覆盖率数据
    # 假设我们有一种方法来正确地从 gcov 输出中提取覆盖率百分比
    coverage_output = subprocess.check_output(
        ["gcov", "-s", SCRIPT_DIR, "*.c"],
        cwd=SCRIPT_DIR,
        text=True
    )
    coverage_percentage = re.search(r'Lines executed:(\d+\.\d+)% of \d+', coverage_output)
    return float(coverage_percentage.group(1)) if coverage_percentage else 0.0

def delta_debug(tests, target_coverage):
    if len(tests) <= 1:
        return tests  # 不能进一步减少子集

    mid = len(tests) // 2
    first_half = tests[:mid]
    second_half = tests[mid:]

    run_coverage(first_half)
    coverage_1 = get_coverage()
    if coverage_1 >= target_coverage:
        return delta_debug(first_half, target_coverage)

    run_coverage(second_half)
    coverage_2 = get_coverage()
    if coverage_2 >= target_coverage:
        return delta_debug(second_half, target_coverage)

    # 如果两个子集合并起来没有达到目标覆盖率，则需要更多的测试用例
    return delta_debug(first_half + second_half, target_coverage)

if __name__ == "__main__":
    test_files = [f for f in os.listdir(TEST_DIR) if f.endswith('.png')]
    target_coverage = 39.66  # 目标覆盖率

    run_coverage(test_files)  # 初始覆盖率检查
    actual_coverage = get_coverage()
    print(f"Actual initial coverage: {actual_coverage}%")
    
    if actual_coverage >= target_coverage:
        minimal_tests = delta_debug(test_files, target_coverage)
        print(f"Minimal test subset with the same coverage: {minimal_tests}")
    else:
        print("Initial coverage is less than target coverage.")

    print(f"Number of probes needed: {probes_counter}")
