# TestGimpPDB

A Gimp plugin that minimally tests most procedures in Gimp PDB.

*!!! Use only in a testing environment, not in a production environment, since it will alter your local GIMP resources!!!*

*!!! Work in progress.  This is not stable. It is not a complete test of Gimp.  It is not sanctioned by Gimp.org!!!*

*!!! It is a GimpFu plugin and also requires my repository GimpFuV3. !!!*

I am using it to test Gimp 3.  With minor changes, it might also work for other Gimp versions.

Appears in menus as *Test>Test Gimp PDB...*

Not totally automated, a human must read and interpret a log.

A user interface lets you choose subsets of PDB procedures.

Mostly "sanity" tests.  
Only the PDB status result is compared to an expected value.
Other returned values from a procedure are not examined.
Side effects on other resource (e.g. the current image) are not examined.

Not all PDB procedures will pass since it dumbly improvises parameters to plugins.
Parameter values are of the correct type, not necessarily in range, nor semantically meaningful.

To some extent it can do fuzzy testing, generating stochastic improvised parameters.

## Why test the PDB?

The PDB is high in the stack of layers, so testing it exercises many layers.

The PDB contains:

  - plugins, that themselves call other plugins or internal procedures in the PDB.
  - internal procedures (interface to libgimp)
  - other extensions

Layers that may be exercised by this testing :

  - plugins and internal procedures in the PDB
  - interpreters (for Scheme, Python, Lua plugins)
  - libgimp
  - gimp core
  - libraries that Gimp uses

## The log

The log defaults to standard out.
Thus you should start Gimp in a console.

The log might contain interleaved log messages from:

  - the PDB procedure
  - GimpFu
  - PyGObject
  - Python interpreter
  - Gimp
  - Babl and Gegl
  - GLib and similar

Each of those can be configured/built to do more/less logging.

At the end of the log:
  - test statistics and summary by this plugin
  - a summary by GimpFu
  - a final Python exception if GimpFu discovered any errors
    (in the execution of this plugin, which encompasses all called PDB procedures.)
  - many other usually spurious(?) messages when Gimp recovers from this plugin.

Note the above may change as this plugin, GimpFu, and Gimp evolve.

## The extent of testing

Some PDB procedures are never tested because they obstruct automated testing:
   - interactive (they don't seem to respect run-mode?)
   - recurse (i.e. this plugin doesn't test itself)
   - delete test data needed by other tests
   - quit Gimp
   - other special cases (hardcoded in excludedTestCases.py)

It can test all procedures in *your* PDB.
The PDB contains procedures of a stock Gimp installation (so-called internal procedures, and official plugins)
as well as plugins that you have installed.

Plugins are tested non-interactively, with improvised actual parameters
(not their default parameters.)

## How a procedure is tested

Dumb testing:

  - certain semantic constraints are not understood by the tests,
    e.g. tests don't understand certain procedures will not try to create Gimp artifacts that already exist.
  - tests do not understand how procedure result relates to inputs,
    only that there should be a returned result of a certain type.  I.E. result values are not compared to an expected value (except of course for the status result)
  - tests do not understand procedure side effects
    I.E. changes to passed images are not compared to an expected image
    and other changes to Gimp resources are not examined.

Primarily tests that a procedure can be called without engendering:
  - seg fault
  - Gimp error
  - GimpFu exception
  - Python exception

You should expect many procedures will return a Gimp error because testing is dumb:
  - value out of range
  - other: e.g. "can't create foo because it already exists."

Gimp errors that indicate flaw in Gimp:
  - wrong parameter types
  - almost any other error e.g. ScriptFu: unknown symbol

# Improvised test data

The primary test data is the image that is open when you begin testing.
This plugin clones it and passes the clone to most procedures.
Some procedures expect certain qualities of the image:
  - a selection exists
  - strokes exist
  - a particular image mode e.g. RGBA
  - etc.

Thus you can repeat testing with different starting images.

Some improvised data is canned (hard coded) and arbitrary.
Some can be stochastically chosen.

## Installation

Copy the directory to where Gimp plugins are installed.
Restart Gimp.
Note the main plugin file must be named same as directory (since Gimp v3.)

## Dependencies

  - Gimp
  - GimpFu module (note that GimpFu is deprecated since Gimp v3.  Use my other repository
  which is unofficial GimpFu for Gimp v3.)
  - PyGObject Python module
  - Various standard Python modules (e.g. logging.)

## Warning

Running this plugin can call many procedures that create local Gimp resources such as brushes.  Don't run this plugin in an environment that contains production resources.  You may need to periodically flush local Gimp resources ( e.g. delete subsets of .config/GIMP/2.99/)

## Regenerating PDB metadata

This plugin reads the formal specifications for PDB procedures from a .json file in this repository.
The .json file is a snapshot from a particular build and installation of Gimp.
It should be periodically regenerated.
See the directory testPDB.
To regenerate, you must run a plugin that calls the PDB procedure dump_to_file (which might go away?)
Then run the nawk script testPDBTxt.nawk to convert to JSON.


## TODO

  - you must open an image before you can invoke the plugin
  - read the procedure metadata from the PDB instead of a .json file

  - capture test results and compare to known/previous results
  - allow the subset of interactive plugins to be tested (currently excluded)
  - certain rare parameter types not yet improvised


## Recent changes

- Better improvisation: on error "out of range" iteratively improvise values from a set,
  where at least one element of the set
  typically would be in range.
