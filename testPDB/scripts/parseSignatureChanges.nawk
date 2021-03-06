# parse a comm of the pdb, finding signatures which changed

# lloyd konneker May 2020

# invoke   gawk -f parseSignatureChanges.nawk col12.txt >signaturesChanged.txt
# as pipe: comm -3 pdb2_10.txt.sig  pdb2_99.txt.sig | gawk -f parseSignatureChanges.nawk >signaturesChanged.txt

# From the top directory, as a pipe:
# comm -3 pdb2_10.dump.signatures  pdb2_99.dump.signatures | gawk -f scripts/parseSignatureChanges.nawk
# if comm complains not sorted, be sure to sort -o in place first

# Input
# A text file from running comm on two .txt.sig getting the first two columns
# (the signatures that are in first version and not in second version, and vice versa,
# excluding column 3, the signatures that are in both)
# comm -3 pdb2_10.txt.sig pdb2_99.txt.sig > temp.txt

# Output:
# a txt file containing pairs of lines
# where both of the pair have the same PDB procedure name, but differing signatures
# OR
# a txt file containing just a name on each line, each name has some signature change
# but is still in both versions

# !!! Note any pair will not be in any particular order:
# first line may be from first version, second from second version, or vice versa.

# Use case
# To produce a document describing the differences.
# Run diff on the file to highlight the specific differences


# remove columns in the input created using tab or space character
function trimLeadingSpace(text) {
   sub(/^[ \t]+/, "", text)
   return text
}

function printBothLines(line1, line2) {
  # print for use with diff
  print trimLeadingSpace(line1)
  print trimLeadingSpace(line2)
}

# output signature change in various forms
function outputSignatureChange(line1, line2, line1NF, line2NF) {
  # TODO comment one of these out.

  printBothLines(line1, line2)

  # print only the name, where count of args is different
  # This is deficient since it allows type changes that maintain count
  # if (line1NF != line2NF) {
  #    print $1
  #}

  # print only the name
  # print $1
}

# performed on every line
{
  currentName = $1
  if (currentName == previousName) {
    # Same PDB procedure name as previous
    outputSignatureChange(previousRecord, $0, previousNF, NF)

    if (state == "twoNames") {
      # error, saw a third instance of name
    }
    state = two Names
  }
  else {
    # a new name.
    state = "oneNames"
  }

  previousName = currentName
  previousRecord = $0
  previousNF = NF
}
