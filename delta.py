import sys
import subprocess

def is_interesting(subset, command):
    try:
        result = subprocess.run(command + subset, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return result.returncode == 1
    except subprocess.CalledProcessError as e:
        print('Error:', e, file=sys.stderr)
        return False
    except Exception as e:
        print('Unexpected error:', e, file=sys.stderr)
        return False

def delta_debug(n, is_interesting_func):
    test_config = list(range(n))
    def minimize(subset):
        if not is_interesting_func(subset):
            return []
        for i in range(len(subset)):
            smaller_subset = subset[:i] + subset[i+1:]
            if is_interesting_func(smaller_subset):
                return minimize(smaller_subset)
        return subset
    return minimize(test_config)


if __name__ == "__main__":
    n = int(sys.argv[1])
    cmd = sys.argv[2]
    command = cmd.split(' ')
    try:
        interesting_subset = delta_debug(n, command)
        print(interesting_subset)
    except Exception as e:
        print("Error during delta debugging:", e, file=sys.stderr)
