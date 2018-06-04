# v150622 1515
# 3DE4.script.hide: true
#!/usr/bin/python

import math
import sys
import tools

import lens_distortion_plugins as ldp


def isodd(num):
        return num % 2


def evenize(number):
    if number > 0:
        number = int(math.ceil(number))
        if isodd(number):
            number = number+1
    else:
        number = int(math.floor(number))
        if isodd(number):
            number = number-1
    return number


# Convert box from unit to pixel
def unit2px(w_px, h_px, box):
    bottomx = evenize(w_px * box[0])
    bottomy = evenize(h_px * box[1])
    topx = evenize(w_px * box[2])
    topy = evenize(h_px * box[3])

    outx = topx-bottomx
    outy = topy-bottomy
    return tools.Resolution(outx, outy)


def get_bounding_box_ldm(ldm, direction):
    if direction == "undistort":
        return ldm.getBoundingBoxUndistort(0, 0, 1, 1, 32, 32)
    elif direction == "distort":
        return ldm.getBoundingBoxDistort(0, 0, 1, 1, 32, 32)
    else:
        return [0, 0, 1, 1]


def get_bounding_box(direction, folcalParameter, lensModelParameter):
    model = lensModelParameter['model']
    if model == '3DE Classic LD Model':
        ldm = ldp.classic_3de_mixed()
    if model == '3DE4 Anamorphic, Degree 6':
        ldm = ldp.anamorphic_deg_6()
    if model == '3DE4 Anamorphic - Standard, Degree 4':
        ldm = ldp.anamorphic_deg_4_rotate_squeeze_xy()
    if model == '3DE4 Radial - Standard, Degree 4':
        ldm = ldp.radial_decentered_deg_4_cylindric()
    if model == '3DE4 Radial - Fisheye, Degree 8':
        ldm = ldp.radial_deg_8()

    # Not a realistic filmback, just proxy data
    ldm.setParameterValueDouble("tde4_filmback_width_cm",
                                folcalParameter["filmW"])
    ldm.setParameterValueDouble("tde4_filmback_height_cm",
                                folcalParameter["filmH"])
    ldm.setParameterValueDouble("tde4_focal_length_cm",
                                folcalParameter["focalLength"])
    ldm.setParameterValueDouble("tde4_pixel_aspect",
                                folcalParameter["pixelAspect"])

    for parameterName in lensModelParameter:
        if parameterName != 'model':
            ldm.setParameterValueDouble(parameterName,
                                        lensModelParameter[parameterName])

    ldm.initializeParameters()

    return get_bounding_box_ldm(ldm, direction)


def calculateBoundigBox(originalSizeX, originalSizeY, direction,
                        folcalParameter, lensModelParameter):
    boundingBox = get_bounding_box(direction,
                                   folcalParameter,
                                   lensModelParameter)
    return unit2px(originalSizeX, originalSizeY, boundingBox)
