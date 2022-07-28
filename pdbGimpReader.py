
import gi
gi.require_version("Gimp", "3.0")
from gi.repository import Gimp


from testLog import TestLog

from gimpfu import *

# all methods are class methods

"""
Read a dictionary modeled after the PDB from the Gimp PDB.
"""

class PDBGimpReader:

    def nameProcType(procType):
        # string name of GimpPDBProcType
        return "foo"


    def getArgTypes(procedure):
        list = []

        argParamSpecs = procedure.get_arguments()   # list of GParamSpec

        for paramSpec in argParamSpecs:
            # value_type is a GType
            typeName = paramSpec.value_type.name
            list.append(typeName)

        #Alternative: procedure.new_arguments() returns GimpValueArray, not iterable
        #Alternative: procedure.find_argument(name)

        return list


    def readData():
        TestLog.say(f"!!!! Reading the PDB from GIMP PDB !!!!")
        data = {}

        # query with regex on name.
        # Other args defaulted by gimp, but gimpfu requires them.

        # The gimpfu construct is not pdb.query
        # Its not gimp.gimp_pdb_query since it is not a libgimp method
        # The method for querying the pdb is IN the PDB
        names = pdb.gimp_pdb_query(".*", ".*", ".*", ".*", ".*", ".*", ".*")

        aPDB = Gimp.get_pdb()
        for name in names:
            """
            The PDB contains no procedure for querying the signature !!!!
            lookup_procedure is NOT IN the PDB.
            It is a method of libgimp Gimp.PDB class
            """
            # lookup an instance of Gimp.Procedure, by name
            procedure = aPDB.lookup_procedure(name)

            attributes = {}

            procType = procedure.get_proc_type()
            # GimpPDBProcType an enum value
            # value_name is like GIMP_PDB_PROC_TYPE_INTERNAL
            # value_name is like "internal, temporary, plugin" strings
            attributes["type"] = procType.value_nick
            # print(attributes["type"])

            attributes["in"] = PDBGimpReader.getArgTypes(procedure)
            # FUTURE: attributes["out"] = outFormalArgs

            data[name] = attributes
        # print(f"name: {name}, dir: {data}")
        return data
