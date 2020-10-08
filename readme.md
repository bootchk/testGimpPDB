# TestGimpPDB

A Gimp plugin that tests most procedures in Gimp PDB.

Appears in menus as *Test>Test Gimp PDB...*

Not totally automated, a human must read and interpret a log.

A user interface lets you choose subsets of PDB procedures.


Improvises parameters to plugins.
Values are of the correct type, not necessarily in range.

## The log

The log defaults to standard out.
Thus you should start Gimp in a console.

The log will contain interleaved log messages from:

  - the procedure
  - GimpFu
  - Python interpreter
  - Gimp
  - Babl and Gegl

Each of those can be configured/built to do more/less logging.

## The extent of testing

Some PDB procedures are never tested because they obstruct automated testing:
   - interactive (they don't seem to respect run-mode?)
   - recurse (i.e. this plugin doesn't test itself)
   - delete test data needed by other tests
   - quit Gimp

It can test all procedures in *your* PDB.
The PDB contains procedures of a stock Gimp installation (so-called internal procedures, and official plugins)
as well as plugins that you have installed.

Plugins are tested non-interactively, with improvised actual parameters
(not their default parameters.)

## How a procedure is tested

Dumb testing:

  - certain semantic constraints are not understood by the tests,
    e.g. tests don't understand certain procedures will not create Gimp artifacts that already exist.
  - tests do not understand how procedure result relates to inputs,
    only that there should be a result of a certain type.  I.E. output values are not tested.

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


## TODO

  - you must open an image before you can invoke the plugin
  - read the procedure metadata from the PDB instead of a .json file
  - Better improvisation: on "error parameter out of range" iteratively improvise values from a set,
    where at least one element of the set
    typically would be in range.
  - capture test results and compare to known/previous results
