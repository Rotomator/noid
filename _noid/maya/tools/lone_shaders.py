import noid_log as log


try:
    import maya.cmds as cmds  # @UnresolvedImport
except ImportError:
    log.error("Failed to import maya.cmds module.")


def getLoneSG():
    to_bind = list()

    log.info("Retrieve orphan SGs...")

    # should be the "right" command but returns None sometimes :/
    # for name in cmds.listSets(t=1):

    for name in cmds.ls(type="shadingEngine"):
        if not cmds.objExists(name):
            continue

        if name.startswith("initial"):
            log.info("{} is a base SG".format(name))
            continue

        if not cmds.listConnections(name + ".surfaceShader"):
            log.info("{} has no shader associated".format(name))
            continue

        if cmds.sets(name, q=True):
            log.info("{} already has members".format(name))
            continue

        log.info("{} seems empty".format(name))
        to_bind.append(name)

    return to_bind


def attachLoneShaders():
    shading_groups = getLoneSG()

    if shading_groups:
        log.info("Got SG to attach : {}".format(shading_groups))

        grp = "dummy_attachments"
        if cmds.objExists(grp):
            log.info(". delete dummy group {}".format(grp))
            cmds.delete(grp)

        objects = list()

        for sg in shading_groups:
            log.info("... {}".format(sg))
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
        log.info(". delete dummy group {}".format(grp))
        cmds.delete(grp)
