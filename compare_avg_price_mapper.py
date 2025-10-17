#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import csv

def read_input(file):
    for line in file:
        # Bỏ BOM nếu có
        line = line.lstrip('\ufeff').strip()
        if line == "":
            continue
        yield line

def main():
    reader = csv.reader(read_input(sys.stdin))
    header = next(reader)  # Bỏ header
    for row in reader:
        if len(row) < 3:
            continue
        brand = row[2].strip()        # Thương hiệu
        price = row[1].replace(',', '').strip()  # Giá
        platform = row[-1].strip()    # Platform (Tiki / Hasaki)
        try:
            price = float(price)
            print(f"{brand}\t{platform}\t{price}")
        except:
            continue

if __name__ == "__main__":
    main()

