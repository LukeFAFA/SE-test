import subprocess

def is_interesting(command, subset):
    try:
        cmd = command.split() + [str(s) for s in subset]
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result.communicate()
        return result.returncode == 1
    except Exception as e:
        print "Error running command: {0}".format(e)
        return False

def delta_debug(command, current_set):
    if len(current_set) == 1:
        return current_set

    # Divide the set into two subsets
    mid = len(current_set) // 2
    set1 = current_set[:mid]
    set2 = current_set[mid:]

    # Test each subset to see if it is interesting
    if is_interesting(command, set1 + current_set):
        return delta_debug(command, set1)
    if is_interesting(command, set2 + current_set):
        return delta_debug(command, set2)

    # If neither subset is interesting on its own, return the combination
    return delta_debug(command, set1) + delta_debug(command, set2)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print "Usage: python delta.py <size_n> <command>"
        sys.exit(1)
    
    n = int(sys.argv[1])
    command = sys.argv[2]
    
    full_set = range(n)
    minimal_interesting_subset = delta_debug(command, full_set)
    print minimal_interesting_subset
