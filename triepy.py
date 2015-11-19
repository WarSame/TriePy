# Trie work
# Graeme Cliffe


class Node:
    # Node - element in the trie
    # May have children nodes. May be a leaf.
    # Must be on the path to some leaf
    def __init__(self):
        self.children = {}
        self.leaf = False

    def set_child(self, char, child_node):
        self.children[char] = child_node

    def get_child(self, char):
        if char in self.children:
            return self.children[char]

    def __str__(self):
        node_string = ""
        if not self.children.keys():
            return node_string
        node_string += "\nConnected to:"
        for char in self.children.keys():
            node_string += char + "\t"
        return node_string


class Trie:
    def __init__(self, words):
        # Given a list of words insert all words into trie
        self.start_node = Node()
        for word in words:
            self.insert_word(word)

    def get_trie(self):
        # Return a list containing the entire trie
        curr_node = self.start_node
        return self.get_children_strings(curr_node)

    def get_children(self, stub):
        # Return a list containing all the words in the trie branching from the stub
        curr_node = self.start_node
        for char in stub:
            child = curr_node.get_child(char)
            if child:
                # If our node has a child, move to it and continue
                curr_node = child
            else:
                # If not, the stub is not in the trie
                return ""
        # We now have our stub node and can find all
        # Its descendants, and return those
        leaves = self.get_children_strings(curr_node)
        for i in range(0, len(leaves)):
            leaves[i] = stub + leaves[i]
        return leaves

    def get_children_strings(self, curr_node):
        # Given a node, return all strings branching from that node in a list
        leaves = []
        for child in curr_node.children.keys():
            child_node = curr_node.get_child(child)
            # Add children leaves to our leaves collection
            child_leaves = self.get_children_strings(child_node)
            # Append the current letter in front of all child leaves
            for i in range(0, len(child_leaves)):
                child_leaves[i] = child + child_leaves[i]
            # Add our children leaves to the entire set of leaves
            leaves += child_leaves

            if child_node.leaf:
                # If we get a leaf, start a new
                leaves.append(child)
        # Return leaves up
        return leaves

    def insert_word(self, word):
        # Given a word, insert it into the trie
        curr_node = self.start_node
        for char in word:
            # Loop through entire word
            child = curr_node.get_child(char)
            if child:
                # If you find a child, move to it
                curr_node = child
            else:
                # If not, make one
                new_node = Node()
                curr_node.set_child(char, new_node)
                # And move to that new one
                curr_node = new_node
        # Make the last character in the word a leaf
        curr_node.leaf = True

    def is_leaf(self, word):
        # Given a word, find if it is a leaf(full word)
        curr_node = self.start_node
        for char in word:
            child = curr_node.get_child(char)
            if child:
                # If the next letter is in the trie, move on to it
                curr_node = child
            else:
                # Otherwise the word is not in the trie
                return False
        # Return whether the end node is a leaf or not
        return curr_node.leaf

    def is_in_trie(self, word):
        # Given a char string, find if it is in the trie - word or word prefix
        curr_node = self.start_node
        for char in word:
            child = curr_node.get_child(char)
            if child:
                # If child in trie, search from it
                curr_node = child
            else:
                return False
        return True

    def remove_word(self, word):
        # Return true if able to remove word
        if not self.is_in_trie(word):
            return False
        return self.remove_word_recursive(word, self.start_node, 0)

    def remove_word_recursive(self, word, parent_node, depth):
        # If we hit the bottom letter delete the bottom node and return up
        if len(word) == depth:
            # No matter what, remove the word as a leaf
            parent_node.leaf = False
            # If there are no children for our node, then delete it
            if not parent_node.get_child(word[depth-1]):
                del parent_node
            return True
        # If we are at a non bottom node, keep going
        self.remove_word_recursive(word, parent_node.get_child(word[depth]), depth + 1)
        # Then delete the child node if it has only one child and is not a leaf
        if len(parent_node.children) == 0 and not parent_node.leaf:
            del parent_node
        return True


def build_trie_from_enable():
    f = open("../enable1.txt", "r")
    words = []
    for line in f.readlines():
        words.append(line.strip("\n"))
    return Trie(words)


def main():
    tr = build_trie_from_enable()
    print tr.remove_word("zygote")
    result = tr.get_trie()
    for i in result:
        print i


main()
