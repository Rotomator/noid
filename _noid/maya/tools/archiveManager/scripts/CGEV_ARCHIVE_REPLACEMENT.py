import pymel.core as pm
import maya.OpenMaya as om
import maya.mel as mel
import os
import random
import time
import re
import string
import operator
import math
import copy

from functools import wraps

import CGEV_genLib as gl
reload(gl)


#  prefix_familyName_familyType_index
# example:  -eo_chalet_S1_1

# no prefix work also
#example :  gingerbreadHouse_A_grp_25


@gl.viewportOff
def mayaNodes_replaceByArchive(mainWindow):


    dictFamily=dict();tmpNodeList=list();tmpArcList=list()

    allParents=[ item for item in gl.getParentNodes(None,'mesh',1) ]

    allParentsCopy=copy.copy(allParents)

    ''' EXCEPTION FOR VRAY PROXY'''

    for node in allParents:

        if "proxy" in node:

            newNode=pm.rename(node,node.replace("proxy","")).longName()

            allParentsCopy.remove(node)
            allParentsCopy.append(newNode)
        else:
            allParentsCopy.append(node)

    allParents= list( set (copy.copy(allParentsCopy) ) )

    hierarchyList=list()
    organizeList=list()

    for  item in allParents:


        hierarchyList.append( pm.PyNode(item).parentAtIndex(0).name(long=True))

    hierarchyList=list(set(hierarchyList))


    for elem in hierarchyList:


        nodeList=[node.longName() for node in pm.listRelatives(elem,c=True,type="transform") if node.longName() not in hierarchyList ]


        #check if ends with digit

        allObj_digit=list (set ( [ item.replace(item.split('|')[-1],item.split('|')[-1] .replace('_'+item.split('_')[-1],''))  for item in nodeList if  item.split('_')[-1].isdigit()] ) )

        allObj_nodigit=[ item.replace(item.split('|')[-1],item.split('|')[-1])  for item in nodeList if not item.split('_')[-1].isdigit() ]


        allObjLong=list ( set([item for item in (allObj_digit+allObj_nodigit)]))


        for obj in allObjLong:

            organizeList.append([elem,obj])



    ''' CREATE DICTFAMILY VALUE : NODES, PARENT'''
    i=0
    for item in organizeList:


        fam=item[1].split('|')[-1]


        dictFamily[fam+'_'+str(i)]={'nodes':[],'parent':item[0]}
        i+=1


    for node in allParents:

        parentNode=pm.PyNode(node).parentAtIndex(0).name(long=True)


        matchName=node.split('|')[-1].replace('_'+node.split('_')[-1],'')


        for key, value in dictFamily.iteritems():

            keyName=key.replace(('_'+key.split('_')[-1]),'')



            if keyName==matchName and value['parent']==parentNode:
                dictFamily[key]['nodes'].append(node)



    ''' MATCH ARCHIVE AND REPLACE NODE'''


    allArchive = [ node.parentAtIndex(0).name(long=True) for node in pm.ls(type='archiveNode') ]

    for key, value in dictFamily.iteritems():

        tmpNodeList=list()
        tmpArcList=list()

        mainWindow.setupProgressBar(len(value['nodes']),'replacing members of  '+key)

        for node in value['nodes']:


            matchName=node.split('|')[-1].replace('_'+node.split('_')[-1],'')


            for arc in allArchive:

                if arc.split('|')[-1]==matchName:

                    tmpNodeList.append(node)

                    matrix=gl.getNodeMatrix(pm.PyNode(node))
                    newArc=pm.duplicate(arc)[0].rename(node)
                    tmpArcList.append(newArc)
                    gl.setNodeMatrix(newArc,matrix)
                    mainWindow.growBar()
        pm.delete(tmpNodeList)
        pm.parent(tmpArcList,value['parent'])

