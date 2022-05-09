

#import gi
#gi.require_version("Gimp", "3.0")
#from gi.repository import Gimp
from gimpfu import *

"""
Class that accesses the GIMP PDB.
"""


class PDB():
    @classmethod
    def default_value_for_procname_arg(cls, procName, argIndex, expectedType):
        """
        Returns str of default value for arg.
        Default value may be the string "None" meaning no default specified.
        Exception if argIndex out of range.
        """

        # Gimp.get_pdb().lookup_procedure(proc_name)
        # returns Gimp.Procedure
        # procedure.find_argument(name)

        # Using GI
        # result = Gimp.get_pdb().get_proc_argument(procname, argIndex)
        # Fail: no such method

        # Using GimpFu
        paramSpec = pdb.gimp_pdb_get_proc_argument(procName, argIndex)
        # Returns GParam
        # print(f"Param spec: {paramSpec.__gtype__}")
        # print( dir(paramSpec))

        #print(f"Str() of default value: {paramSpec.default_value}")
        #print(f"repr() of default value: {repr(paramSpec.default_value)}")

        # We don't expect paramSpec is None.  If so, the rest will raise exception.
        # We do allow the default_value to represent None, meaning no default value specified.

        result = str(paramSpec.default_value)

        """
        Str could still look like:
        <enum GIMP_RUN_NONINTERACTIVE of type Gimp.RunMode>
        because the __str__ is deficient?

        So special case: substitute a convenient interger for enums.
        1 almost always is in range.
        """
        if "<enum" in result:
            result = '1'

        """
        Add quotes to make string defaults look like string literals.
        """
        if result != "None" and expectedType == "gchararray" :
            result = '"' + result + '"'

        """
        Ensure the string is "None"
        or a string that looks like an argument in Python to a PDB procedure.
        """
        assert (isinstance(result, str))
        return result
