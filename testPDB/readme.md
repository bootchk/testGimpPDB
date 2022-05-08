This directory contains various files about the GIMP PDB.

See also process.md

About the contents:
 /sourceData   sources for scripts.  Some are manually entered, some generated from the PDB (.dump)
 /scripts      scripts to manipulate the data.  Scripts for tools: shell and nawk
 Everything else: generated artifact files, distinguished by suffix
    simpleName   list of PDB procedure names
    name.signatures list of signatures of PDB procedure names
    name.deprecations list of "foo => bar" i.e. a mapping from procedure name to procedure name (signatures same)
    name .json    in json format



A nawk script to convert a pdb dump (pdb.txt) to json (pdb.json) and a signature file .txt.sig

A nawk script to convert gimp/pdb/gimp-pdb-compat.c to a readable text file
of deprecated PDB procedures

The process is:

GIMP pdb dump => pdb<foo>.dump
This file is in a special format, with parens.
Use the GIMP app interactively.
Choose the plugin "Test>Dump PDB to /work/pdb.txt"
(That plugin calls the PDB procedure gimp-pdb-dump.)
That plugin is in the GimpFuv3 repo at TestPlugins/test/dump_pdb
It creates a file "pdb.txt" at "/work"
(which in a vagga container, is the project directory.)

Move pdb.txt to testPDB/sourceData and rename it to say pdb2_99.dump.

cd to testPDB

nawk the above => .json
               => .txt.sig

nawk -f scripts/parsePDBDump.nawk sourceData/pdb2_99.dump > pdb2_99.json

Edit the JSON file to remove the last comma in the file
(some JSON parsers don't allow a trailing comma in a list.)

Since you altered the data for testGimpPDB project,
reinstall it, so the data is installed in ~/.config/gimp/.../plug-ins/testGimpPDB

Now should be able to run testGimpPDB plugin
(it looks in this directory, testGimpPDB/testPDB/pdb2_99.json )

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
