
This documents some processes to generate documents.
They should be shell scripts.


Collation
=========

This works better:
export LC_ALL=C

Otherwise, comm will complain of sort orders.
Maybe gawk  sort order differs from comm sort order?


Useful subroutines
==================

awk one-liners
==============
Print only the first word of each line
nawk '{ print $1}' inputFile

sort in place
=============
sort -o file1 file1



comm as set operation
=====================

comm treats files as sets of lines.
column 3 is intersection of the files as sets (comm -12)
column 1 is file1 subtract file2  (comm -23)
column 2 is file2 subtract file1  (comm -13)



comm set operations on name lists of different versions
=======================================================
Where a list is only the name, not the full signature

Removed (or renamed i.e. deprecated) from version 1:
See below, not simple

New in version 2:   column 2 of comm, i.e. >comm -13



Terminology
===========

deprecations:  a triple  oldName => newName
deprecated: old name
deprecatee: new name
added: name not present in earlier version (totally new, or a deprecatee)
new: name not present in earlier version and not a deprecatee
newDeprecated: name present in earlier version, not in new version, and no known deprecation
   (TODO synonym for removed?)

TODO signaturesChanged


Algebra
=======

newDeprecateesV3 + newV3 = addedV3

removedV2 + deprecatedV2 + commonV2V3 = V2

commonV2V3 + addedV3 = V3

TODO


Generate signature files for two versions
=========================================
nawk -f parsePDBTxt.nawk pdb2_10.txt >pdb2_10.json
nawk -f parsePDBTxt.nawk pdb2_99.txt >pdb2_99.json

This is the basis for following steps





To generate a list of possible new deprecations
===============================================

1. Produce list of signature changed procedure names.
comm -3 pdb2_10.txt.sig  pdb2_99.txt.sig | gawk -f parseSignatureChanges.nawk >signaturesChanged.txt
Fields:  foo

2. Produce list of names not in V2 or in V2 but changed signature from V2
comm -23 pdb2_10.txt.sig  pdb2_99.txt.sig | gawk '{ print $1}' > removedOrSignatureChanged.txt
Fields:  foo

3. Produce list of names not in v2
Subtract 1 from 2
comm -23 removedOrSignatureChanged.txt signaturesChanged.txt > removedOrDeprecated.txt
Fields: foo

4. Produce list of known deprecations.
gawk -f parsePDBCompat.nawk ~/v*G*/gimp/app/pdb/gimp-pdb-compat.c > deprecations.txt
Fields: foo => bar

5. Produce possible new deprecations
Subtract 4 from 3
comm -23 removedOrDeprecated.txt deprecations.txt > newDeprecated



To generate a list of totally new procedure
===========================================
(!!! Or undocumented deprecation)

Requires from above:
signaturesChanged.txt
deprecations.txt

1. Produce list of (names not in V1) or (name in V1 but changed signature from V1 to V2)
comm -13 pdb2_10.txt.sig  pdb2_99.txt.sig | gawk '{ print $1}' > addedOrSignatureChanged.txt
Fields:  foo

2. Subtract signature changes
comm -23 addedOrSignatureChanged.txt signaturesChanged.txt > added.txt
Fields: foo
It includes added new and added deprecatees

3. Create sorted list of new (deprecatee) names of deprecated
Its the third word of deprecated
gawk '{ print $3}' deprecations.txt > deprecatees.txt
sort -o deprecatees.txt deprecatees.txt
Fields:  foo

4. Subtract deprecatees

comm -23 added.txt deprecatees.txt > new.txt
