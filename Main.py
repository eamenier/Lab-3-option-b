class avl_node: 
    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None
        self.parent = None
        self.height = 0

    def get_balance(self):
        left_height = -1
        if self.left_child is not None:
            left_height = self.left_child.height
        right_height = -1
        if self.right_child is not None:
            right_height = self.right_child.height
        return left_height - right_height

    def update_height(self):
        left_height = -1
        if self.left_child is not None:
            left_height = self.left_child.height
        right_height = -1
        if self.right_child is not None:
            right_height = self.right_child.height
        self.height = max(left_height, right_height) + 1

    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False
        if which_child == "left":
            self.left_child = child
        else:
            self.right_child = child
        if child is not None:
            child.parent = self
        self.update_height()
        return True

    def replace_child(self, current_child, new_child):
        if self.left_child is current_child:
            return self.set_child("left", new_child)
        elif self.right_child is current_child:
            return self.set_child("right", new_child)
        return False

class avl_tree(object): 
    def __init__(self):
        self.root = None

    def get_height(self, current):
        if current is None: return 0
        return current.height

    def insert(self, value):  
        node = avl_node(value)
        if self.root is None:  
            self.root = node
            self.root.parent = None
            return
        cur = self.root
        while cur is not None:  
            if node.value < cur.value:
                if cur.left_child is None:
                    cur.left_child = node
                    node.parent = cur
                    cur = None
                else:
                    cur = cur.left_child

            else:
                if cur.right_child is None:
                    cur.right_child = node
                    node.parent = cur
                    cur = None

                else:
                    cur = cur.right_child
        node = node.parent
        while node is not None: 
            self.rebalance(node)
            node = node.parent

    def rebalance(self, node): 
        node.update_height()
        if node.get_balance() == -2:
            if node.right_child.get_balance() == 1:
                self.right_rotate(node.right_child)
            return self.left_rotate(node)
        elif node.get_balance() == 2:
            if node.left_child.get_balance() == -1:
                self.left_rotate(node.left_child)
            return self.right_rotate(node)
        return node

    def right_rotate(self, node):  
        left_right_child = node.left_child.right_child
        if node.parent is not None:
            node.parent.replace_child(node, node.left_child)
        else:
            self.root = node.left_child
            self.root.parent = None

        node.left_child.set_child('right', node)
        node.set_child('left', left_right_child)

        return node.parent

    def left_rotate(self, node):  
        right_left_child = node.right_child.left_child
        if node.parent is not None:
            node.parent.replace_child(node, node.right_child)
        else:
            self.root = node.right_child
            self.root.parent = None

        node.right_child.set_child("left", node)
        node.set_child("right", right_left_child)

        return node.parent

    def search(self, value):  
        temp = self.root
        while temp is not None:
            if temp.value == value:
                return True
            elif temp.value < value:
                temp = temp.right_child
            else:
                temp = temp.left_child
        return False

class rbt_node(object): 
    def __init__(self, key, parent, is_red=False, left=None, right=None):
        self.key = key
        self.left_child = left
        self.right_child = right
        self.parent = parent
        if is_red:
            self.color = "red"
        else:
            self.color = "black"

    def both_children_black(self): 
        if self.left_child is not None and self.left_child.is_red():
            return False
        if self.right_child is not None and self.right_child.is_red():
            return False
        return True

    def count(self):
        count = 1
        if self.left_child is not None:
            count += self.left_child.count()
        if self.right_child is not None:
            count += self.right_child.count()
        return count

    def get_grandparent(self): 
        if self.parent is None:
            return None
        return self.parent.parent

    def get_siblings(self):
        if self.parent is not None:
            if self is self.parent.left_child:
                return self.parent.right_child
            return self.parent.left_child
        return None

    def get_uncle(self):
        grandparent = self.get_grandparent()
        if grandparent is None:
            return None
        if grandparent.left_child is self.parent:
            return grandparent.right_child
        return grandparent.left_child

    def is_black(self): 
        return self.color == "black"

    def is_red(self): 
        return self.color == "red"

    def replace_child(self, current_child, new_child):
        if self.left_child is current_child:
            return self.set_child("left", new_child)
        elif self.right_child is current_child:
            return self.set_child("right", new_child)
        return False

    def set_child(self, which_child, child):
        if which_child is not "left" and which_child is not "right":
            return False
        if which_child == "left":
            self.left_child = child
        else:
            self.right_child = child
        if child is not None:
            child.parent = self
        return True

class rb_tree(object): 
    def __init__(self):
        self.root = None

    def insert(self, key):
        new_node = rbt_node(key, None, True, None, None)
        self.insert_node(new_node)

    def insert_node(self, new_node):
        if self.root is None: 
            self.root = new_node
        else:
            temp = self.root
            while temp is not None:
                if new_node.key < temp.key:
                    if temp.left_child is None:
                        temp.set_child("left", new_node)
                        break
                    else:
                        temp = temp.left_child
                else:
                    if temp.right_child is None:
                        temp.set_child("right", new_node)
                        break
                    else:
                        temp = temp.right_child

        new_node.color = "red"  
        self.insertion_balance(new_node) 

    def insertion_balance(self, new_node):
        if new_node.parent is None: 
            new_node.color = "black"
            return

        if new_node.parent.is_black(): 
            return

        parent = new_node.parent 
        grandparent = new_node.get_grandparent()
        uncle = new_node.get_uncle()

        if uncle is not None and uncle.is_red(): 
            parent.color = uncle.color = "black"
            grandparent.color = "red"
            self.insertion_balance(grandparent)
            return

        if new_node is parent.right_child and parent is grandparent.left_child:
            self.left_rotate(parent)
            new_node = parent
            parent = new_node.parent

        elif new_node is parent.left_child and parent is grandparent.right_child:
            self.right_rotate(parent)
            new_node = parent
            parent = new_node.parent

        parent.color = "black"
        grandparent.color = "red"

        if new_node is parent.left_child:
            self.right_rotate(grandparent)
        else:
            self.left_rotate(grandparent)

    def right_rotate(self, selected_node): 
        left_right_child = selected_node.left_child.right_child
        if selected_node.parent is not None:
            selected_node.parent.replace_child(selected_node, selected_node.left_child)
        else:
            self.root = selected_node.left_child
            self.root.parent = None
        selected_node.left_child.set_child("right", selected_node)
        selected_node.set_child("left", left_right_child)

    def left_rotate(self, selected_node):  
        right_left_child = selected_node.right_child.left_child
        if selected_node.parent is not None:
            selected_node.parent.replace_child(selected_node, selected_node.right_child)
        else:
            self.root = selected_node.right_child
            self.root.parent = None
        selected_node.right_child.set_child("left", selected_node)
        selected_node.set_child("right", right_left_child)

    def search(self, key):
        temp = self.root
        while temp is not None:
            if temp.key == key:
                return True
            elif key < temp.key:
                temp = temp.left_child
            else:
                temp = temp.right_child
        return False

def print_anagrams(word, prefix=""):
    if len(word) <= 1:
        str = prefix + word
        if english_words.search(str):
            print(str)
    else:
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: i] # letters before cur
            after = word[i + 1:] # letters after cur

            if cur not in before: # check if permutations of cur have not been generated
                print_anagrams(before + after, prefix + cur)
# fill tree with words.txt
def populateTree(input):
    global english_words 
    # open file 
    with open("words.txt", "r") as file:
        #if selection is RBT
        if input == 'RBT':
            english_words = rb_tree()
            # insert word in lowercase; exclude last item
            for line in file:
                english_words.insert(line[:-1].lower())
        # if selection is AVL
        else:
            english_words = avl_tree()
            # insert word in lowercase; exclude last item
            for line in file:
                english_words.insert(line[:-1].lower())
# count anagrams almost same as print_anagrams; doesn't work properly
def count_anagrams(word, prefix=""):
    if len(word) <= 1:
        str = prefix + word 
        if english_words.search(str):
            return 1
        return 0
    else: 
        # set counter
        count = 0
        #print_anagrams
        for i in range(len(word)):
            cur = word[i: i + 1]
            before = word[0: 1]
            after = word[i + 1:]
            # increase count recursively 
            if cur not in before:
                count += count_anagrams(before + after, prefix + cur)
        return count
# find word with greatest amount of anagrams in test file
def greatest_num_anagrams(file):
    wordsFile = file
    # count and word holders
    greatest_count = 0
    greatest_anagrams = " "
    # for each line in file increase count using count_anagrams starting at zero and excluding last item
    for line in wordsFile:
        count = count_anagrams(line[0: -1])
        # find the word with the greatest count of anagrams
        if count > greatest_count:
            greatest_count = count
            greatest_anagrams = line[0: -1]
    return greatest_anagrams

user = input("Enter 'RBT' or 'AVL' to use either implementation:\n")
#if user != 'RBT' or user != 'AVL':
    #input("Enter 'RBT' or 'AVL' to use either implementation:\n")
populateTree(user)
test_1 = "spot"
test_2 = "y"
test_3 = "no"
print(count_anagrams(test_1))
print_anagrams(test_1)
print(count_anagrams(test_2))
print_anagrams(test_2)
print(count_anagrams(test_3))
print_anagrams(test_3)
print("")
#test file for greatest number of anagrams
print("Word with most anagrams in my test file:")
with open("Main.txt", "r") as file:
    print(greatest_num_anagrams(file))
