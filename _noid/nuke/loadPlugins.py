import nuke
import LensDistort.LensDistort_3de

def main() :
    toolbar= nuke.toolbar("Nodes")
    m= toolbar.addMenu("NOID")
    m.addCommand("ChromaticAberation", "nuke.createNode('ChromaticAberation')")

