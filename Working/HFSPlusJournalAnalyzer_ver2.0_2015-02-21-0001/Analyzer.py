from Utility import *
from struct import *
from HFSPlus_ParseModule import *
from HFSPlus_JournalTrack import *
from HFSPlus_sStructure import *
from types import MethodType
from collections import *
from Output import *
import types
import Collector
import sys
import datetime
import csv

def catalogFileAnalyzer(catalogFile,tranBlocks):

    modifiedNodes=[]
    for i in range(1,trnaBlock[0]+1):
        if tranBlocks[i].blockType[0]==2 and tranBlocks[i].offset not in modifiedNodes:
            modifiedNodes.append(tranBlocks[i].offset)

    nodeSize,temp1,totalNodes=unpack_from('>HHL',catalogFile,32)

    nodePointer=0
    for i in range(1,totalNodes):

        nodePointer+=nodeSize

        if nodePointer not in modifiedNodes and ord(catalogFile[nodePointer+8])==0xFF:

            numRecords=unpack_from('>H',catalogFile,nodePointer+10)

            for j in range(numRecords):

                offset=nodePointer+unpack_from('>H',catalogFile,nodePointer+nodeSize-2*(j+1))
                        
                keyLength=unpack_from('>H',catalogFile,offset)

                if unpack_from('>H',catalogFile,offset+keyLength+2)<3:

                    parentID=unpack_from('>L',catalogFile,offset+2)

                    for k in range(unpack_from('>H',catalogFile,offset+6)):
                        nodeName+=('\u'+catalogFile[offset+8+2*k].encode('hex')+catalogFile[offset+8+2*k+1].encode('hex')).decode('unicode-escape')

                    offset+=2+keyLength
                    
                    CNID=unpack_from('>L',catalogFile,offset+keyLength+0xA)

                elif unpack_from('>H',catalogFile,offset+keyLength+2)<5:

                    CNID=unpack_from('>L',catalogFile,offset+2)

                    offset+=2+keyLength
                    
                    parentID=unpack_from('>L',catalogFile,offset+4)

                    nodeName=u''
                    for k in range(unpack_from('>H',catalogFile,offset+8)):
                        nodeName+=('\u'+catalogFile[offset+2*k+10].encode('hex')+catalogFile[offset+2*k+11].encode('hex')).decode('unicode-escape')
                    
                nameAndParent[0][CNID]=[nodeName,parentID]


def parsingBlock(specialFileFork,allocBlockSize):

    nonLeafNode=[BTIndexNode,BTHeaderNode,BTMapNode]
    leafNodeType=[ExtentsLeafNode,CatalogLeafNode,AttrLeafNode]

    if self.offset==1024:

        self.blockType.append(4)
        self.content=VolumeHeader(self.content)
    
    for i in range(3):
        
        check=False
        offset=0

        for j in range(8):

            if specialFileFork[i].extents[j].startBlock*allocBlockSize<=self.offset<(specialFileFork[i].extents[j].startBlock+specialFileFork[i].extents[j])*allocBlockSize:
                offset+=self.offset-specialFileFork[i].extents[j].startBlock*allocBlockSize
                check=True
                break

            self.offset=offset+specialFileFork[i].extents[j].startBlock*allocBlockSize
            
        if check:

            self.blockType.append(i)

            if k>0:

                kind=ord(self.content[8])
                self.blockType.append(kind)

                if kind==255:
                    self.content=leafNodeType[i](self.content,size)

                else:
                    self.content=nonLeafNode[kind]

            else:
                self.allocDataAnalyzer()

            break


def allocDataAnalyzer(self):

    allocatedBlock=[0]
    bitOffset=self.offset*8
    start=-1
    for k in range(size):
        for l in range(8):

            if start==-1 and (ord(self.content[k])>>(7-l))%2==1:
                start==k*8+l

            elif start!=-1 and (ord(self.content[k])>>(7-l))%2==0:

                allocatedBlock[0]+=1
                allocatedBlock.append((start+bitOffset,k*8+l-start))
                start=-1
    
    for k in range(1,existentExtent[0]+1):

        if existentExtent[k].state==1:

            check=0

            if RangeChecking(bitOffset,self.size*8,existentExtent[k].startBlock,existentExtent[k].blockCount)==2:
                
                check=1
                for l in range(1,allocatedBlock[0]+1):
                    if RangeChecking(allocatedBlock[l][0],allocatedBlock[l][1],existentExtent[k].startBlock,existentExtent[k].blockCount):
                        check=2
                        break
                        
            elif bitOffset<=existentExtent[k].startBlock<bitOffset+tranLen*8:
                
                check=1
                for l in range(1,allocatedBlock[0]+1):
                    if allocatedBlock[l][0]<=existentExtent[k].startBlock and allocatedBlock[l][0]+allocatedBlock[l][1]==bitOffset+tranLen*8:
                        check=2
                        break

            elif bitOffset<existentExtent[k].startBlock+existentExtent[k].blockCount<=bitOffset+tranLen*8:

                check=1
                for l in range(1,allocatedBlock[0]+1):
                    if allocatedBlock[l][0]==bitOffset and allocatedBlock[l][0]+allocatedBlock[l][1]>=existentExtent[k].startBlock+existentExtent[k].blockCount:
                        check=2
                        break

            if check==2:
                allocatedBlock.pop(l)
                allocatedBlock[0]-=1

            elif check==1:
                existentExtent[k].state=0


def modifiedInit(self):

    self.startBlock,self.blockCount=unpack('>LL')

    if self.startBlock!=0 or self.blockCount!=0:

        n=1
        while n<=existentExtent[0]:

            if RangeChecking(existentExtent[n].startBlock,existentExtent[n].blockCount,self.startBlock,self.blockCount)>0:

                existentExtent[n].state=-1
                existentExtent.pop(n)
                existentExtent[0]-=1
                n-=1

            n+=1

        existentExtent[0]+=1
        existentExtent.append(self)


def initFullPath(self):

    nameAndParent[1][self.CNID]=[self.nodeName,self.parentID]
    fullPath=[]

    i=self.CNID
    while i in nameAndParent[1].keys():
        fullPath.insert(0,'/{0}'.format(nameAndParent[1][i][0]))
        i=nameAndParent[1][i][1]

    self.fullPath=u''.join(fullPath)
    self.unidentifiedAncestor=i


def completeFullPath(self):

    fullPath=[]

    i=self.unidentifiedAncestor
    while i!=1:

        if i not in nameAndParent[0].keys():

            self.fullPath='unknown'
            fullPath=[]
            break

        fullPath.insert(0,'/{0}'.format(nameAndParent[0][j][0]))
        i=nameAndParent[0][j][1]

    self.fullPath+=u''.join(fullPath)


def initFullPathOfRecords(self):

    self.records.initFullPath()


def completeFullPathOfRecords(self):

    self.records.completeFullPath()


def main(option):

    if 'i' in option:

        temp=Collector.main(option)
        journal=temp[0]
        vh=temp[1]
        allocationFile=temp[2]
        extentsFile=temp[3]
        catalogFile=temp[4]
        attributesFile=temp[5]

    else:

        f=open(option['j'],'rb')
        journal=f.read()
        f.close()

        files=[]
        for i in ['v','al','e','c','at']:
            if i in option:

                f=open(option[i],'rb')
                files.append(f.read())
                f.close()

            else:
                files.append(0)

        vh=files[0]
        allocationFile=files[1]
        extentsFile=files[2]
        catalogFile=files[3]
        attributesFile=files[4]

    print 'Analyzing journal...'
    jParseList=journalParser(journal)[0]
    #jT = journalTrack(jParseList)

    path='result{0}'.format(option['id'])

    DirectoryCleaning(path)

    rawCSV(path,jParseList)
    rawSQLite3(path,jParseList)

    if 'r' in option:
        recovery(option['l'],path,option['r'],jParseList,vh)

if __name__=='__main__':
    main(translatingInput(sys.argv))