"""
Assignment 2 starter code
CSC148, Winter 2022
Instructors: Bogdan Simion, Sonya Allin, and Pooja Vashisth

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Bogdan Simion, Dan Zingaro
"""
from __future__ import annotations

import time

from huffman import HuffmanTree
from utils import *


# ====================
# Functions for compression


def build_frequency_dict(text: bytes) -> dict[int, int]:
    """ Return a dictionary which maps each of the bytes in <text> to its
    frequency.

    >>> d = build_frequency_dict(bytes([65, 66, 67, 66]))
    >>> d == {65: 1, 66: 2, 67: 1}
    True
    """
    d = {}
    for i in text:
        if i not in d:
            d[i] = 1
        else:
            d[i] = d[i] + 1
    return d


def build_huffman_tree(freq_dict: dict[int, int]) -> HuffmanTree:
    """ Return the Huffman tree corresponding to the frequency dictionary
    <freq_dict>.

    Precondition: freq_dict is not empty.

    >>> freq = {2: 6, 3: 4}
    >>> t = build_huffman_tree(freq)
    >>> result = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> t == result
    True
    >>> freq = {2: 6, 3: 4, 7: 5}
    >>> t = build_huffman_tree(freq)
    >>> result = HuffmanTree(None, HuffmanTree(2), \
                             HuffmanTree(None, HuffmanTree(3), HuffmanTree(7)))
    >>> t == result
    True
    >>> import random
    >>> symbol = random.randint(0,255)
    >>> freq = {symbol: 6}
    >>> t = build_huffman_tree(freq)
    >>> any_valid_byte_other_than_symbol = (symbol + 1) % 256
    >>> dummy_tree = HuffmanTree(any_valid_byte_other_than_symbol)
    >>> result = HuffmanTree(None, HuffmanTree(symbol), dummy_tree)
    >>> t.left == result.left or t.right == result.left
    True
    """
    if len(freq_dict) == 1:
        f = list(freq_dict.items())
        if f[0][0] < 255:
            h = HuffmanTree(None, HuffmanTree(f[0][0]),
                            HuffmanTree(f[0][0] + 1))

        else:
            h = HuffmanTree(None, HuffmanTree(0), HuffmanTree(f[0][0]))
        h.number = f[0][1]
        return h
    elif len(freq_dict) == 0:
        return HuffmanTree(None)
    else:
        lst = list(freq_dict.items())
        sorted_freq = []
        for i in freq_dict:
            sorted_freq.append(freq_dict[i])
        sorted_freq.sort(reverse=True)
        while len(lst) >= 2:
            min1 = 0
            min2 = 0
            for k in lst:
                if k[1] == sorted_freq[-1] and min1 == 0:
                    min1 = k
                elif k[1] == sorted_freq[-2]:
                    min2 = k
                if min1 != 0 and min2 != 0:
                    break
            lst.remove(min1)
            lst.remove(min2)
            if isinstance(min1[0], HuffmanTree) and\
                    isinstance(min2[0], HuffmanTree):
                h = HuffmanTree(None, min1[0], min2[0])
            elif isinstance(min1[0], HuffmanTree):
                h = HuffmanTree(None, min1[0], HuffmanTree(min2[0]))
            elif isinstance(min2[0], HuffmanTree):
                h = HuffmanTree(None, HuffmanTree(min1[0]), min2[0])
            else:
                h = HuffmanTree(None, HuffmanTree(min1[0]),
                                HuffmanTree(min2[0]))
            h.number = min1[1] + min2[1]
            lst.append((h, h.number))
            sorted_freq.pop(-1)
            sorted_freq.pop(-1)
            sorted_freq.append(h.number)
            sorted_freq.sort(reverse=True)
            if len(sorted_freq) <= 1:
                return h


def get_codes(tree: HuffmanTree) -> dict[int, str]:
    """ Return a dictionary which maps symbols from the Huffman tree <tree>
    to codes.

    >>> tree = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> d = get_codes(tree)
    >>> d == {3: "0", 2: "1"}
    True
    """
    d = {}

    if not tree.is_leaf():
        if tree.left.symbol is not None:
            d[tree.left.symbol] = '0'
        else:
            d.update(_helper_get_code(tree.left, '0'))
        if tree.right.symbol is not None:
            d[tree.right.symbol] = '1'
        else:
            d.update(_helper_get_code(tree.right, '1'))
    return d


def _helper_get_code(tree: HuffmanTree, s: str) -> dict[int, str]:
    d = {}
    if tree.left.symbol is not None:
        d.update({tree.left.symbol: s + '0'})
    else:
        d.update(_helper_get_code(tree.left, s + '0'))
    if tree.right.symbol is not None:
        d.update({tree.right.symbol: s + '1'})
    else:
        d.update(_helper_get_code(tree.right, s + '1'))
    return d


def number_nodes(tree: HuffmanTree) -> None:
    """ Number internal nodes in <tree> according to postorder traversal. The
    numbering starts at 0.

    >>> left = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> right = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> tree = HuffmanTree(None, left, right)
    >>> number_nodes(tree)
    >>> tree.left.number
    0
    >>> tree.right.number
    1
    >>> tree.number
    2
    """
    count = 0
    f = 0
    r = 0
    if not tree.left.is_leaf():
        f = _helper_number_nodes(tree.left, count)
    if not tree.right.is_leaf():
        r = _helper_number_nodes(tree.right, f)
    if r == 0:
        tree.number = f
    else:
        tree.number = r


def _helper_number_nodes(tree: HuffmanTree, c: int) -> int:
    if not tree.left.is_leaf():
        # helper_number_nodes(tree.left, c)
        c = _helper_number_nodes(tree.left, c)
    if not tree.right.is_leaf():
        # helper_number_nodes(tree.right, c)
        c = _helper_number_nodes(tree.right, c)
    tree.number = c
    c += 1
    return c


def avg_length(tree: HuffmanTree, freq_dict: dict[int, int]) -> float:
    """ Return the average number of bits required per symbol, to compress the
    text made of the symbols and frequencies in <freq_dict>, using the Huffman
    tree <tree>.

    The average number of bits = the weighted sum of the length of each symbol
    (where the weights are given by the symbol's frequencies), divided by the
    total of all symbol frequencies.
    >>> freq = {3: 2, 2: 7, 9: 1}
    >>> left = HuffmanTree(None, HuffmanTree(3), HuffmanTree(2))
    >>> right = HuffmanTree(9)
    >>> tree = HuffmanTree(None, left, right)
    >>> avg_length(tree, freq)  # (2*2 + 7*2 + 1*1) / (2 + 7 + 1)
    1.9
    """
    d = get_codes(tree)
    total = 0
    fre = 0
    for i in d:
        total = total + (len(d[i]) * freq_dict[i])
        fre += freq_dict[i]
    try:
        return total / fre
    except ZeroDivisionError:
        return 0


def compress_bytes(text: bytes, codes: dict[int, str]) -> bytes:
    """ Return the compressed form of <text>, using the mapping from <codes>
    for each symbol.

    >>> d = {0: "0", 1: "10", 2: "11"}
    >>> text = bytes([1, 2, 1, 0])
    >>> result = compress_bytes(text, d)
    >>> result == bytes([184])
    True
    >>> [byte_to_bits(byte) for byte in result]
    ['10111000']
    >>> text = bytes([1, 2, 1, 0, 2])
    >>> result = compress_bytes(text, d)
    >>> [byte_to_bits(byte) for byte in result]
    ['10111001', '10000000']
    """
    s = ''
    t = ()
    for i in text:
        s += codes[i]
        if len(s) >= 8:
            s, s2 = s[: 8], s[8:]
            s = bits_to_byte(s)
            t += (s, )
            s = s2
    s = bits_to_byte(s)
    t += (s, )
    k = bytes(0)
    for i in t:
        k += bytes([i])
    return k


def tree_to_bytes(tree: HuffmanTree) -> bytes:
    """ Return a bytes representation of the Huffman tree <tree>.
    The representation should be based on the postorder traversal of the tree's
    internal nodes, starting from 0.

    Precondition: <tree> has its nodes numbered.

    >>> tree = HuffmanTree(None, HuffmanTree(3, None, None), \
    HuffmanTree(2, None, None))
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2]
    >>> left = HuffmanTree(None, HuffmanTree(3, None, None), \
    HuffmanTree(2, None, None))
    >>> right = HuffmanTree(5)
    >>> tree = HuffmanTree(None, left, right)
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))
    [0, 3, 0, 2, 1, 0, 0, 5]
    >>> tree = build_huffman_tree(build_frequency_dict(b"helloworld"))
    >>> number_nodes(tree)
    >>> list(tree_to_bytes(tree))\
            #doctest: +NORMALIZE_WHITESPACE
    [0, 104, 0, 101, 0, 119, 0, 114, 1, 0, 1, 1, 0, 100, 0, 111, 0, 108,\
    1, 3, 1, 2, 1, 4]
    """
    t = bytes(0)
    i = 0
    if tree.number == 0:
        return bytes([0]) + bytes([tree.left.symbol]) + bytes(
            [0]) + bytes([tree.right.symbol])
    else:
        while i <= tree.number:
            t += _helper_tree_to_bytes(tree, i)
            i += 1
        return t


def _helper_tree_to_bytes(tree: HuffmanTree, i: int) -> bytes:
    t = bytes(0)

    if not tree.left.is_leaf():
        t += _helper_tree_to_bytes(tree.left, i)
    if not tree.right.is_leaf():
        t += _helper_tree_to_bytes(tree.right, i)
    if tree.number == i:
        if tree.left.is_leaf():
            t += bytes([0]) + bytes([tree.left.symbol])
        else:
            t += bytes([1]) + bytes([tree.left.number])
        if tree.right.is_leaf():
            t += bytes([0]) + bytes([tree.right.symbol])
        else:
            t += bytes([1]) + bytes([tree.right.number])

    return t


def compress_file(in_file: str, out_file: str) -> None:
    """ Compress contents of the file <in_file> and store results in <out_file>.
    Both <in_file> and <out_file> are string objects representing the names of
    the input and output files.

    Precondition: The contents of the file <in_file> are not empty.
    """
    with open(in_file, "rb") as f1:
        text = f1.read()
    freq = build_frequency_dict(text)
    tree = build_huffman_tree(freq)
    codes = get_codes(tree)
    number_nodes(tree)
    print("Bits per symbol:", avg_length(tree, freq))
    result = (tree.num_nodes_to_bytes() + tree_to_bytes(tree)
              + int32_to_bytes(len(text)))
    result += compress_bytes(text, codes)
    with open(out_file, "wb") as f2:
        f2.write(result)


# ====================
# Functions for decompression

def generate_tree_general(node_lst: list[ReadNode],
                          root_index: int) -> HuffmanTree:
    """ Return the Huffman tree corresponding to node_lst[root_index].
    The function assumes nothing about the order of the tree nodes in the list.

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 1, 1, 0)]
    >>> generate_tree_general(lst, 2)
    HuffmanTree(None, HuffmanTree(None, HuffmanTree(10, None, None), \
HuffmanTree(12, None, None)), \
HuffmanTree(None, HuffmanTree(5, None, None), HuffmanTree(7, None, None)))
    """

    h = HuffmanTree(None, HuffmanTree(None), HuffmanTree(None))
    _help_build_tree(node_lst[node_lst[root_index].l_data], h.left, node_lst)
    _help_build_tree(node_lst[node_lst[root_index].r_data], h.right, node_lst)
    return h


def _help_build_tree(node: ReadNode, t: HuffmanTree, node_lst: list[ReadNode]):
    if node.l_type == 0:
        t.left = HuffmanTree(node.l_data)
    else:
        k = HuffmanTree(None, HuffmanTree(None))
        _help_build_tree(node_lst[node.l_data], k.left, node_lst)
        t.left = k
    if node.r_type == 0:
        t.right = HuffmanTree(node.r_data)
    else:
        k = HuffmanTree(None, None, HuffmanTree(None))
        _help_build_tree(node_lst[node.r_data], k.right, node_lst)
        t.right = k


def generate_tree_postorder(node_lst: list[ReadNode],
                            root_index: int) -> HuffmanTree:
    """ Return the Huffman tree corresponding to node_lst[root_index].
    The function assumes that the list represents a tree in postorder.

    >>> lst = [ReadNode(0, 5, 0, 7), ReadNode(0, 10, 0, 12), \
    ReadNode(1, 0, 1, 0)]
    >>> generate_tree_postorder(lst, 2)
    HuffmanTree(None, HuffmanTree(None, HuffmanTree(5, None, None), \
HuffmanTree(7, None, None)), \
HuffmanTree(None, HuffmanTree(10, None, None), HuffmanTree(12, None, None)))
    >>> lst = [ReadNode(0, 10, 0, 12), ReadNode(0, 6, 0, 9), ReadNode(1, 0, 0, 7), ReadNode(1, 0, 1, 0)]
    >>> l = HuffmanTree(None, HuffmanTree(10), HuffmanTree(12))
    >>> r = HuffmanTree(None, HuffmanTree(None, HuffmanTree(6), HuffmanTree(9)), HuffmanTree(7))
    >>> com = HuffmanTree(None, l, r)
    >>> t1 = generate_tree_postorder(lst, 3)
    >>> t1 == com
    True
    >>> t2 = generate_tree_postorder(lst, 2)
    """

    i = root_index
    h = HuffmanTree(None, HuffmanTree(None), HuffmanTree(None))
    try:
        node_lst[i]
    except IndexError:
        return HuffmanTree(None)

    if node_lst[i].r_type == 0:
        h.right = HuffmanTree(node_lst[i].r_data)
        k = i
    else:
        k = _help_postorder(h.right, node_lst, i - 1)
    if node_lst[i].l_type == 0:
        h.left = HuffmanTree(node_lst[i].l_data)
    else:
        _help_postorder(h.left, node_lst, k - 1)
    return h


def _help_postorder(t: HuffmanTree, node_lst: list[ReadNode], i: int) -> int:
    if node_lst[i].r_type == 0:
        t.right = HuffmanTree(node_lst[i].r_data)
    else:
        t.right = HuffmanTree(None, HuffmanTree(None), HuffmanTree(None))
        i = _help_postorder(t.right, node_lst, i - 1)
    if node_lst[i].l_type == 0:
        t.left = HuffmanTree(node_lst[i].l_data)
    else:
        t.left = HuffmanTree(None, HuffmanTree(None), HuffmanTree(None))
        i = _help_postorder(t.left, node_lst, i - 1)
    return i


def decompress_bytes(tree: HuffmanTree, text: bytes, size: int) -> bytes:
    """ Use Huffman tree <tree> to decompress <size> bytes from <text>.

    >>> tree = build_huffman_tree(build_frequency_dict(b'helloworld'))
    >>> g = compress_bytes(b'helloworld', get_codes(tree))
    >>> number_nodes(tree)
    >>> decompress_bytes(tree, \
             compress_bytes(b'helloworld', get_codes(tree)), len(b'helloworld'))
    b'helloworld'
    """
    d = get_codes(tree)
    t = bytes(0)
    inv_map = {i: j for j, i in d.items()}
    string = ''
    s = 0
    end = 1
    for k in text:
        string += byte_to_bits(k)
    while end < len(string):
        while string[s:end] not in inv_map:
            if len(t) == size:
                return t
            if end == len(string):
                return t
            end += 1
        t += bytes([inv_map[string[s:end]]])
        s = end
    return t


def decompress_file(in_file: str, out_file: str) -> None:
    """ Decompress contents of <in_file> and store results in <out_file>.
    Both <in_file> and <out_file> are string objects representing the names of
    the input and output files.

    Precondition: The contents of the file <in_file> are not empty.
    """
    with open(in_file, "rb") as f:
        num_nodes = f.read(1)[0]
        buf = f.read(num_nodes * 4)
        node_lst = bytes_to_nodes(buf)
        # use generate_tree_general or generate_tree_postorder here
        tree = generate_tree_general(node_lst, num_nodes - 1)
        size = bytes_to_int(f.read(4))
        with open(out_file, "wb") as g:
            text = f.read()
            g.write(decompress_bytes(tree, text, size))


# ====================
# Other functions

def improve_tree(tree: HuffmanTree, freq_dict: dict[int, int]) -> None:
    """ Improve the tree <tree> as much as possible, without changing its shape,
    by swapping nodes. The improvements are with respect to the dictionary of
    symbol frequencies <freq_dict>.

    >>> left = HuffmanTree(None, HuffmanTree(99, None, None), \
    HuffmanTree(100, None, None))
    >>> right = HuffmanTree(None, HuffmanTree(101, None, None), \
    HuffmanTree(None, HuffmanTree(97, None, None), HuffmanTree(98, None, None)))
    >>> tree = HuffmanTree(None, left, right)
    >>> freq = {97: 26, 98: 23, 99: 20, 100: 16, 101: 15}
    >>> avg_length(tree, freq)
    2.49
    >>> improve_tree(tree, freq)
    >>> avg_length(tree, freq)
    2.31
    """
    d = get_codes(tree)
    d2 = d.copy()
    for i in d:
        d2.pop(i)
        for j in d2:
            if len(d[i]) * freq_dict[i] < len(d[j]) * freq_dict[j] and (
                    _help_find(tree, i)
                    and _help_find(tree, j)) is not None \
                    and len(d[i]) != len(d[j]):
                _help_find(tree, i).symbol, _help_find(tree, j).symbol = j, i


def _help_find(tree: HuffmanTree, sym: int) -> HuffmanTree:
    h = 0
    if not tree.is_leaf():
        if isinstance(_help_find(tree.left, sym), HuffmanTree):
            h = _help_find(tree.left, sym)
        if isinstance(_help_find(tree.right, sym), HuffmanTree):
            h = _help_find(tree.right, sym)
    else:
        if tree.symbol == sym:
            return tree
    return h


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    '''
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['compress_file', 'decompress_file'],
        'allowed-import-modules': [
            'python_ta', 'doctest', 'typing', '__future__',
            'time', 'utils', 'huffman', 'random'
        ],
        'disable': ['W0401']
    })
    '''
    mode = input(
        "Press c to compress, d to decompress, or other key to exit: ")
    if mode == "c":
        fname = input("File to compress: ")
        start = time.time()
        compress_file(fname, fname + ".huf")
        print(f"Compressed {fname} in {time.time() - start} seconds.")
    elif mode == "d":
        fname = input("File to decompress: ")
        start = time.time()
        decompress_file(fname, fname + ".orig")
        print(f"Decompressed {fname} in {time.time() - start} seconds.")
