This directory contains various files about the GIMP PDB.

See also process.md

A nawk script to convert a pdb dump (pdb.txt) to json (pdb.json) and a signature file .txt.sig

A nawk script to convert gimp/pdb/gimp-pdb-compat.c to a readable text file
of deprecated PDB procedures

The process is:
GIMP pdb dump => pdb<foo>.txt  (use the GIMP app interactively)
nawk the above => .json
               => .txt.sig

So all .txt and .json and .txt.sig files are ephemeral artifacts,
should be refreshed as gimp repository changes.

Often files are in pairs, for different versions of GIMP.

pdb.json is used as the input to plug-ins/testGimpPDB.
testGimpPDB is data-driven (pdb.json), automated test of PDB.

For now the tests are fuzzy,
i.e. with type valid but arbitrarily valued inputs to procedures under test,
only testing for crashes, with a human inspecting the results.
In the future, the testing could be expanded to
test even more randomly,
with values that might test edge cases, e.g. zeros.

The PDB may change often (with any commit) so you may need to do the following frequently:

Process:

1) call pdb.dump_to_file(f) to generate pdb.txt.  Use plugin dump_pdb.py  in GUI Test>Dump PDB...

2) generate json.   >nawk -f parsePDBTxt.nawk pdb.txt > pdb.json

3) edit pdb.json to remove the last comma

3) run the test plugin    Test>testGimpPDB  which reads the .json
