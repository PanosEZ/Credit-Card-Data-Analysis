import random
from collections import defaultdict
import time
import matplotlib.pyplot as plt


# Part 1: Generating Credit Card Charges
def generate_credit_card_numbers(num_cards):
    card_numbers = set()
    while len(card_numbers) < num_cards:
        card_number = str(random.randint(4000000000000000, 4999999999999999))
        card_numbers.add(card_number)
    return list(card_numbers)

def generate_charges(num_charges, card_numbers):
    charges = []
    for _ in range(num_charges):
        card = random.choice(card_numbers)
        amount = random.uniform(10, 1000)
        charges.append((card, round(amount, 2)))
    return charges

# Part 2: Data Processing and Analysis
def process_charges(charges):
    total_amounts = defaultdict(float)
    transaction_counts = defaultdict(int)

    for card, amount in charges:
        total_amounts[card] += amount
        transaction_counts[card] += 1

    card_min_payment = min(total_amounts, key=total_amounts.get)
    card_max_payment = max(total_amounts, key=total_amounts.get)
    card_min_transactions = min(transaction_counts, key=transaction_counts.get)
    card_max_transactions = max(transaction_counts, key=transaction_counts.get)

    return {
        'min_payment': (card_min_payment, total_amounts[card_min_payment]),
        'max_payment': (card_max_payment, total_amounts[card_max_payment]),
        'min_transactions': (card_min_transactions, transaction_counts[card_min_transactions]),
        'max_transactions': (card_max_transactions, transaction_counts[card_max_transactions])
    }

# Part 3: Implementing a Hash Table
class LinearProbingHashTable:
    def __init__(self, initial_size=103):
        self.size = initial_size
        self.count = 0
        self.keys = [None] * self.size
        self.values = [None] * self.size

    def _hash(self, key):
        return hash(key) % self.size

    def _rehash(self, old_hash):
        return (old_hash + 1) % self.size

    def _resize(self):
        old_keys = self.keys
        old_values = self.values
        self.size = next_prime(2 * self.size)
        self.keys = [None] * self.size
        self.values = [None] * self.size
        self.count = 0

        for key, value in zip(old_keys, old_values):
            if key is not None:
                self.put(key, value)

    def put(self, key, value):
        if self.count / self.size >= 0.7:
            self._resize()

        hash_value = self._hash(key)

        while self.keys[hash_value] is not None:
            if self.keys[hash_value] == key:
                self.values[hash_value] = value
                return
            hash_value = self._rehash(hash_value)

        self.keys[hash_value] = key
        self.values[hash_value] = value
        self.count += 1

    def get(self, key):
        hash_value = self._hash(key)

        while self.keys[hash_value] is not None:
            if self.keys[hash_value] == key:
                return self.values[hash_value]
            hash_value = self._rehash(hash_value)

        return None

def next_prime(n):
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

    while True:
        if is_prime(n):
            return n
        n += 1

# Part 4: Data Analysis Using Hash Table
def process_charges_with_hash_table(charges, hash_table):
    for card, amount in charges:
        if hash_table.get(card) is None:
            hash_table.put(card, amount)
        else:
            existing_amount = hash_table.get(card)
            hash_table.put(card, existing_amount + amount)

    total_amounts = {key: value for key, value in zip(hash_table.keys, hash_table.values) if key is not None}
    transaction_counts = defaultdict(int)
    for card, _ in charges:
        transaction_counts[card] += 1

    card_min_payment = min(total_amounts, key=total_amounts.get)
    card_max_payment = max(total_amounts, key=total_amounts.get)
    card_min_transactions = min(transaction_counts, key=transaction_counts.get)
    card_max_transactions = max(transaction_counts, key=transaction_counts.get)

    return {
        'min_payment': (card_min_payment, total_amounts[card_min_payment]),
        'max_payment': (card_max_payment, total_amounts[card_max_payment]),
        'min_transactions': (card_min_transactions, transaction_counts[card_min_transactions]),
        'max_transactions': (card_max_transactions, transaction_counts[card_max_transactions])
    }

# Main execution
def main():
    sizes = [2000000, 4000000, 6000000]
    execution_times_hash_table = []
    execution_times_no_hash_table = []

    for size in sizes:
        credit_card_numbers = generate_credit_card_numbers(size)
        credit_card_charges = generate_charges(1000000, credit_card_numbers)

        # Process charges without hash table
        start_time = time.time()
        stats = process_charges(credit_card_charges)
        end_time = time.time()
        execution_times_no_hash_table.append(end_time - start_time)

        # Process charges with hash table
        hash_table = LinearProbingHashTable()
        start_time_hash_table = time.time()
        stats_with_hash_table = process_charges_with_hash_table(credit_card_charges, hash_table)
        end_time_hash_table = time.time()
        execution_times_hash_table.append(end_time_hash_table - start_time_hash_table)

        # Print statistics for the current dataset size
        print(f"Statistics for {size} charges:")
        print("Without Hash Table:")
        print(f"Card with the smallest total payment: {stats['min_payment'][0]}, Payment amount: {stats['min_payment'][1]:.2f}")
        print(f"Card with the largest total payment: {stats['max_payment'][0]}, Payment amount: {stats['max_payment'][1]:.2f}")
        print(f"Card with the fewest transactions: {stats['min_transactions'][0]}, Number of transactions: {stats['min_transactions'][1]}")
        print(f"Card with the most transactions: {stats['max_transactions'][0]}, Number of transactions: {stats['max_transactions'][1]}")
        print(f"Execution time (without Hash Table): {end_time - start_time:.2f} seconds\n")

        print("With Hash Table:")
        print(f"Card with the smallest total payment: {stats_with_hash_table['min_payment'][0]}, Payment amount: {stats_with_hash_table['min_payment'][1]:.2f}")
        print(f"Card with the largest total payment: {stats_with_hash_table['max_payment'][0]}, Payment amount: {stats_with_hash_table['max_payment'][1]:.2f}")
        print(f"Card with the fewest transactions: {stats_with_hash_table['min_transactions'][0]}, Number of transactions: {stats_with_hash_table['min_transactions'][1]}")
        print(f"Card with the most transactions: {stats_with_hash_table['max_transactions'][0]}, Number of transactions: {stats_with_hash_table['max_transactions'][1]}")
        print(f"Execution time (with Hash Table): {end_time_hash_table - start_time_hash_table:.2f} seconds\n")

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, execution_times_hash_table, label='With Hash Table')
    plt.plot(sizes, execution_times_no_hash_table, label='Without Hash Table')
    plt.xlabel('Number of Charges')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time vs. Number of Charges')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
