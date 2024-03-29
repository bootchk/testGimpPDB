
import gi
from gi.repository import Gio

from gimpfu import *

import logging

# logger for this plugin.  GimpFu has its own logger

logger = logging.getLogger('testGimpPDB.testHarness')
assert logger is not None

def generateFooGimpData(drawable):
    """ Generate into Gimp, instances of various kinds, each instance named "foo"

    To be used as data for testing.
    Data chosen is arbitrary, we only care that it exists with name 'foo'.
    Arbitrary: get from the current Gimp context.

    The object model, from GIMP App Ref Manual:
    GimpData
        GimpBrush
            GimpBrushClipboard
            GimpBrushGenerated
            GimpBrushPipe
        GimpCurve
        GimpDynamics
        GimpGradient
        GimpPalette
        GimpPattern
            GimpPatternClipboard
        GimpToolPreset
    GimpBuffer
    GimpItem

    Most of these kinds are GimpData

    Kinds:
    palette
    gradient
    pattern ? API is different
    named buffer
    font ?

    We use 'foo' as a string type parameter whenever one is needed,
    and the use is often as the name of a kind of Gimp object.

    Not all these Gimp objects have Gimp classes.
    """

    """
    The code pattern is:
    context_get
    duplicate
    rename
    """

    # palette
    current_name = gimp.context_get_palette()
    duplicate_name = gimp.palette_duplicate(current_name)
    gimp.palette_rename(duplicate_name, "foo")
    logger.debug(f"Created 'foo' palette instance from {duplicate_name}")

    #brush
    current_name = gimp.context_get_brush()
    duplicate_name = gimp.brush_duplicate(current_name)
    gimp.brush_rename(duplicate_name, "foo")
    logger.debug(f"Created 'foo' brush instance from {duplicate_name}")

    # gradient
    current_name = gimp.context_get_gradient()
    duplicate_name = gimp.gradient_duplicate(current_name)
    gimp.gradient_rename(duplicate_name, "foo")
    logger.debug(f"Created 'foo' gradient instance from {duplicate_name}")

    # channel
    # layer mask
    # selection
    # text layer
    # vectors
    # tattoo

    # buffer: an edit buffer from a cut/copy

    # FAIL: gone in v3?  buffer = pdb.gimp_drawable_get_buffer(drawable)

    '''
    Use the v2 signature, which GimpFu will adapt to v3.
    v3: did_copy = pdb.gimp_edit_copy(1, [drawable,])
    '''

    did_copy = pdb.gimp_edit_copy(drawable)
    if not did_copy:
        logger.debug(f"Failed to create buffers")

    # Verify there is a buffer
    buffers = pdb.gimp_buffers_get_list("")
    logger.debug(f"Created buffers: {buffers}")
    # TODO is returning a list of length 0 of type GimpStringArray
    # which GimpFu or PyGObject doesn't handle
    # i.e. convert to a list of strings
    # Expect a non-empty list of names of buffers
    #pdb.gimp_buffer_rename(old, "foo")

    # TODO curve, dynamics, pattern NOT have same approximation

    # for pattern, GUI allows duplicate and delete, but not rename, name is e.g. "Amethyst copy"
    # no API for duplicate, rename, or delete
    # script-fu-paste-as-pattern will allow create a named pattern




def improviseFileParam():
    '''
    Create a parameter:
       in the Python language
       that designates a file
       in a call to a GIMP PDB procedure

    We only need a string that is a file name.
    GimpFu itself will convert to what PDB procedures want (a GFile.)

    When converting to GFile, a prefix path is added (to the current working directory.)
    The string here is just a filename, and must not name directories that don't exist yet.
    Although the filename doesn't need to exist as a file.
    '''
    filename = "fooFileName.tmp"
    logger.debug(f"Improvised filename: {filename}")
    return filename

"""
CRUFT : don't need to create a GFile here.

Is it a GFile or a GLocalFile?
Web says GLocalFile is an internal type?

Probably need a patch to GimpFu to create a GValue of type GFile
when it sees it is needed.

    # create a named file
    # fooFile = Gio.file_new_for_path("/work/foo")

    # create a temporary file.  This creates a real file, does IO?
    # fooFile, stream = Gio.file_new_tmp(None)
    # Not used: stream

    # create for a parse name
    fooFile = Gio.file_parse_name("/work/foo")

    assert fooFile is not None

    # fooFile is-a GLocalFile, i.e. file doesn't exist yet if path is malformed
    # create the file?
    logger.debug(f"Created fooFile: {fooFile.get_parse_name()} types: {fooFile.__gtype__} ")
    #raise Exception
"""


def improviseFooParameters(image, drawable):
    """
    Create instances of various Gimp types.
    Passed as args to PDB procedures, by name.
    Used like 'image', 'drawable', instances passed into the tests.
    """

    """
    Use any vectors in the image, else improvise one
    """
    # GimpFu, not gi
    fooVectors = gimp.Vectors(image, "foo")
    if fooVectors is None:
        fooVectors = pdb.gimp_vectors_new()
        # is empty, and is not attached to image
    if fooVectors is None:
        logger.warning(f"fooVectors is None, tests requiring vector args will fail.")


    fooFile = improviseFileParam()

    """
    Many procedures take an array of drawables.
    We don't create a global fooDrawableArray since GimpFu will automatically convert Drawable to GimpDrawableArray
    where required.
    """

    return fooVectors, fooFile
