class LinkedList:
	def __init__(self):
		self.head = None
		self.curr = None

	# This function prints contents of linked list 
    # starting from head 
    def printList(self): 
        temp = self.head 
        while (temp): 
            print temp.data, 
            temp = temp.next

    def insert(self, node):
    	"""
    		A method to insert a node into linked list in 
    		ascending order
    	"""
    	# If linked list is empty
    	if not self.head:
    		self.head = node
    		return

    	temp = self.head
    	while temp.next != None and temp.next.val < node.val:
    		temp = temp.next

    	next_node = temp.next
    	temp.next = node
    	node.next = next_node

    	return

    def remove(self, val):
    	# If linked list is empty
    	if not self.head:
    		return False

    	else:
    		curr = self.head
    		prev = None
    		while curr != None and curr.val != val:
    			curr = curr.next
    			prev = curr

    		if curr != None:
    			prev.next = curr.next
    			return True

    		return False

    def next(self):
    	if self.curr == None:
    		return self.head
    	else:
    		self.curr = self.curr.next
    		return self.curr
    def reset_iter(self):
    	self.curr = self.head
    	return


class Node:
    def __init__(self,val):
        self.val = val
        self.next = None 