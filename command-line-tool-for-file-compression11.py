# Command-Line_Tool_for_File_Compression
# Develop a command-line tool that can compress and decompress files using various algorithms like Huffman Coding or LZW.
# Huffman Coding

import heapq
import os
from collections import defaultdict

# Huffman Node


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

# Build the Huffman Tree


def build_huffman_tree(freq_map):
    heap = [Node(char, freq) for char, freq in freq_map.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

# Generate the Huffman Codes


def generate_codes(root, current_code, codes):
    if root is None:
        return
    if root.char is not None:
        codes[root.char] = current_code
        return
    generate_codes(root.left, current_code + "0", codes)
    generate_codes(root.right, current_code + "1", codes)

# Compress a file using Huffman Coding


def huffman_compress(file_path):
    # Read file content
    with open(file_path, 'r') as f:
        content = f.read()

    # Calculate frequency of each character
    freq_map = defaultdict(int)
    for char in content:
        freq_map[char] += 1

    # Build the Huffman Tree
    root = build_huffman_tree(freq_map)

    # Generate Huffman Codes
    codes = {}
    generate_codes(root, "", codes)

    # Encode the content
    encoded_content = ''.join(codes[char] for char in content)

    # Save the encoded content and the frequency map to a file
    compressed_file = file_path + ".huff"
    with open(compressed_file, 'w') as f:
        f.write(f"{freq_map}\n{encoded_content}")

    print(f"File compressed to {compressed_file}")

# Decompress a Huffman encoded file


def huffman_decompress(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Read the frequency map and encoded content
    freq_map = eval(lines[0].strip())
    encoded_content = lines[1].strip()

    # Build the Huffman Tree
    root = build_huffman_tree(freq_map)

    # Decode the content
    decoded_content = []
    current_node = root
    for bit in encoded_content:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_content.append(current_node.char)
            current_node = root

    # Save the decoded content
    decompressed_file = file_path.replace(".huff", "_decompressed.txt")
    with open(decompressed_file, 'w') as f:
        f.write(''.join(decoded_content))

    print(f"File decompressed to {decompressed_file}")
