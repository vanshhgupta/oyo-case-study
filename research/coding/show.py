import csv, sys
a, b = int(sys.argv[1]), int(sys.argv[2])
r = list(csv.DictReader(open('research/guest_reviews_filtered.csv')))
for x in r[a-1:b]:
    print(x['row'], x['rating'], x['text'][:360])
