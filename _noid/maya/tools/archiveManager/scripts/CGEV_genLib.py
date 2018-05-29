import pymel.core as pm

import os
import time
import string
from functools import wraps
from maya import mel
import random
import math



def viewportOff(func):
    """
    Decorator - turn off Maya display while func is running.
    if func will fail, the error will be raised after.
    """
    @wraps(func)
    def wrap(*args, **kwargs):

        # Turn $gMainPane Off:
        mel.eval("paneLayout -e -manage false $gMainPane")

        # Decorator will try/except running the function.
        # But it will always turn on the viewport at the end.
        # In case the function failed, it will prevent maya viewport off.
        try:
            return func(*args, **kwargs)
        except Exception:
            raise  # will raise original error
        finally:
            mel.eval("paneLayout -e -manage true $gMainPane")

    return wrap


def human_time_diff(elapsed):
    hours, remainder = divmod(elapsed, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{0}h {1}m {2}s'.format(int(hours), int(minutes), int(seconds))


def getNodes(grp=None,nodeType='Transform',dataType=0,mainWindow=None):

    nodes=list()
    nType=eval('pm.nodetypes.'+nodeType)
    dType={0:'node',1:'node.longName()'}

    if grp==None:
        grpNode=[item for item in pm.ls (sl=1)]
    else:
        grpNode=[item for item in pm.ls (grp)]

    if grp=='type':
        listAll=grpNode=pm.ls(type=nodeType)

    else:
        listAll=pm.listRelatives(grpNode,ad=1,f=True,ni=True)
    if mainWindow:
        mainWindow.setupProgressBar(len(grpNode),'GET NODES')
    for node in grpNode:
        if grp=='type':
            nodes=[eval(dType[dataType]) for node in listAll ]

        else:
            nodes=[eval(dType[dataType]) for node in listAll if isinstance(node,nType)]
        if mainWindow:
            mainWindow.growBar()
    if dataType!=0:
        nodes.sort(key=len,reverse=True)

    return nodes


def getParentNodes(grp,nodeType='mesh',dataType=0,mainWindow=None):

    nodes=list()
    get_nodes=getNodes(grp,'Transform',0,mainWindow=mainWindow)
    dType={0:'node',1:'node.longName()'}

    for node in get_nodes:

        child=node.childAtIndex(0)

        if  pm.nodeType(child) == nodeType:
            nodes.append(eval(dType[dataType]))
    if dataType!=0:
        nodes.sort(key=len,reverse=True)

    return nodes


def attrCmd(mode=0,cmd='',nodes=list(),attrList=list(),dataType=list(),value=list()):

    '''
    2 modes to control attr :

    -0 add attr
    -1 delete ,set,get attr

    '''

    listAttr=list()

    for node in nodes:

        attrs=list()
        values=list()

        i=0
        for attr in attrList:

            if mode==0:
                if pm.attributeQuery(attr,n=node,exists=True)==False:

                    if dataType[i]=='string':
                        pm.addAttr(node,ln=attr,dt=dataType[i])
                    else:
                        pm.addAttr(node,ln=attr,at=dataType[i])

            elif mode==1:

                if pm.attributeQuery(attr,n=node,exists=True)==True:
                    attrs.append(attr)
                    nodeAttr=node.attr(attr)

                    if cmd=='delete':
                        funct=getattr(nodeAttr,cmd)()

                    else:
                        funct=getattr(nodeAttr,cmd)(value[i])
                        values.append(funct)

            i+=1
        listAttr.append({'node':node,'attrs':attrs,'values':values})
    return listAttr


def getTransform(node,space='world'):
    dictTransform={}
    pos=node.getTranslation(space)
    rot=node.getRotation(space)
    scale=node.getScale()

    dictTransform={'position':pos,'rotation':rot,'scale':scale}
    return dictTransform


def getNodeMatrix(node):
    matrix=pm.PyNode(node).getMatrix()
    return matrix

def setNodeMatrix(node,matrix):
    pm.PyNode(node).setMatrix(matrix)



def randomColor(size,format=255):

    allColors=list()

    for index in range(size):

        rgb=list()

        for color in range(3):

            randc=random.randint(0,255)
            randf=round((randc/float(format)),1)
            rgb.append(randf)

        allColors.append(rgb)

    return allColors


def createSet(setName=''):

    allSet=pm.ls(type='objectSet')
    vps=()
    if setName in allSet:
        vps=pm.PyNode(setName)
    else:
        vps=pm.sets(n=setName,em=True)
    setMembers=(setName,vps.members())
    return setMembers


def getSetMembers(setName='') :

    allSet=pm.ls(type='objectSet')
    vproxyGrp=list()
    vproxyGrpName=list()
    for set in allSet:
        if set==setName:
            vproxyGrp=set.members()
    if vproxyGrp :
        for grp in vproxyGrp:
            vproxyGrpName.append(grp.name())

        return vproxyGrpName


def getPtcInstancer(ptcNode=''):
    ptcInst=pm.particleInstancer(ptcNode='', q=True, name=True )
    if ptcInst:
        return ptcInst[0]


def stCross(a, b ):

    """Computes a cross product"""

    c = [a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]]
    return c
