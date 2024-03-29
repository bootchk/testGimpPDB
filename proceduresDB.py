

import json

from testLog import TestLog
from pdbGimpReader import PDBGimpReader

# all methods are class methods


class PDBJsonReader:

    """
    /work refers to the vagga project directory
    where, in the container, is mounted a development directory.
    !!! TODO This should be relative to the plugin's directory, somehow.
    """

    def pathToPDBJson():
        from pathlib import Path

        # relative to this .py file
        path = Path(__file__).parent / "./testPDB/pdb2_99.json"

        TestLog.say(f"Reading JSON file: {path}")

        # path = "/work/testGimpPDB/testPDB/pdb.json"
        return path


    def readData():
        TestLog.say(f"!!!! Reading the PDB from a JSON file, not from the GIMP PDB !!!!")
        TestLog.say(f"!!!! If it is not current, expect tests to fail              !!!!")
        TestLog.say(f"!!!! Please read testPDB/process.md and readme.md            !!!!")
        data = {}
        with open(PDBJsonReader.pathToPDBJson(), "r") as read_file:
            data = json.load(read_file)
        return data






"""
A class that mimics the GIMP PDB.

Provides various dictionaries that act as key/value databases.
A Python dictionary modeled after the PDB

A dictionary keyed by procedure name, yielding a dictionary of attributes of the procedure.

name : {
    type : name of GimpDBPProcType e.g. "temporary"
    in   : [ name of gtype, ... e.g. gint
    ]
}

See testPDB/process.md for the process of refreshing the JSON from GIMP PDB.

class data and methods, no instance
"""

class ProceduresDB:

    data = {}

    """
    Alternate sources of data
    The PDB itself is most accurate.
    JSON is historical, it was generated by nawk scripts, it is useful for other purposes.
    """
    def readFromJSON():
        ProceduresDB.data = PDBJsonReader.readData()
        # assert ProceduresDB.data is-a dictionary modeled after the PDB

    def readFromGimp():
        # Query PDB
        ProceduresDB.data = PDBGimpReader.readData()

    def sortedNames():
        return ProceduresDB.data.keys()

    def attributeDictionary(procName):
        """ Return a dictionary of attributes for a PDB procedure. """
        return ProceduresDB.data[procName]

    def typeof(procName):
        """ Return the PDBProcedureType for a PDB procedure. """
        return ProceduresDB.data[procName]["type"]

    def isTypeTemporary(procName):
        return ProceduresDB.typeof(procName) == "temporary"
