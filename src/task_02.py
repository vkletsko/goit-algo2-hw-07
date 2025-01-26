import timeit
from functools import lru_cache
import matplotlib.pyplot as plt


@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


class SplayTreeNode:
    def __init__(self, data, parent=None, value=None):
        self.data = data
        self.parent = parent
        self.left_node = None
        self.right_node = None
        self.value = value


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, data, value):
        if self.root is None:
            self.root = SplayTreeNode(data, value=value)
        else:
            self.insert_node(data, value, self.root)

    def insert_node(self, data, value, current_node):
        if data < current_node.data:
            if current_node.left_node:
                self.insert_node(data, value, current_node.left_node)
            else:
                current_node.left_node = SplayTreeNode(
                    data, current_node, value)
        else:
            if current_node.right_node:
                self.insert_node(data, value, current_node.right_node)
            else:
                current_node.right_node = SplayTreeNode(
                    data, current_node, value)

    def find(self, data):
        node = self.root
        while node is not None:
            if data < node.data:
                node = node.left_node
            elif data > node.data:
                node = node.right_node
            else:
                self.splay(node)
                return node.value
        return None

    def splay(self, node):
        while node.parent is not None:
            if node.parent.parent is None:
                if node == node.parent.left_node:
                    self.rotate_right(node.parent)
                else:
                    self.rotate_left(node.parent)
            elif node == node.parent.left_node and node.parent == node.parent.parent.left_node:
                self.rotate_right(node.parent.parent)
                self.rotate_right(node.parent)
            elif node == node.parent.right_node and node.parent == node.parent.parent.right_node:
                self.rotate_left(node.parent.parent)
                self.rotate_left(node.parent)
            else:
                if node == node.parent.left_node:
                    self.rotate_right(node.parent)
                    self.rotate_left(node.parent)
                else:
                    self.rotate_left(node.parent)
                    self.rotate_right(node.parent)

    def rotate_right(self, node):
        left_child = node.left_node
        if left_child is None:
            return

        node.left_node = left_child.right_node
        if left_child.right_node:
            left_child.right_node.parent = node

        left_child.parent = node.parent
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.left_node:
            node.parent.left_node = left_child
        else:
            node.parent.right_node = left_child

        left_child.right_node = node
        node.parent = left_child

    def rotate_left(self, node):
        right_child = node.right_node
        if right_child is None:
            return

        node.right_node = right_child.left_node
        if right_child.left_node:
            right_child.left_node.parent = node

        right_child.parent = node.parent
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left_node:
            node.parent.left_node = right_child
        else:
            node.parent.right_node = right_child

        right_child.left_node = node
        node.parent = right_child


def fibonacci_splay(n, tree):
    if n <= 1:
        return n

    cached_value = tree.find(n)
    if cached_value is not None:
        return cached_value

    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


def compare():
    steps = list(range(0, 951, 50))
    lru_times = []
    splay_times = []

    for n in steps:
        lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=1)
        lru_times.append(lru_time)

        tree = SplayTree()
        splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=1)
        splay_times.append(splay_time)

    print("n\tLRU Cache (s)\tSplay Tree (s)")
    for i, n in enumerate(steps):
        print(f"{n}\t{lru_times[i]:.6f}\t\t{splay_times[i]:.6f}")
    draw_plot(steps, lru_times, splay_times)


def draw_plot(steps, lru_times, splay_times):
    lru_times = [time for time in lru_times]
    splay_times = [time for time in splay_times]

    plt.figure(figsize=(10, 6))
    plt.plot(steps, lru_times, label='LRU Cache', color='b', marker='o')
    plt.plot(steps, splay_times, label='Splay Tree', color='g', marker='o')

    plt.title("LRU Cache vs Splay Tree")
    plt.xlabel("n - Число Фибоначчи")
    plt.ylabel("Час виконання (с)")

    plt.xlim(min(steps), max(steps))

    plt.xticks(steps, rotation=45)
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


compare()
