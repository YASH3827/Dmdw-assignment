def get_transactions(file_path):
    transactions = []
    with open(file_path, 'r') as file:
        for line in file:
            transactions.append(list(map(int, line.strip().split())))
    return transactions


def find_error(file1, file2):
    transactions1 = get_transactions(file1)
    transactions2 = get_transactions(file2)

    if len(transactions1) != len(transactions2):
        print("Number of transactions does not match")
        return

    for i, (trans1, trans2) in enumerate(zip(transactions1, transactions2)):
        if sorted(trans1) != sorted(trans2):
            print(f"Transaction {i + 1} does not match")
            return

    print("No error!")


if __name__ == "__main__":
    original_file = 'D_medium.dat'
    decompressed_file = 'decompressed.dat'
    find_error(original_file, decompressed_file)
