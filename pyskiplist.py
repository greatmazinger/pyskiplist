#
# This implements skiplists as described in:
# "Skip Lists: A Probabilistic Alternative to Balanced Trees" by William Pugh.
#
# The level generation is fixed to reach a maximum size according to the
# expected size. Although this is not the pure version, Pugh does recommend it
# for practical use.
#
# The default probability p = 1/2. 
# The class End is used to create a sentinel for the end of the list.
#
# My inspiration was taken from:
#       http://code.activestate.com/recipes/576930/
#

from math import log
from random import random, seed

class Node( object ):
    def __init__( self,
                  value = None, 
                  next = [] ):
        self.value = value
        self.next = next

class End( object ):
    def __cmp__( self, other ):
        return 1 # always greater than any other object

END = Node( End(), [] )

class SkipList:
    def __init__( self, expected_size = 100, p = 0.5 ):
        self.size = 0
        self.maxlevels = int( log(expected_size, 2) + 1 )
        self.head = Node( 'HEAD', [END] * self.maxlevels )
        self.p = p

    def random_level( self ):
        lev = 1
        while ((random() < self.p) and (lev < self.maxlevels)):
            lev = lev + 1
        return lev

    def insert( self, value ):
        saveprev = [None] * self.maxlevels
        node = self.head
        for lev in reversed( range(self.maxlevels) ):
            while (node.next[lev].value <= value):
                node = node.next[lev]
            saveprev[lev] = node
        new = Node( value = value,
                    next = [ None ] * self.random_level() )
        for lev in range( len(new.next) ):
            # saveprev[lev] points to new[lev]
            tmp = saveprev[lev].next[lev]
            saveprev[lev].next[lev] = new
            new.next[lev] = tmp
        self.size = self.size + 1

    def delete( self, value ):
        node = self.head
        saveprev = [None] * self.maxlevels
        for lev in reversed( range(self.maxlevels) ):
            while (node.next[lev].value < value):
                node = node.next[lev]
            saveprev[lev] = node
        node = saveprev[0].next[0]
        if node.value == value:
            # saveprev[0] points to the node to be deleted
            for lev in range( self.maxlevels ):
                if saveprev[lev].next[lev] != node:
                    break
                saveprev[lev].next[lev] = node.next[lev]
                node.next[lev] = None
            self.size = self.size - 1

    def printme( self ):
        print "Size = ", self.size
        print "Maxlevels = ", self.maxlevels
        node = self.head
        node = node.next[0]
        while (node != END):
            print "->", node.value,
            node = node.next[0]
        print

if __name__ == "__main__":
    # Simple test
    # TODO: This should be put in a test suite.
    from random import randint
    seed( 8 )
    l = [ randint(0, 90000) for x in xrange(800000) ]
    seed( 31 )
    print "Running myskiplist test:"
    mylist = SkipList( expected_size = 800000, p = 0.25 )
    for x in l:
        mylist.insert( x )
    print "Initial list:"
    print "Size:", mylist.size
    # mylist.printme()
    # delete some keys
    d = [ randint(0, 90000) for x in xrange(2000000) ]
    # d = [510, 507]
    for x in d:
        # print "Deleting key:", x
        mylist.delete(x)
    print "After deletes:"
    print "Size:", mylist.size
    # mylist.printme()
    print "Done."
