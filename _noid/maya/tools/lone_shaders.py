from cgev.common import log

try:
    import maya.cmds as cmds  # @UnresolvedImport
except ImportError:
    log.error("Failed to import maya.cmds module")


def getLoneSG():
    to_bind = list()

    log.info("Retrieve orphan SGs ...")

    # should be the "right" command but returns None sometimes :/
    # for name in cmds.listSets(t=1):

    for name in cmds.ls(type="shadingEngine"):
        if not cmds.objExists(name):
            continue

        if name.startswith("initial"):
            log.info("{0} is a base SG", name)
            continue

        if not cmds.listConnections(name + ".surfaceShader"):
            log.info("{0} has no shader associated", name)
            continue

        if cmds.sets(name, q=True):
            log.info("{0} already has members", name)
            continue

        log.info("{0} seem empty", name)
        to_bind.append(name)

    return to_bind


def attachLoneShaders():
    shading_groups = getLoneSG()

    if shading_groups:
        log.info("Got SG to attach : {0}", shading_groups)

        grp = "dummy_attachments"
        if cmds.objExists(grp):
            log.info(". delete dummy group {0}", grp)
            cmds.delete(grp)

        objects = list()

        for sg in shading_groups:
            log.info("... {0}", sg)
            obj = cmds.particle()
            obj = cmds.ls(obj, transforms=True)[0]

            objects.append(obj)
            cmds.sets(obj, e=True, forceElement=sg)

        grp = cmds.group(objects, name=grp)

        result = cmds.ls(type='renderLayer')
        for renderLayer in result:
            cmds.editRenderLayerMembers(renderLayer, grp)

        cmds.scale(0.00001, 0.00001, 0.00001, grp)
    else:
        log.info("SG attachments ok !")


def detachLoneShaders():
    grp = "dummy_attachments"
    if cmds.objExists(grp):
        log.info(". delete dummy group {0}", grp)
        cmds.delete(grp)
