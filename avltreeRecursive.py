myavllist = [150,40,900,300,700,60,500,160,450,600,30,80,430]

class Node(object):
    def __init__(self,key,parent=None):
        self.key = key
        self.parent = parent
        self.L_child = None
        self.R_child = None
        self.L_hight = 0
        self.R_hight = 0
        self.hight = 0

    def isLeaf(self):
        if self.L_child ==None and self.R_child==None:
            return True
        else:
            return False
    
    def leafDeletion(self):
        #just make its parent pointing to none and update its parent hight
        par = self.parent
        if par.L_child is not None and par.L_child is self:
            par.L_child = None
            par.L_hight = 0
        else:
            par.R_child = None
            par.R_hight = 0


    def updateHight(self):
        if self.L_child is not None:
            self.L_hight = self.L_child.hight + 1
        else:
            self.L_hight = 0
        if self.R_child is not None:
            self.R_hight = self.R_child.hight + 1
        else:
            self.R_hight = 0
        self.hight = max(self.L_hight,self.R_hight)
    
    def isRoot(self):
        if self.parent is None:
            return True
        else:
            return False

    def balance(self):
        L=0
        R=0
        if self.L_child is not None:
            L = self.L_hight
        if self.R_child is not None:
            R = self.R_hight
        return R - L



class AVLtree(object):
    def __init__(self,node=None):
        self.rootNode = node

    def sameNodes(self,node1,node2):
        same = False
        if node1 is not None and node2 is not None:
            if node1.key == node2.key:
                same = True
        return same

    def reBalance(self,uNode):
        if uNode.balance() > 1:
            if uNode.R_child.balance() < 0 :
                #double left rotation
                self.RRotation(uNode.R_child)
                self.LRotation(uNode)
            else:
                self.LRotation(uNode)
        elif uNode.balance() < -1:
            if uNode.L_child.balance() > 0 :
                #double right rotation
                self.LRotation(uNode.L_child)
                self.RRotation(uNode)
            else:
                self.RRotation(uNode)


    def accessNode(self,key,cur_node=None):
        if cur_node is None:
            cur_node = self.rootNode
        print "key: %d with hight %d" %(cur_node.key,cur_node.hight)
        if key<cur_node.key:
            if cur_node.L_child == None:
                print "FAILURE:key not found"
            else:
                self.accessNode(key,cur_node.L_child)
        elif key>cur_node.key:
            if cur_node.R_child == None:
                print "FAILURE:key not found"
            else:
                self.accessNode(key,cur_node.R_child)
        else:
            print "Found Key!!!"

    def attachOnLeft(self,cur_node,key):
        cur_node.L_child = Node(key,cur_node)
        cur_node.L_hight += 1
        cur_node.hight = max(cur_node.L_hight,cur_node.R_hight)

    def attachOnRight(self,cur_node,key):
        cur_node.R_child = Node(key,cur_node)
        cur_node.R_hight += 1
        cur_node.hight = max(cur_node.L_hight,cur_node.R_hight)

    def LRotation(self,rotatedNode):
        newRoot = rotatedNode.R_child
        #correct the relation of the new root with the parent of rotated node
        if not rotatedNode.isRoot():
            newRoot.parent = rotatedNode.parent
            #if rotatedNode.parent.L_child is rotatedNode:
            if self.sameNodes(rotatedNode.parent.L_child,rotatedNode):
                rotatedNode.parent.L_child = newRoot
            else:
                rotatedNode.parent.R_child = newRoot
        else:
            newRoot.parent = None
            self.rootNode = newRoot
        #the left child(if exists) of the new root node becomes the right child of the rotated node
        rotatedNode.R_child = newRoot.L_child
        if newRoot.L_child is not None:
            newRoot.L_child.parent = rotatedNode
        #the rotated node becomes the left child of the new root node
        rotatedNode.parent = newRoot
        newRoot.L_child = rotatedNode
        #correct each hight of subtree
        self.updatehight(rotatedNode)
        self.updatehight(newRoot)

    def RRotation(self,rotatedNode):
        newRoot = rotatedNode.L_child
        #correct the relation of the new root with the parent of rotated node
        if not rotatedNode.isRoot():
            newRoot.parent = rotatedNode.parent
            if self.sameNodes(rotatedNode.parent.L_child,rotatedNode):
                rotatedNode.parent.L_child = newRoot
            else:
                rotatedNode.parent.R_child = newRoot
        else:
            newRoot.parent = None
            self.rootNode = newRoot
        #the left child(if exists) of the new root node becomes the right child of the rotated node
        rotatedNode.L_child = newRoot.R_child
        if newRoot.R_child is not None:
            newRoot.R_child.parent = rotatedNode
        #the rotated node becomes the left child of the new root node
        rotatedNode.parent = newRoot
        newRoot.R_child = rotatedNode
        #correct each hight of subtree
        self.updatehight(rotatedNode)
        self.updatehight(newRoot)

    def updatehight(self,cur_node):
        if cur_node.L_child is not None:
            cur_node.L_hight = cur_node.L_child.hight + 1
        else:
            cur_node.L_hight = 0
        if cur_node.R_child is not None:
            cur_node.R_hight = cur_node.R_child.hight + 1
        else:
            cur_node.R_hight = 0
        cur_node.hight = max(cur_node.L_hight,cur_node.R_hight)

    def insertNode(self,key,cur_node=None):
        if cur_node is None:
            cur_node = self.rootNode
        if self.rootNode is None:
            self.rootNode = Node(key)
            return
        if key<cur_node.key:
            if cur_node.L_child == None:
                self.attachOnLeft(cur_node,key)
            else:
                self.insertNode(key,cur_node.L_child)
        else:
            if cur_node.R_child == None:
                self.attachOnRight(cur_node,key)
            else:
                self.insertNode(key,cur_node.R_child)
        self.updatehight(cur_node)
        if cur_node.balance() > 1 or cur_node.balance() < -1:
            self.reBalance(cur_node)

    def swapNodeData(self,node1,node2):
        tempKey = node1.key
        node1.key = node2.key
        node2.key = tempKey


    def deleteNode(self,s_key,cur_node = None):
        if cur_node is None:
            cur_node = self.rootNode
        if s_key < cur_node.key:
            self.deleteNode(s_key,cur_node.L_child)
        elif s_key > cur_node.key:
            self.deleteNode(s_key,cur_node.R_child)
        elif s_key == cur_node.key:
            #key to delete found.Start the deletion process
            #if node is a leaf just make its parent pointing to none
            if cur_node.isLeaf():
                cur_node.leafDeletion()
            else:
                self.findProcAndDel(cur_node.L_child,cur_node)
        else:
            print "FAILURE:key not found"
            return
        cur_node.updateHight()
        if cur_node.balance() > 1 or cur_node.balance() < -1:
            self.reBalance(cur_node)
        
    def findProcAndDel(self,cnode,dnode):
        if cnode.R_child is not None:
             self.findProcAndDel(cnode.R_child,dnode)
        else:
            if cnode.isLeaf():
                cnode.leafDeletion()
            else:
                cnode.parent.R_child = cnode.L_child
                cnode.L_child.parent = cnode.parent
                cnode.parent.R_hight -= 1
            self.swapNodeData(cnode,dnode)
        cnode.updateHight()
        if cnode.balance() > 1 or cnode.balance() < -1:
            self.reBalance(cnode)
         


myavl = AVLtree()
#myavl.rootNode = Node(150,None) #initialize the root node
for i in myavllist:
    myavl.insertNode(i)
myavl.accessNode(600)
myavl.deleteNode(500)
myavl.accessNode(430)

# myavl2 = AVLtree()
# myavl2.rootNode = Node(3,None)
# myavl2.insertNode(1)
# myavl2.insertNode(2)
# #myavl2.reBalance(myavl2.rootNode)
# myavl2.accessNode(1)
"""
sources
http://interactivepython.org/runestone/static/pythonds/Trees/AVLTreeImplementation.html
https://www.cs.usfca.edu/~galles/visualization/AVLtree.html
http://www.cise.ufl.edu/~nemo/cop3530/AVL-Tree-Rotations.pdf
Deletion:
http://www.cs.toronto.edu/~krueger/cscB63h/lectures/tut03.txt
"""

