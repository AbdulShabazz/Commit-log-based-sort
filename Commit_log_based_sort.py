import time

class CommitLogEntry:
    def __init__(self, commit_type, value):
        self.commit_type = commit_type  # 'min', 'max', or 'count'
        self.value = value              # New min_val, max_val, or count

def process_elements_with_min_max(input_sequence):
    commit_log = []
    count_map = {}
    min_val = None
    max_val = None
    min_commits = []
    max_commits = []
    last_count_commit_index = None

    for element in input_sequence:
        # Handle count updates
        if element in count_map:
            count_map[element] += 1
            # Overwrite the last count commit if it exists
            if last_count_commit_index is not None and commit_log[last_count_commit_index].commit_type == 'count':
                commit_log[last_count_commit_index].value = count_map[element]
            else:
                # Add a new count commit
                commit_log.append(CommitLogEntry('count', count_map[element]))
                last_count_commit_index = len(commit_log) - 1
        else:
            # New unique element
            count_map[element] = 1
            # Add a new count commit
            commit_log.append(CommitLogEntry('count', count_map[element]))
            last_count_commit_index = len(commit_log) - 1

        # Handle min_val updates
        if min_val is None or element < min_val:
            min_val = element
            commit_log.append(CommitLogEntry('min', min_val))
            min_commits.append(min_val)
            last_count_commit_index = None  # Reset count commit index

        # Handle max_val updates
        elif max_val is None or element > max_val:
            max_val = element
            commit_log.append(CommitLogEntry('max', max_val))
            max_commits.append(max_val)
            last_count_commit_index = None  # Reset count commit index

        # If neither min nor max changes, do nothing additional

    return commit_log, min_commits, max_commits, count_map

def reconstruct_sorted_unique_with_min_max(min_commits, max_commits, count_map):
    # Extract all unique values
    all_unique = set(count_map.keys())
    min_unique = set(min_commits)
    max_unique = set(max_commits)
    extreme_unique = min_unique.union(max_unique)
    non_extreme_unique = all_unique - extreme_unique

    # Sort non-extreme unique values
    sorted_non_extreme = sorted(non_extreme_unique)

    # Combine sorted non-extreme values with sorted min and max commits
    sorted_min_commits = sorted(min_unique)
    sorted_max_commits = sorted(max_unique)

    sorted_unique = sorted_non_extreme + sorted_min_commits + sorted_max_commits

    # Remove duplicates and sort the entire list
    sorted_unique = sorted(set(sorted_unique))

    return sorted_unique

def replay_commit_log_with_min_max(commit_log, sorted_unique, count_map, sort_order='ascending'):
    sorted_sequence = []
    if sort_order == 'ascending':
        traversal = sorted_unique
    else:
        traversal = reversed(sorted_unique)

    for value in traversal:
        count = count_map[value]
        sorted_sequence.extend([value] * count)

    return sorted_sequence

# Example Usage
if __name__ == "__main__":
    input_sequence = [5, 3, 8, 3, 9, 1, 5]
    commit_log, min_commits, max_commits, count_map = process_elements_with_min_max(input_sequence)

    print(f"\nInitializing commit log for unique_sort... [00:00:00]")
    start_time = time.time()
    sorted_unique = reconstruct_sorted_unique_with_min_max(min_commits, max_commits, count_map)
    end_time = time.time()
    total_runtime = end_time - start_time
    print(f"Commit log completed.      [{total_runtime:.4f}] seconds.\n")

    print(f"Initializing commit log for Ascending sort... [00:00:00]")
    start_time = time.time()
    sorted_asc = replay_commit_log_with_min_max(commit_log, sorted_unique, count_map, 'ascending')
    end_time = time.time()
    total_runtime = end_time - start_time
    print(f"Commit log completed.      [{total_runtime:.4f}] seconds.\n")

    print(f"Initializing commit log for Descending sort... [00:00:00]")
    start_time = time.time()
    sorted_desc = replay_commit_log_with_min_max(commit_log, sorted_unique, count_map, 'descending')
    end_time = time.time()
    total_runtime = end_time - start_time
    print(f"Commit log completed.      [{total_runtime:.4f}] seconds.\n")

    # Display Commit Log
    print("Commit Log:")
    for idx, entry in enumerate(commit_log):
        print(f"{idx + 1}. {entry.commit_type.upper()}: {entry.value}")

    # Display Sorted Unique and Sorted Sequences
    print("\nSorted Unique:", sorted_unique)
    print("Ascending:", sorted_asc)
    print("Descending:", sorted_desc)
