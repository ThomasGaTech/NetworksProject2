# Project 2 for OMS6250
#
# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.

from Message import *
from StpSwitch import *

class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):    
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)
        self.root = self.switchID
        self.distance = 0
        self.pathThrough = self.switchID
        self.activeLinks = []

    def send_initial_messages(self):

        for linkID in self.links:
            # Message(root, distance, origin, destination, pathThrough)
            message = Message(self.switchID, 0, self.switchID, linkID, False)
            self.send_message(message)
        return
        
    def process_message(self, message):
        # if they go through you add them to your active links
        if message.pathThrough:
            if message.origin not in self.activeLinks:
                self.activeLinks.append(message.origin)
        # if they don't go through you and you don't go through them delete them from your active links
        elif message.pathThrough == False and message.origin != self.pathThrough and message.origin in self.activeLinks:
            self.activeLinks.remove(message.origin)

        # if the message has a new root
        if message.root < self.root:
            self.root = message.root
            self.distance = message.distance + 1
            self.pathThrough = message.origin
            if self.pathThrough not in self.activeLinks:
                self.activeLinks.append(self.pathThrough)
            for linkID in self.links:
                message = Message(self.root, self.distance, self.switchID, linkID, self.pathThrough == linkID)
                self.send_message(message)
        # if the message has the same root but a shorter distance
        if message.root == self.root and message.distance + 1 < self.distance:
            self.distance = message.distance + 1
            newPathThrough = message.origin

            for linkID in self.links:
                message = Message(self.root, self.distance, self.switchID, linkID, newPathThrough == linkID)
                self.send_message(message)

            self.activeLinks.remove(self.pathThrough)
            self.pathThrough = newPathThrough
            if newPathThrough not in self.activeLinks:
                self.activeLinks.append(newPathThrough)
        # message has the same root and same distance but the sender has a smaller switchID than current path
        if message.root == self.root and message.distance + 1 == self.distance and self.pathThrough > message.origin:
            newPathThrough = message.origin

            for linkID in self.links:
                message = Message(self.root, self.distance, self.switchID, linkID, newPathThrough == linkID)
                self.send_message(message)

            self.activeLinks.remove(self.pathThrough)
            self.pathThrough = newPathThrough
            if newPathThrough not in self.activeLinks:
                self.activeLinks.append(newPathThrough)
        return
    
    def generate_logstring(self):
        linkStrings = []
        self.activeLinks.sort()
        for linkID in self.activeLinks:
            linkStrings.append(str(self.switchID) + ' - ' + str(linkID))
        return ', '.join(linkStrings)