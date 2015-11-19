#!/usr/bin/python

import UIObjects
import getopt
import json
import sys
from SwiftGenerator import SwiftGenerator
from Validator import Validator


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print 'ParseJSON.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'ParseJSON.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print 'Input file is "', inputfile
    print 'Output file is "', outputfile

    style = json.loads(open(inputfile).read())

    validator = Validator()
    validator.validate(style)
    swiftgenerator = SwiftGenerator()
    ui = UIObjects

    _file = open(outputfile, "w+")
    swiftgenerator.openClass()

    if 'Fonts' in style:
        fontdefinitions = style['Fonts']
        swiftgenerator.buildFontConstants(fontdefinitions)

    if 'Colors' in style:
        colordefinitions = style['Colors']
        swiftgenerator.buildColorConstants(colordefinitions)

    if 'Images' in style:
        imagedefinitions = style['Images']
        swiftgenerator.buildImageConstants(imagedefinitions)

    if 'Labels' in style:
        for key, value in style['Labels'].iteritems():
            label = ui.uiObject(key + "Label", "UILabel")
            swiftgenerator.labelOutletCollections([label])

    if 'Buttons' in style:
        for key, value in style['Buttons'].iteritems():
            button = ui.uiObject(key + "Button", "UIButton")
            swiftgenerator.buttonOutletCollections([button])

    if 'TextFields' in style:
        for key, value in style['TextFields'].iteritems():
            textfield = ui.uiObject(key + "TextField", "UITextField")
            swiftgenerator.textFieldOutletCollection([textfield])

    for key, value in style['Labels'].iteritems():
        label = ui.Label(key + "Label", value)
        if label.attributes:
            swiftgenerator.buildAttributesForObjects([label.attributes])
        swiftgenerator.buildStyleFunctions([label])

    for key, value in style['Buttons'].iteritems():
        button = ui.Button(key + "Button", value)
        if button.normal:
            normal = value["normal"]
            if "titleColor" in normal:
                button.titleColorNormal = normal['titleColor']
            if "backgroundimage" in normal:
                button.backgroundimage = normal['backgroundimage']
        if button.selected:
            selected = value["selected"]
            if "titleColor" in selected:
                button.titleColorSelected = selected['titleColor']
            if "backgroundImage" in selected:
                button.backgroundimage = selected['backgroundimage']
        if button.highlighted:
            highlighted = value["highlighted"]
            if "titleColor" in highlighted:
                button.titleColorHighlighted = highlighted['titleColor']

        if button.attributes:
            swiftgenerator.buildAttributesForObjects([button.attributes])
        swiftgenerator.buildStyleFunctions([button])

    for key, value in style['TextFields'].iteritems():
        textfield = ui.TextField(key + "TextField", value)
        if "textcolor" in value:
            textfield.textcolor = value['textcolor']
        if textfield.attributes:
            swiftgenerator.buildAttributesForObjects([textfield.attributes])
        swiftgenerator.buildStyleFunctions([textfield])

        swiftgenerator.closeClass()

        # write and close file
        _file.write(swiftgenerator.end())
        _file.close()
        print swiftgenerator.end()


if __name__ == "__main__":
    main(sys.argv[1:])
