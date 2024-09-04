def decompress(output_file, input_file):
    conversion_dict = {}
    transactions = []

    with open(input_file, 'r') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines) and lines[i].strip():
        parts = list(map(int, lines[i].strip().split()))
        key = parts[0]
        items = parts[1:]
        conversion_dict[key] = items
        i += 1

    i += 1

    while i < len(lines):
        transaction = list(map(int, lines[i].strip().split()))
        expanded_transaction = []
        for item in transaction:
            if item in conversion_dict:
                expanded_transaction.extend(conversion_dict[item])
            else:
                expanded_transaction.append(item)
        transactions.append(expanded_transaction)
        i += 1

    with open(output_file, 'w') as file:
        for transaction in transactions:
            file.write(" ".join(map(str, transaction)) + "\n")

    original_data_file = 'D_medium.dat'
    with open(original_data_file, 'r') as file:
        original_data = file.read()

    with open(output_file, 'a') as file:
        file.write(original_data)


if __name__ == "__main__":
    input_file = 'D_medium_compressed.dat'
    output_file = 'decompressed.dat'
    decompress(output_file, input_file)
    print(f"Decompression complete. Output saved to {output_file}.")
