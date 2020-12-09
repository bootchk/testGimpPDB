# parse a comm of the pdb, finding signatures which changed

# lloyd konneker May 2020

# invoke   gawk -f parseSignatureChanges.nawk col12.txt >signatureChanges.txt

# Input
# A text file from running comm on two .txt.sig getting the first two columns
# (the signatures that are in first version and not in second version, and vice versa,
# excluding column 3, the signatures that are in both)
# comm -3 pdb2_10.txt.sig pdb2_99.txt.sig > temp.txt

# Output:
# a txt file containing pairs of lines
# where both of the pair have the same PDB procedure name, but differing signatures

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


# output the current pair in various forms
function outputPair(line1, line2, line1NF, line2NF) {
  # print both, for use with diff
  print trimLeadingSpace(line1)
  print trimLeadingSpace(line2)

  # print only the name, where count of args is different
  if (line1NF != line2NF) {
      print $1
  }
}

# performed on every line
{
  currentName = $1
  if (currentName == previousName) {
    # Same PDB procedure name as previous
    outputPair(previousRecord, $0, previousNF, NF)

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
