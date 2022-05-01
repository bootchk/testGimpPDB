
from gimpfu import *

# TODO excise this
import gi
gi.require_version("Gimp", "3.0")
from gi.repository import Gimp



def generateNewTextLayer(image):
    # cruft testing various forms, issue with Gimp.Unit symbols
    #result = pdb.gimp_text_layer_new(testImage, "Foo", "Courier", 12, Gimp.Unit.POINTS)
    #result = pdb.gimp_text_layer_new(testImage, "Foo", "Courier", 12, Gimp.SizeType.POINTS)
    #result = pdb.gimp_text_layer_new(testImage, "Foo", "Courier", 12, Gimp.Unit.POINT)

    # This works: pass int literal for unit
    return pdb.gimp_text_layer_new(image, "Foo", "Courier", 12, 1)


def generateNewColorLayer(image):
    """
    I tried several things here.

    The active layer is not necessarily part of testImage??
    Seemed to fail with "it is attached to another image"
    activeLayer = pdb.gimp_image_get_active_layer(testImage)

    Tried new from drawable.
    pdb.gimp_layer_new_from_drawable(activeLayer, testImage)
    """

    # width, height, type, name, opacity, mode
    # Don't care for type, mode to be any specific value.
    result = result = pdb.gimp_layer_new(image, 20, 20, 0, "testDrawable", 100, 0)
    return result


def generateDrawableAproposToProc(procName, testImage):
    """
    Generate a drawable from the test image.
    Appropriate to the proc, by examining procName.
    E.G. certain procedures want a text layer, a floating sel layer, or a group layer
    """
    if procName.find("text") > 0:
        result = generateNewTextLayer(testImage)

        """
        # TODO if "floating" create a floating selection layer
        WIP, it crashes
        elif procName.find("floating") > 0:
            # float the selection, getting a new layer
            drawable = pdb.gimp_image_get_active_drawable(testImage)
            # !!! Clunky num_drawables API. But GimpFu will convert instance to [instance]
            result = pdb.gimp_selection_float(1, drawable)  # TODO 0,0 ) offsets
        """
    else:
        result = generateNewColorLayer(testImage)

    # Add to image, most procedures want that.  parent layer none
    # ??? pdb.gimp_image_insert_layer(testImage, result, None )
    # ??? insert with no parent, at position 1    pdb.gimp_image_insert_layer(testImage, result, None, 1)
    testImage.insert_layer(result)

    #print(f"testImage: {testImage.filename}")
    #print(f"testLayer: {result.name}")

    # Assert the layer is attached to the image
    # The image property of a layer is the image to which the layer is attached.
    # Note we don't have any access to the ID's used on the wire
    assert (result.image == testImage)
    return result
