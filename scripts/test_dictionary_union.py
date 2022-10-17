#!/usr/bin/env python3

if __name__ == "__main__":
    dict1 = { "k1": 1, "k2": 2 }
    dict2 = { "k2": 2, "k3": 3 }

    dict_union = dict1 | dict2

    print(dict_union)