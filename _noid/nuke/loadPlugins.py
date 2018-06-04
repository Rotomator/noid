import nuke
import LensDistort.LensDistort_3de

<<<<<<< HEAD
toolbar = nuke.toolbar("Nodes")
m= toolbar.addMenu("NOID")
m.addCommand("ChromaticAberation", "nuke.createNode('ChromaticAberation')")
=======
def main() :
    toolbar= nuke.toolbar("Nodes")
    m= toolbar.addMenu("NOID")
    m.addCommand("ChromaticAberation", "nuke.createNode('ChromaticAberation')")
>>>>>>> c19bfa8b2e3b225b306790e2ed7f77464ba1d0e0

