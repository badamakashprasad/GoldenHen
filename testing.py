import csv

with open("nseJsonListing.csv","r") as fp:
    reader = csv.DictReader(fp)
    latest = [i for i in reversed(list(reader))][0]
