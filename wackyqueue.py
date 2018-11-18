"""
# Copyright Nick Cheng, 2018
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 1, CSCA48, Winter 2018
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.

Modify by: Chengyu Xin
Student number: 1004068518
utorid: xincheng
"""

from wackynode import WackyNode

# Do not add import statements or change the one above.
# Write your WackyQueue class code below.


class WackyQueue():
    '''Class of WackyQueue'''

    def __init__(self):
        '''(WackyQueue) -> NoneType
        This is the init method in <WackyQueue> for initializing variables
        '''
        # create odd and even linked list both with a dummy WackyNode
        self._oddlist = WackyNode(None, 0)
        self._evenlist = WackyNode(None, 0)

    def insert(self, item, pri):
        '''(WackyQueue, obj, int) -> NoneType
        Insert a WackyNode with <item> object
        and <pri> as its priority into WackyQueue
        '''
        def insert_process(insert_node, before, after, gap, connect):
            '''(WackyNode, WackyNode, WackyNode, WackyNode,
            WackyNode) -> NoneType
            A helper function for the process when inserting a WackyNode
            in the WackyQueue, it organizes the WackyQueue in correct order
            after inserting
            '''
            # connect the insert WackyNode in correct order
            before.set_next(insert_node)
            insert_node.set_next(after)
            gap.set_next(connect)
        # create a WackyNode to insert
        new_node = WackyNode(item, pri)
        # initialize variables for looping by heapler function
        curr, oprev, ocurr, eprev, ecurr = set_variables(self._oddlist,
                                                         self._evenlist)
        # create a flag. When flag is True, current and odd current are
        # at the same position, vise versa
        flag = True
        # loop through two linked list to find the insert position
        while curr and curr.get_priority() >= pri:
            # check if current and odd current are at the same position
            if flag:
                # Do the looping process by helper function
                curr, oprev, ocurr = loop_process(curr, oprev, ocurr,
                                                  curr.get_next(), ecurr)
            # else current and even current are at the same position
            else:
                # Do the looping process by helper function
                curr, eprev, ecurr = loop_process(curr, eprev, ecurr,
                                                  curr.get_next(), ocurr)
            # switch the state of flag
            flag = not flag
        # if current and odd current are at the same position after the loop
        if flag:
            # insert the new WackyNode in correct order by helper function
            insert_process(new_node, oprev, ecurr, eprev, ocurr)
        # else current and even current are at same position after the loop
        else:
            # insert the new WackyNode in correct order by helper function
            insert_process(new_node, eprev, ocurr, oprev, ecurr)

    def extracthigh(self):
        '''(WackyQueue) -> obj
        Remove and return the first item in the wacky queue
        REQ: WackyQueue is not empty
        '''
        # get the first WackyNode in odd linked list
        first = self._oddlist.get_next()
        # rearrange odd and even linked list to correct order after extracting
        self._oddlist.set_next(self._evenlist.get_next())
        self._evenlist.set_next(first.get_next())
        # return the first item
        return first.get_item()

    def isempty(self):
        '''(WackyQueue) -> bool
        Return Ture if WackyQueue is empty
        '''
        # return the result if oddlist is empty without dummy
        return self._oddlist.get_next() is None

    def changepriority(self, item, pri):
        '''(WackyQueue, obj, int) -> NoneType
        Change the priority of the first copy of object <item> to priority
        <pri>, the wacky queue is unchange if object is not in WackyQueue or
        already has priority <pri>
        '''
        def delete_process(prev1, curr1, prev2, curr2):
            '''(WackyNode, WackyNode, WackyNode, WackyNode) -> NoneType
            A helper function for the delete process when changing
            a WackyNode's priority in the WackyQueue, it organizes the
            WackyQueue in correct order after deleting the WackyNode
            '''
            # connect the rest of WackyNodes in correct order
            prev1.set_next(curr1)
            prev2.set_next(curr2.get_next())
        # initialize variables for looping by heapler function
        curr, oprev, ocurr, eprev, ecurr = set_variables(self._oddlist,
                                                         self._evenlist)
        # loop through two linked list to find the first copy of object
        while curr and curr.get_item() != item:
            # check if current and odd current are at the same position
            if curr == ocurr:
                # Do the looping process by helper function
                curr, oprev, ocurr = loop_process(curr, oprev, ocurr,
                                                  curr.get_next(), ecurr)
            # else current and even current are at the same position
            else:
                # Do the looping process by helper function
                curr, eprev, ecurr = loop_process(curr, eprev, ecurr,
                                                  curr.get_next(), ocurr)
        # if the object exist and it doesn't have the same priority as we want
        if curr and curr.get_priority() != pri:
            # if current and odd current are at the same position after loop
            if curr == ocurr:
                # delete the WackyNode with the object and connect the rest
                # of WackyNodes in correct order by helper function
                delete_process(oprev, ecurr, eprev, ocurr)
            # else current and even current are at the same position after loop
            else:
                # delete the WackyNode with the object and connect the rest
                # of WackyNodes in correct order by helper function
                delete_process(eprev, ocurr, oprev, ecurr)
            # insert the object back with new priority
            self.insert(item, pri)

    def negateall(self):
        '''(WackyQueue) -> NoneType
        Negate the priority of every object in the wacky queue
        '''
        def negate_process(curr, prev):
            '''(WackyNode, WackyNode) -> WackyNode
            A helper function for the process of negating the priority of
            every object in the WackyQueue, it negates the <curr> WackyNode's
            priority and switch the order with <prev> WackyNode
            Return the WackyNode in next position of <curr> WackyNode
            '''
            # save the next WackyNode of current Node for future use
            temp = curr.get_next()
            # negate the current WackyNode's priority
            curr.set_priority(-curr.get_priority())
            # reverse the order with its previous WackyNode
            curr.set_next(prev)
            return temp

        def decide_head(odd_head, even_head):
            '''(WackyNode, WackyNode) -> NoneType
            A helper function for choosing heads for odd and even list after
            negating in WackyQueue
            '''
            # set the head of the odd and even list after dummy
            self._oddlist.set_next(odd_head)
            self._evenlist.set_next(even_head)
        # initialize current and previous position in odd list
        oprev = None
        ocurr = self._oddlist.get_next()
        # initialize current and previous position in even list
        eprev = None
        ecurr = self._evenlist.get_next()
        # initialize a position alternating at odd and even current
        curr = ocurr
        # create a flag. When flag is True, current and odd current are
        # at the same position, vise versa
        flag = True
        # loop through two linked list to find the insert position
        while curr:
            # check if current and odd current are at the same position
            if flag:
                # Do the negating process on current by helper function
                temp = negate_process(curr, oprev)
                # Do the looping process by helper function
                curr, oprev, ocurr = loop_process(curr, oprev, ocurr,
                                                  temp, ecurr)
            # else current and even current are at the same position
            else:
                # Do the negating process on current by helper function
                temp = negate_process(curr, eprev)
                # Do the looping process by helper function
                curr, eprev, ecurr = loop_process(curr, eprev, ecurr,
                                                  temp, ocurr)
            # switch the state of flag
            flag = not flag
        # if current and odd current are at the same position after loop
        # which means total amount of WackyNodes are even
        if flag:
            # choose the head for odd and even list by helper function
            # switching two linked list with each other
            decide_head(eprev, oprev)
        # else current and even current are at the same position after loop
        # which means total amount of WackyNodes are odd
        else:
            # choose the head for odd and even list by helper function
            decide_head(oprev, eprev)

    def getoddlist(self):
        '''(WackyQueue) -> NoneType
        Return a pointer to a linked list of WackyNodes in odd position
        in the WackyQueue
        If there is no first object, then an empty list is returned
        '''
        # return the pointer to linked list of WackyNodes in odd position
        return self._oddlist.get_next()

    def getevenlist(self):
        '''(WackyQueue) -> NoneType
        Return a pointer to a linked list of WackyNodes in even position
        in the WackyQueue
        If there is no second object, then an empty list is returned
        '''
        # return the pointer to linked list of WackyNodes in even position
        return self._evenlist.get_next()


def set_variables(oddlist, evenlist):
    '''(obj, obj) -> WackyNode, WackyNode, WackyNode, WackyNode, WackyNode
    A helper function for initializing variables for loopping in WackyQueue
    Takes two pointers to two linked list which contains all the WackyNodes
    in the WackyQueue
    Returns five WackyNodes position for the loop
    '''
    # initialize current and previous position in odd list
    op = oddlist
    oc = oddlist.get_next()
    # initialize current and previous position in even list
    ep = evenlist
    ec = evenlist.get_next()
    # initialize a position alternating at odd and even current
    curr = oc
    # return five WackyNodes
    return curr, op, oc, ep, ec


def loop_process(alter_curr, prev, curr, temp, next_position):
    '''(WackyNode, WackyNode, WackyNode, WackyNode, WackyNode) -> WackyNode,
    WackyNode, WackyNode
    A helper function for the looping process in WackyQueue
    Returns three WackyNodes position for the loop
    '''
    # change alternative current to next position
    alter_curr = next_position
    # change previous and current to their next position respectively
    # to keep looping
    prev = curr
    curr = temp
    # return three position for next loop
    return alter_curr, prev, curr
