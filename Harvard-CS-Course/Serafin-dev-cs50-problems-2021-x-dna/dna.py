import sys
import csv
#recursive function to count every matching sequence of every STR
def rCount(st, iP, r):
    if st == s[iP:iP + len(st)]:
        r += 1
        return rCount(st, iP + len(st), r)
    return r
#
def compute(seq):
    for k in data:
        c = 0
        for base in seq:
            data[k].append(rCount(k, c, 0))
            c += 1
        data[k] = max(data[k])

def compare():
    with open(sys.argv[1]) as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            l = list(row.values())
            l.remove(l[0])
            if list(data.values()) == [int(i) for i in l]: 
                match = row["name"]
                return print(match)
        return print("No match")
        
if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    sys.exit(1)

data = {}
with open(sys.argv[1]) as csvFile:
    strs = csvFile.readline().rstrip().split(",")
    strs.remove("name")
    for s in strs:
        data[s] = []
    
with open(sys.argv[2], "r") as txtFile:
    s = txtFile.read().rstrip()
    l = []
    compute(s)
compare()