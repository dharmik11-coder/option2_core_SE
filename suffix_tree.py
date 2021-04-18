from string import punctuation

# Class for Suffix Node
class Node:

    def __init__(self, index=-1, parent_node=None, depth=-1):

        self.index = index
        self.depth = depth
        self.parent = parent_node
        self.general_indexes = {}
        self.link = None
        self.transition_links = []

    def add_link(self, node):

        self.link = node

    def get_link(self):

        if self.link is not None:
            return self.link
        return False

    def leaf_check(self):

        return self.transition_links == []

    def add_transition(self, node, suffix):

        transition = self.get_transition(suffix)
        if transition:
            self.transition_links.remove((transition, suffix))
        self.transition_links.append((node, suffix))

    def get_transition(self, suffix):
        """Returns the transition node"""

        for node, suffix2 in self.transition_links:
            if suffix == suffix2:
                return node
        return False

    def transition_check(self, suffix):

        for node, suffix2 in self.transition_links:
            if suffix == suffix2:
                return True
        return False

    def traverse(self, func):
        """Takes a function as an argument and applies that to all the transition links of the tree"""

        for (node, _) in self.transition_links:
            node.traverse(func)
        func(self)

    def get_leaves(self):
        """Returns all the leaf nodes"""

        if self.leaf_check():
            return [self]
        return [leaf for (node, _) in self.transition_links for leaf in node.get_leaves()]

# Class for Suffix Tree
class SuffixTree:

    def __init__(self, ip):
        self.root_node = Node()
        self.root_node.depth = 0
        self.root_node.index = 0
        self.root_node.parent = self.root_node
        self.root_node.add_link(self.root_node)
        self.endpoint_index = []
        self.concat_files(ip)

    def new_node(self, input, current_node, depth):
        """Creates a new non-leaf node """

        index = current_node.index
        parent = current_node.parent
        result = Node(index=index, depth=depth)
        result.add_transition(current_node, input[index + depth])
        current_node.parent = result
        parent.add_transition(result, input[index + parent.depth])
        result.parent = parent
        return result

    def new_leaf(self, num, index, current_node, depth):
        """Creates a new leaf node """

        result = Node()
        result.index = index
        result.depth = len(num) - index
        current_node.add_transition(result, num[index + depth])
        result.parent = current_node
        return result

    def first_index(self, index):
        """Returns node's starting index as the index of the string"""
        idx = 0
        for index2 in self.endpoint_index[1:]:
            if index < index2:
                return idx
            idx += 1
        return idx

    def concat_files(self, ip_list):
        """This function will insert an endpoint character to the end of each string to identify strings coming from different file"""

        ep_val = 0
        req_string = ""
        for string in ip_list:
            self.endpoint_index.append(len(req_string))
            req_string += string
            req_string += punctuation[ep_val]
            ep_val += 1

        self.final_string = req_string
        self.build_tree(req_string)
        self.root_node.traverse(self.label_nodes)

    def build_tree(self, text):
        """McCreight's Algorithm to build suffix tree in O(n+m) linear time; n,m = length of 2 strings"""

        current_node = self.root_node
        current_depth = 0
        for i in range(len(text)):
            while current_node.depth == current_depth and current_node.transition_check(text[current_depth + i]):
                current_node = current_node.get_transition(text[current_depth + i])
                current_depth += 1
                while current_depth < current_node.depth and text[current_node.index + current_depth] == text[
                    i + current_depth]:
                    current_depth += 1
            if current_depth < current_node.depth:
                current_node = self.new_node(text, current_node, current_depth)
            self.new_leaf(text, i, current_node, current_depth)
            if not current_node.get_link():
                self.new_slink(text, current_node)
            current_node = current_node.get_link()
            current_depth -= 1
            if current_depth < 0:
                current_depth = 0

    def label_nodes(self, ip_node):
        """Labels the nodes of trees with index of strings found in their child nodes"""

        if ip_node.leaf_check():
            label = {self.first_index(ip_node.index)}
        else:
            label = {node for nodes in ip_node.transition_links for node in nodes[0].general_indexes}
        ip_node.general_indexes = label

    def new_slink(self, input, current_node):
        """Creates a new slink """

        depth = current_node.depth
        result = current_node.parent.get_link()
        while result.depth < depth - 1:
            result = result.get_transition(input[current_node.index + result.depth + 1])
        if result.depth > depth - 1:
            result = self.new_node(input, result, depth - 1)
        current_node.add_link(result)

    def identical_strand(self):
        """Returns the identical longest strand, list of indexes, list of offsets of bytes for identical string in files """
        end_node = self.deepest_com_node(self.root_node)
        begin = end_node.index
        end = end_node.index + end_node.depth
        fin_str = self.final_string[begin:end]
        node_idx = end_node.general_indexes
        offset = [n.index for n in end_node.get_leaves()]

        return fin_str, node_idx, offset

    def deepest_com_node(self, node):
        """Returns the deepest node for the longest common strand of bytes in files."""

        res = [self.deepest_com_node(node) for (node, _) in node.transition_links if len(node.general_indexes) > 1]
        if not res:
            return node
        end_node = max(res, key=lambda x: x.depth)
        return end_node

