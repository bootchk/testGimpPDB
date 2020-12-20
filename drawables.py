
from gimpfu import *

# TODO excise this
import gi
gi.require_version("Gimp", "3.0")
from gi.repository import Gimp



def generateDrawableAproposToProc(procName, testImage):
    """
    Generate a drawable from the test image.
    Appropriate to the proc, by examining procName.
    E.G. certain procedures want a text layer, a floating sel layer, or a group layer
    """
    if procName.find("text") > 0:
        # Create a text layer

        # cruft testing various forms, issue with Gimp.Unit symbols
        #result = pdb.gimp_text_layer_new(testImage, "Foo", "Courier", 12, Gimp.Unit.POINTS)
        #result = pdb.gimp_text_layer_new(testImage, "Foo", "Courier", 12, Gimp.SizeType.POINTS)
        #result = pdb.gimp_text_layer_new(testImage, "Foo", "Courier", 12, Gimp.Unit.POINT)

        # This works: pass int literal
        result = pdb.gimp_text_layer_new(testImage, "Foo", "Courier", 12, 1)

        # Add to image, most procedures want that.  parent layer none
        # pdb.gimp_image_insert_layer(testImage, result, None )
        testImage.insert_layer(result)
        """
        WIP, it crashes
        elif procName.find("floating") > 0:
            # float the selection, getting a new layer
            drawable = pdb.gimp_image_get_active_drawable(testImage)
            # !!! Clunky num_drawables API. But GimpFu will convert instance to [instance]
            result = pdb.gimp_selection_float(1, drawable)  # TODO 0,0 ) offsets
        """
    else:
        result = pdb.gimp_image_get_active_drawable(testImage)
    # TODO if "floating" create a floating selection layer
    return result
