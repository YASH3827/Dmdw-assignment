from collections import defaultdict
from itertools import combinations
import time


class FpNode:
    def __init__(self, item, parent=None):
        self.item = item
        self.frequency = 1
        self.next_node_in_ht = None
        self.parent = parent
        self.children = {}


class FpTree:
    def __init__(self, transactions=None, min_support_threshold=0):
        self.root = FpNode(None)
        self.header_table = defaultdict(list)
        self.item_frequencies = defaultdict(int)
        self.min_support_threshold = min_support_threshold
        self.total_transactions = 0
        self.total_items = 0

        if transactions:
            self.build_tree(transactions)

    def build_tree(self, transactions):
        for transaction in transactions:
            self.total_transactions += 1
            for item in transaction:
                self.item_frequencies[item] += 1
                self.total_items += 1

        # Filter items by minimum support threshold
        self.item_frequencies = {k: v for k, v in self.item_frequencies.items() if v >= self.min_support_threshold}

        for transaction in transactions:
            transaction = [item for item in transaction if item in self.item_frequencies]
            transaction.sort(key=lambda item: self.item_frequencies[item], reverse=True)
            self.insert_tree(transaction)

    def insert_tree(self, transaction):
        current_node = self.root
        for item in transaction:
            if item not in current_node.children:
                new_node = FpNode(item, current_node)
                current_node.children[item] = new_node
                self.header_table[item].append(new_node)
            else:
                current_node.children[item].frequency += 1
            current_node = current_node.children[item]

    def mine_patterns(self, timeout=600):
        start_time = time.time()
        patterns = []

        for item in sorted(self.item_frequencies, key=self.item_frequencies.get):
            conditional_tree = self.build_conditional_tree(item)
            if time.time() - start_time > timeout:
                break
            if self.contains_single_path(conditional_tree.root):
                patterns.extend(self.generate_patterns_from_single_path(conditional_tree.root))
            else:
                patterns.extend(conditional_tree.mine_patterns(timeout - (time.time() - start_time)))

        return patterns

    def build_conditional_tree(self, item):
        conditional_patterns = []
        for node in self.header_table[item]:
            path = []
            current_node = node.parent
            while current_node and current_node.item is not None:
                path.append(current_node.item)
                current_node = current_node.parent
            for _ in range(node.frequency):
                conditional_patterns.append(path)
        return FpTree(conditional_patterns, self.min_support_threshold)

    def contains_single_path(self, node):
        while len(node.children) == 1:
            node = next(iter(node.children.values()))
        return len(node.children) == 0

    def generate_patterns_from_single_path(self, node):
        patterns = []
        items = []
        while node:
            items.append(node.item)
            if node.parent:
                patterns.extend([set(combination) for combination in combinations(items, len(items))])
            node = next(iter(node.children.values()), None)
        return patterns
