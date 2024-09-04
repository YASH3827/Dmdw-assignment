import time
from fptree import FpTree


def delete_after_blank_lines(file_path, blank_lines_to_find=1):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    blank_lines_count = 0
    index_to_cut = len(lines)
    for i, line in enumerate(lines):
        if not line.strip():
            blank_lines_count += 1
            if blank_lines_count == blank_lines_to_find:
                index_to_cut = i
                break

    with open(file_path, 'w') as file:
        file.writelines(lines[:index_to_cut])


def data_compression(input_file, output_file):
    start_time = time.time()

    transactions = []
    with open(input_file, 'r') as file:
        for line in file:
            transactions.append(list(map(int, line.strip().split())))

    min_support_thresholds = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.35, 0.3, 0.25, 0.2, 0.175, 0.15, 0.125, 0.1, 0.075,
                              0.05, 0.025, 0.01, 0.005, 0.0025, 0.001]
    compression_dict = {}
    replacement_value = -1

    for threshold in min_support_thresholds:
        print(f"Processing threshold: {threshold}")
        tree = FpTree(transactions, int(threshold * len(transactions)))
        patterns = tree.mine_patterns()

        print(f"Patterns found: {len(patterns)}")

        for pattern in patterns:
            if len(pattern) > 1:
                frozen_pattern = frozenset(pattern)
                if frozen_pattern not in compression_dict:
                    compression_dict[frozen_pattern] = replacement_value
                    replacement_value -= 1

    print(f"Compression dict size: {len(compression_dict)}")

    compressed_transactions = []
    for transaction in transactions:
        transaction = set(transaction)
        compressed_transaction = set()
        for pattern in compression_dict.keys():
            if pattern.issubset(transaction):
                transaction.difference_update(pattern)
                compressed_transaction.add(compression_dict[pattern])
        compressed_transaction.update(transaction)  # Add remaining items
        compressed_transactions.append(sorted(compressed_transaction))

    with open(output_file, 'w') as file:
        for pattern, value in compression_dict.items():
            sorted_pattern = sorted(filter(lambda x: x is not None, pattern))
            file.write(f"{value} " + " ".join(map(str, sorted_pattern)) + "\n")
        file.write("\n")
        for transaction in compressed_transactions:
            file.write(" ".join(map(str, transaction)) + "\n")

    delete_after_blank_lines(output_file)

    end_time = time.time()
    print(f"Compression complete. Output saved to {output_file}.")
    print(f"Elapsed time: {end_time - start_time} seconds")


if __name__ == "__main__":
    input_file = 'D_medium.dat'
    output_file = 'D_medium_compressed.dat'
    data_compression(input_file, output_file)
    print(f"Compression complete. Output saved to {output_file}.")
