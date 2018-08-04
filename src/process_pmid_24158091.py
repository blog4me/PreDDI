#!/usr/bin/env python3

import io
import csv
import utils


def map_to_drugbank():
    matched = []
    total = 0
    existing_pairs = set()
    duplicated = 0

    with io.open('../data/pmid_24158091/amiajnl-2013-001612-s3.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        next(reader, None)
        #  0 - event
        #  1 - drug1
        #  2 - drug2
        #  3 - a
        #  4 - b
        #  5 - c
        #  6 - d
        #  7 - pop_event_rate
        #  8 - uor025
        #  9 - label
        # 10 - aor025
        for row in reader:
            row = [x.strip() for x in row]
            if row[10] == 'NA' or float(row[10]) < 1.1:
                continue
            total += 1
            id1 = utils.name_to_drugbank_id(row[1])
            id2 = utils.name_to_drugbank_id(row[2])
            if id1 is not None and id2 is not None:
                if (id1, id2) in existing_pairs or (id2, id1) in existing_pairs:
                    duplicated += 1
                    continue
                else:
                    existing_pairs.add((id1, id2))
                    #  0 - drugbank1
                    #  1 - drugbank2
                    #  2 - event
                    #  3 - drug1
                    #  4 - drug2
                    #  5 - a
                    #  6 - b
                    #  7 - c
                    #  8 - d
                    #  9 - pop_event_rate
                    # 10 - uor025
                    # 11 - label
                    # 12 - aor025
                    matched.append(
                        [id1, id2, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                         row[10]])

    with io.open('../data/pmid_24158091/amiajnl-2013-001612-s3_matched.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        writer.writerow(
            ['drugbank1', 'drugbank2', 'event', 'drug1', 'drug2', 'a', 'b', 'c', 'd', 'pop_event_rate', 'uor025',
             'label', 'aor025'])
        for row in matched:
            writer.writerow(row)


def process():
    map_to_drugbank()