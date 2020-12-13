
This documents some processes to generate documents.
They should be shell scripts.



Data flow
=========

Source files:
 PDB earlyVersion, lateVersion   the PDB's themselves are dumpable.
 /gimp/app/pdb/gimp-pdb-compat.c    The file which defines deprecations (out of date though)
 *.nawk
 *.sh
 *.md  documentation
 undocumentedDeprecations: manually entered

Everything else is ephemeral artifact, can be regenerated:
All files are text files (no binary.)
Suffixes indicate format:
no suffix      one field, a PDB procedure name
.signatures    many fields, signatures
.json
.dump         in the format that GIMP dumps the PDB
.deprecation  three fields: nameInEarlyVersion => nameInLateVersion
.data         a source document, entered using editor


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

            -------------set2---------
------set1-------------
| comm -23  | comm -12 |  comm -13    |

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

List: generate sorted list

earlyVersion e.g. V2 or V2.10
lateVersion  e.g. V3

deprecations:  a triple  nameInEarlyVersion => nameInLateVersion
deprecated: nameInEarlyVersion
deprecatee: nameInLateVersion
!!! nameInEarlyVersion name also appears in lateVersion, but is redirected to nameInLateVersion

added: name not present in earlyVersion (totally new, or a deprecatee)
new: name not present in earlyVersion and not a deprecatee

newDeprecated: name present in earlyVersion, not in lateVersion, and no known deprecation
   (not a synonym for removed because it includes undocumentedDeprecations)

signatureChanged: name present in both versions but whose signature has changed
(this is fuzzy, see unifications in parseSignatureChanges.nawk)
A deprecation is distinct from signatureChange.  But a deprecation may also have a changed signature.

removed: name present in earlyVersion and not deprecated i.e. not replaced by another name in lateVersion



Algebra
=======

TODO
work in progress

common + allDeprecatees + added = lateVersion

common + (knownDeprecatees + newDeprecatees) + added = lateVersion

earlyVersion - removed +   = lateVersion

newDeprecateeslateVersion + newlateVersion = addedlateVersion

removedearlyVersion + deprecatedearlyVersion + commonearlyVersionlateVersion = earlyVersion

commonearlyVersionlateVersion + addedlateVersion = lateVersion



Generate signature files for two versions
=========================================
nawk -f parsePDBDump.nawk pdb2_10.dump >pdb2_10.json
nawk -f parsePDBDump.nawk pdb2_99.dump >pdb2_99.json

Side effects are pdb2_10.signatures and ...

This is the basis for following steps



List signature signature changes
================================

1.List signature changed procedure names.
comm -3 pdb2_10.dump.signatures  pdb2_99.dump.signatures | gawk -f parseSignatureChanges.nawk >signatureChanged
Fields:  foo



To generate a list of possible undocumented/new deprecations
========================================================

(includes undocumentedDeprecations)

This documents generateNewDeprecations.sh

2.List names (not in earlyVersion) or (in earlyVersion but changed signature from earlyVersion)
comm -23 pdb2_10.dump.signatures  pdb2_99.dump.signatures | gawk '{ print $1}' > removedOrSignatureChanged
Fields:  foo

TODO this is not right

3.List names not in lateVersion
Subtract 1 from 2
comm -23 removedOrSignatureChanged signatureChanged > removedOrDeprecated
Fields: foo

6. List possible new deprecations
Subtract 4 from 3
comm -23 removedOrDeprecated knownDeprecated > newDeprecated
Fields: foo



??? Abandoned
To generate removed
===================
generateRemoved.sh

1.  Generate possible new deprecations
sh generateNewDeprecations.sh > newDeprecations

2.  Get undocumentedDeprecated from undocumentedDeprecations
nawk '{ print $1}' undocumentedDeprecations > undocumentedDeprecated
sort -o undocumentedDeprecated undocumentedDeprecated

3.  Filter: newDeprecations subtract undocumentedDeprecated
comm -23  newDeprecations  undocumentedDeprecated



Produce names in early and late versions
========================================
1.  Produce names in earlyVersion
nawk '{ print $1}' pdb2_10.dump.signatures > namesInEarlyVersion

2.  Produce names in lateVersion
nawk '{ print $1}' pdb2_99.dump.signatures > namesInLateVersion



Deprecations
============

Kinds:
1. hidden (in the dump)
2. known (in gimp-pdb-compat.c)
3. undocumented (in undocumentedDeprecations.data)


Undocumented deprecations
=========================

Requires undocumentedDeprecations.data

1. Produce undocumentedDeprecated
gawk '{ print $1}' undocumentedDeprecations.data | sort > undocumentedDeprecated

2. Produce undocumentedDeprecatee without duplicates
Since many-to-one deprecated to deprecatee, eliminate duplicates.
Also assert is sorted.
gawk '{ print $3}' undocumentedDeprecations.data | sort | uniq > undocumentedDeprecatee


Known deprecations
==================

generateKnownDeprecations.sh

1. Parse the source doc  !!! Unsorted
gawk -f parsePDBCompat.nawk ~/v*G*/gimp/app/pdb/gimp-pdb-compat.c | sort > known.deprecations
Fields: foo => bar

gawk '{ print $1}' known.deprecations > knownDeprecated
gawk '{ print $3}' known.deprecations | sort | uniq > knownDeprecatees


Hidden deprecations
===================

requires a .dump

nawk -f parseHiddenDeprecations.nawk pdb2_99.dump | sort > hidden.deprecations
gawk '{ print $1}' hidden.deprecations > hiddenDeprecated
gawk '{ print $3}' hidden.deprecations | sort | uniq > hiddenDeprecatees


All Deprecations
================

generateAllDeprecations.sh

cat known.deprecations hidden.deprecations undocumentedDeprecations.data | sort | uniq > all.deprecations
gawk '{ print $1}' all.deprecations | uniq -> allDeprecated
gawk '{ print $3}' all.deprecations | sort | uniq > allDeprecatees



To check any .deprecations
==========================

Requires namesInEarlyVersion, namesInLateVersion

Insure each deprecated name in earlyVersion
Insure each deprecatee name in lateVersion
TODO
Insure each deprecated not already in documented.deprecations
Insure each deprecatee not already in documented.deprecations

1. Insure each deprecated name in earlyVersion
Compare: col1 should be empty.
comm -23 undocumentedDeprecated namesInEarlyVersion
Any in col1 are fooDeprecated FAIL to be in earlyVersion

2. Insure each deprecatee name in lateVersion
comm -23 undocumentedDeprecatee namesInLateVersion
Any in col1 are undocumentedDeprecatee FAIL to be in lateVersion

!!! Some will be transitive deprecations that are OK.
e.g. gimp-blend => gimp-edit-blend
gimp-edit-blend => gimp-drawable-edit-gradient-fill
Results in gimp-edit-blend a deprecatee not in lateVersion




To generate a list of added
===========================
(!!! Includes new and deprecatees)
generateAdded.sh

Requires from above:
signatureChanged

1.List (names not in earlyVersion) or (name in signatureChanged but changed signature from signatureChanged to lateVersion)
comm -13 pdb2_10.dump.signatures  pdb2_99.dump.signatures | gawk '{ print $1}' > addedOrSignatureChanged
Fields:  foo

2. Subtract signature changes
comm -23 addedOrSignatureChanged signatureChanged > added
Fields: foo
It includes totally new and deprecatees




List new
========

generateNew.sh

requires undocumentedDeprecatees

1. Added minus undocumented deprecatees
comm -23 added undocumentedDeprecatees > new




List removed
============

aka "Deprecated: not replaced"

generateRemovedNotDeprecated.sh

1.  Names in early but not late version
comm -23 namesInEarlyVersion namesInLateVersion > namesRemovedOrDeprecated

2.  subtract deprecated
comm -23 namesRemoved allDeprecated > removed
