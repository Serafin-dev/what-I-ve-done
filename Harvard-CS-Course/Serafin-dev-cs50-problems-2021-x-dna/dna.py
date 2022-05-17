import sys
import csv

# recursive function to count every matching sequence of every STR
def countStrRepetitions(dnaSequence, s, iPoint, counter):
    if s == dnaSequence[iPoint: iPoint + len(s)]:
        counter += 1
        return countStrRepetitions(dnaSequence, s, iPoint + len(s), counter)
    return counter

# compare all str runs and select the maximum
def computeLongestRun(dnaSequence):
    for s in strs:
        iPoint = 0
        for base in dnaSequence:
            strs[s].append(countStrRepetitions(dnaSequence, s, iPoint, 0))
            iPoint += 1
        strs[s] = max(strs[s])

# Show the resulting match or not if there isn't
def checkIfMatch(row, values):
        if list(strs.values()) == [int(i) for i in values]:
            match = row["name"]
            return print(match)
        return print("No match")

if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    sys.exit(1)

def main():
    with open(sys.argv[1], "r") as csvFile:
        strsList = csvFile.readline().rstrip().split(",")
        strsList.remove("name")
        for s in strsList:
            strs[s] = []

        # compute longest run of each str for a given dna sequence
        with open(sys.argv[2], "r") as txtFile:
            dnaSequence = txtFile.read().rstrip()
            computeLongestRun(dnaSequence)

    # check match
    with open(sys.argv[1], "r") as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            rowValues = list(row.values())
            rowValues.remove(rowValues[0])

            # Show the resulting match or not if there isn't
            if list(strs.values()) == [int(i) for i in rowValues]:
                match = row["name"]
                return print(match)
        return print("No match")

strs = {}
main()
