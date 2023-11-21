# This is the code I need to implement


class BitSeq:
    """A BitSeq is a sequence of bits
    Represented by a list of numbers that hold the packed bits,
    and a bunch of helper methods to help us build up a bit
    sequence and print/manipulate/observe the sequence of bits.
    """

    MAX_BITS_PER_INT = 16

    def __init__(self, max_bits_per_int=16):
        self.bits = []  # List of ints-- keep them 16-bit unsigned
        self.num_bits_in_seq = 0
        self.last_bit = None  # I added this to help
        self.MAX_BITS_PER_INT = max_bits_per_int

    def get_bit(self, which_bit: int) -> int:
        """Helper function for getting a bit at a specific index"""
        ## 0-based indexing
        ## If which_bit >= num_bits_in_seq throw an IndexError
        #  raise IndexError as specified
        if which_bit >= self.num_bits_in_seq:
            raise IndexError
        else:
            int_index = which_bit // self.MAX_BITS_PER_INT  # what int from bits[] is the bit in
            bit_index = which_bit % self.MAX_BITS_PER_INT  # get the index of the bit in the int
            # return the bit at the given index, get bit and position
            bit = self.bits[int_index]
            position = self.MAX_BITS_PER_INT - bit_index - 1
            # shift the bit to the right by the position and extract the bit
            return (bit >> position) & 1

    def get_bits_as_string(self):
        """Returns a string that represents the bits stored in this BitSeq"""
        bits_as_string = ""
        # loop though all the bits
        for i in range(self.num_bits_in_seq):
            # check if we need to add a space because we are at the end of an int
            if i % self.MAX_BITS_PER_INT == 0 and i != 0:
                bits_as_string += " "
            bit = self.get_bit(i)  # use the helper function
            bits_as_string += str(bit)  # add the bit to the string
        return bits_as_string

    ## e.g. pack_bits("1111") will put the bits 1111 in the first available spot
    def pack_bits(self, new_bits_as_chars: str):
        """Given a string of 1s and 0s, packs relevant bits into this BitSeq"""
        # for each char in new_bits_as_chars, add it to the end of the bit sequence from self.last_bit
        # check if we need to add a new int to self.bits
        # if so, add it
        # add the bit to the last int in self.bits

        # loop through each character
        for c in new_bits_as_chars:
            if c == "0" or c == "1":
                # check if we need to add a new int to self.bits
                if (self.last_bit is None) or (
                        self.num_bits_in_seq % self.MAX_BITS_PER_INT == 0 and self.num_bits_in_seq != 0):
                    self.bits.append(0)  # add a new int to self.bits
                    self.last_bit = 0  # reset the last bit helper variable
                    self.last_bit += int(c)  # add the new bit to the last bit
                else:
                    # here I need to account for the added zeros I added to complete the last int
                    self.last_bit = self.last_bit << 1  # shift the last bit left by 1
                    self.last_bit += int(c)  # add the new bit to the last bit

                self.num_bits_in_seq += 1  # reflect that I added a bit to the sequence

                # Now I want to add the new last bit to the last int in self.bits
                # But I want to make sure it is a 16-bit int, so I have to "fill in" the rest of the int with zeros
                # I however want to keep the last bit as is so that I can add more bits to it later in the right position
                # check if it's full. If it's not, fill it
                if self.num_bits_in_seq % self.MAX_BITS_PER_INT != 0:
                    # find the number of zeros to add by finding the number of "mising" bits in the int:
                    # comparing the number of bits in the sequence to the number of bits in the last int
                    # then subtracting from the max number of bits per int
                    num_zeros_to_add = self.MAX_BITS_PER_INT - (self.num_bits_in_seq % self.MAX_BITS_PER_INT)
                    self.bits[-1] = self.last_bit << num_zeros_to_add
                else:
                    self.bits[-1] = self.last_bit


class FreqTable:
    """A table of frequencies as shown in the README"""
    def __init__(self, input_str: str = ""):
        self.char_count = [0] * 256  # ASCII values
        self.populate(input_str)  # populate the table with the given string

    def clear(self):
        """Resets the frequency counts"""
        self.char_count = [0] * 256  # reset all to 0

    def populate(self, input_str):
        """ Updates the current frequency counts with the input string """
        # fir each character, add frequeency at the index of the character in the char_count list
        for c in input_str:
            self.char_count[ord(c)] += 1

    def get_char_count(self, char):
        """Returns the current frequency count for the given char"""
        return self.char_count[ord(char)]

    def print_freq_table(self):
        """ Print the frequency table in a easy to view format """
        for i in range(256):
            # only print the characters that have a frequency count so that it is more readable
            if self.char_count[i] != 0:
                char_name = chr(i)
                char_count = self.char_count[i]
                print(char_name + ": " + str(char_count))


class HTree:
    """ A node in a Huffman Tree and the tree itself """
    def __init__(self, c=None, freq=0, p0=None, p1=None):
        self.char = c
        self.freq = freq
        self.p0 = p0
        self.p1 = p1

    def print_tree(self, level=0, path: str = ""):
        """ Print the tree in a nice to view format """
        # this function was given
        for i in range(level):
            print("--", end='')
        print(f"Char: {self.char}, count: {self.freq}. Path: {path}")
        if self.p0:
            self.p0.print_tree(level + 1, path + "0")
        if self.p1:
            self.p1.print_tree(level + 1, path + "1")


    ## For a specified tree and character,
    ##  determine if the character is in the tree,
    ##  and if so, the frequency count to get to it.
    ## Returns -1 if the character is not in the tree
    def get_char_count(self, char):
        """ Returns the frequency count for the given character"""
        # if it is a leaf node, check if the character is the same and return the frequency count
        if self.char == char:
            return self.freq

        # if it is not, we have to loop throuhg the tree to find the character
        # determine if the character is in the tree by looping through root.p0 and root.p1
        # if the character is in the tree, return the frequency count it has (each node is itself a tree)
        # if the character is not in the tree, return -1

        # check self.p0 first
        if self.p0 != None:
            char_count = self.p0.get_char_count(char)  # recurse through the tree with this function
            if char_count != -1:  # this function returns -1  if the character is not in the tree
                return char_count

        # check self.p1 second
        if self.p1 != None:
            char_count = self.p1.get_char_count(char)  # recurse through the tree with this function
            if char_count != -1:
                return char_count

        # if the character is not in the tree, return -1
        return -1


    ## For a specified tree and character,
    ##  determine if the character is in the tree,
    ##  and if so, the path to get to it.
    ## Returns "" if the character is not in the tree
    def get_char_path(self, target, path=""):
        """ Returns the path to the given character """
        # if it is a leaf node, check if the character is the same and return the path
        if self.char == target:
            return path
        # if it's not a leaf node and it has no children, then the character is not in the tree since this is called recursively
        elif self.p0 == None and self.p1 == None:
            return ""
        else:
            # if it is not, we have to loop throuhg the tree to find the character
            # so we loop through root.p0 and root.p1
            return self.p0.get_char_path(target, path + "0") + self.p1.get_char_path(target, path + "1")


    ## Produces a serialized output of the tree, in the format:
    ## A0C1000D1001E1010F1011G1100H1101B111
    ## where it's [char][pathToChar][char][pathToChar]
    def serialize(self, path=""):
        """ Returns a serialized version of the tree """
        # if it is a leaf node, return the character and the path
        if self.char is not None:
            return self.char + path
        # if it is not, we have to loop throuhg the tree to find the character
        else:
            return self.p0.serialize(path + "0") + self.p1.serialize(path + "1")

    ## Assumes all 1s and 0s are bits;
    ## A0C1000D1001E1010F1011G1100H1101B111
    ## Builds a tree based on the provided serialized tree string
    ## Doesn't populate it with frequencies, just the chars
    def deserialize(self, s):
        """ Builds a tree based on the provided serialized tree string """
        # first make sure the string is not empty
        if len(s) == 0:
            return ""

        # start by getting the first character and the path
        char = s[0]
        # remove the character from the string
        s = s[1:]
        # build the path
        path = ""
        # loop through the string until we get to a character (it will not be a 0 or a 1)
        while len(s) > 0 and s[0] in "01":
            path += s[0]  # add to path
            s = s[1:]  # remove from string
        # once we have the character and the path, we can create a tree from the first character
        node = self
        # loop through the path and create the tree
        for bit in path:
            # left is when the bit is 0
            if bit == '0':
                # check that we haven't reached the end of the path
                if node.p0 is None:
                    node.p0 = HTree()
                # move to the next node
                node = node.p0
            else:
                # right is when the bit is 1
                if node.p1 is None:
                    node.p1 = HTree()
                # move to the next node
                node = node.p1

        # once we have looped through the whole path,  we can add the character
        node.char = char
        return self.deserialize(s)  # call recursively to build the rest of the tree


    ## If the path exists, check if the char is the same and returns true/false
    ## If the path doesn't exist, creates the path and creates leaf node with the given char
    ## NOTE: I implemented this, but I ended up not using it
    def create_path(self, char: str, path: str):
        """ Creates a path to the given character """
        # check that the path is not empty, if it is, it means we have reached the end of the path, and we can add the character
        if len(path) == 0:
            self.char = char
            return True

        # if the path is not empty, we have to keep looping thorugh the tree
        else:
            if path[0] == "0":
                if self.p0 == None:
                    self.p0 = HTree()
                return self.p0.create_path(char, path[1:])
            else:
                if self.p1 == None:
                    self.p1 = HTree()
                return self.p1.create_path(char, path[1:])


class LUT:
    """ A lookup table for characters and their paths """
    def __init__(self):
        self.representation = [""] * 256


    def print_lookup_table(self):
        """ Print the table out in a nice to view manner """
        # very similar to the freq table
        for i in range(256):
            if self.representation[i] != "":
                char_name = chr(i)
                char_path = self.representation[i]
                print(char_name + ": " + char_path)


    ## Saves the path for a given char
    ## e.g. set_encoding('A', '10010')
    def set_encoding(self, char, path):
        """ Saves the path for a given character"""
        # This function was given
        self.representation[ord(char)] = path


    ## Returns the path for a given char
    ## e.g. get_encoding('A') returns '10010'
    def get_encoding(self, char):
        """ Returns the path for a given character"""
        # I can just return the path at the index of the character in the representation list
        return self.representation[ord(char)]

    ## Given the root of a Huffman Tree, populate this lookup table.
    def populate_from_huffman_tree(self, htree_root: HTree):
        """ Given the root of a Huffman Tree, populate this lookup table. """
        # if it is a leaf node, add the character and the path to the lookup table
        if htree_root.p0 == None and htree_root.p1 == None:
            self.set_encoding(htree_root.char, "")
        else:
            # populate this lookup table with the paths to each character
            self.populate_from_huffman_tree_helper(htree_root, "")


    ## Helper function for populate_from_huffman_tree
    def populate_from_huffman_tree_helper(self, node, path):
        """ Helper function for populate_from_huffman_tree that populates the lookup table with the paths to each character"""
        # if it is a leaf node, add the character and the path to the lookup table
        if node.p0 == None and node.p1 == None:
            self.set_encoding(node.char, path)
        # if it is not, we have to loop throuhg the tree to find the character
        else:
            self.populate_from_huffman_tree_helper(node.p0,
                                                   path + "0")  # call recursively with the next bit in the path, add a 0 since it is the left side of the tree
            self.populate_from_huffman_tree_helper(node.p1,
                                                   path + "1")  # call recursively with the next bit in the path, add a 1 since it is the right side of the tree



## We use this to bundle up an encoded message and the Huffman Tree used to encode it.
class SecretMessage:
    """ A bundle of an encoded message and the Huffman Tree used to encode it """
    def __init__(self, encoded_message: BitSeq, huffman_tree: HTree):
        self.encoded_bit_sequence = encoded_message
        self.huffman_tree = huffman_tree


## The Encoder class is used to do encoding;
## It holds all the things we need to encode.
## This makes it helpful to inspect and test that
## all the pieces are working as expected.
class Encoder:
    """ The Encoder class is used to do encoding;"""
    def __init__(self):
        self.freq_table = None
        self.lookup_table = None
        self.huffman_tree = None
        self.encoded_bit_sequence = None


    ## Given a message,do all the steps to encode the message.
    ## When this is complete, the Encoder should have the
    ##  freq_table, lookup_table, huffman_tree, and encoded_bit_sequence
    ##  attributes should all be populated. (this allows us to test all the things)
    ## The huffman_tree and encoded_bit_sequence should be returned in a
    ##  SecretMessage object, so it can be "sent to a someone else".
    def encode(self, message_to_encode) -> SecretMessage:
        """ Given a message, do all the steps to encode the message. Steps are given in the README """
        # fist, given the message, create a frequency table
        self.freq_table = FreqTable(message_to_encode)
        # then, create a lookup table from the frequency table
        self.lookup_table = LUT()
        self.lookup_table.populate_from_huffman_tree(self.create_encoding_tree())
        # then, create a huffman tree from the frequency table
        # then, create an encoded bit sequence from the message and the lookup table
        self.encoded_bit_sequence = self.create_encoded_bit_sequence(message_to_encode)
        # then, return a SecretMessage object with the huffman tree and encoded bit sequence
        return SecretMessage(self.encoded_bit_sequence, self.huffman_tree)


    def create_encoded_bit_sequence(self, message_to_encode):
        """ helper function for encode that creates an encoded bit sequence from the message and the lookup table"""
        # create an empty bit sequence
        encoded_bit_sequence = BitSeq()
        # loop though each character in the message
        for c in message_to_encode:
            # pack the current character's path into the bit sequence
            curr_encoding = self.lookup_table.get_encoding(c)  # use the lookup table functions
            encoded_bit_sequence.pack_bits(curr_encoding)  # use the bit sequence functions
        return encoded_bit_sequence

    ## This is the function that actually creates the HuffmanTree.
    ## Follow the process outlined in the README,
    ## in the "Creating the mapping: The Huffman Tree" section.
    def create_encoding_tree(self):
        # implement this
        # follow the process outlined in the README in this folder
        # here is the information from the README:
        # The tree is created thusly:
        #     Create a node for each character (including the count), and put it in an appropriate data structure
        #     While there is more than 1 node in the list:
        #     Select two nodes with the lowest counts
        #     Create a new node that is the parent node of those two nodes
        #     Set the count of that new node to be the sum of the counts of the two children nodes
        #     Take the two children nodes out of the list
        #     Put the new parent node in the list
        #     The last node in the list is the root of the tree.
        # create_encoding_tree should build the tree with the given frequencies.

        # create a node for each character (including the count), and put it in an appropriate data structure
        nodes = []
        # loop through each character in the frequency table
        for i in range(256):
            if self.freq_table.char_count[i] != 0:  # check that the character exists in the problem space
                nodes.append(HTree(chr(i), self.freq_table.char_count[
                    i]))  # add the character and the frequency to the list of nodes
        # while there is more than 1 node in the list:
        while len(nodes) > 1:
            # select two nodes with the lowest counts
            nodes.sort(key=lambda x: x.freq)  # sort the nodes by frequency
            lowest_node_1 = nodes[0]
            lowest_node_2 = nodes[1]
            # create a new node that is the parent node of those two nodes
            # set the count of that new node to be the sum of the counts of the two children nodes
            parent_node = HTree(None, lowest_node_1.freq + lowest_node_2.freq, lowest_node_1, lowest_node_2)
            # take the two children nodes out of the list
            nodes.remove(lowest_node_1)
            nodes.remove(lowest_node_2)
            # put the new parent node in the list
            nodes.append(parent_node)
        # the last node in the list is the root of the tree
        self.huffman_tree = nodes[0]
        return self.huffman_tree


## This is like the Encoder, but Decoding.
class Decoder:
    def __init__(self, huffman_tree: HTree):
        self.huffman_tree = huffman_tree


    ## Do the decoding of the provided message, using the
    ## self.huffman_tree.
    def decode(self, secret_message: BitSeq):
        """ Do the decoding of the provided message, using the self.huffman_tree."""
        decoded_string = ""
        node = self.huffman_tree  # start at the root of the tree
        # loop through each bit in the bit sequence
        for i in range(secret_message.num_bits_in_seq):
            bit = secret_message.get_bit(i)  # get the bit corresponding to the index
            if bit == 0:
                node = node.p0  # if the bit is 0, traverse the left side of the tree
            else:
                node = node.p1  # if the bit is 1, traverse the right side of the tree
            # if the node is a leaf node, add the character to the output string
            if node.char is not None:
                decoded_string += node.char
                node = self.huffman_tree
        return decoded_string

    ## Inputs:
    ## bit_seq: the BitSeq we're decoding
    ## cur_node: the current node in the HTree we're on
    ## out: a list of characters that have been emitted so far
    ## which_bit: which bit in the bit_seq we're at in our traversal
    ## path: the path that has gotten us to this point so far
    ##
    ## It's intended to be called recursively.
    ##
    ## Example first call:
    ## decode_helper(message, self.huffman_tree, [], 0, [])
    def decode_helper(self, bit_seq: BitSeq, cur_node, out: [], which_bit: int, path: []):
        """ Helper function for decode that traverses the tree and adds the characters to the output list"""
        ## I implemented this, but I ended up not using it
        # this is a recursive function that will traverse the tree
        # for each bit in the bit sequence, traverse the tree
        # if the bit is 0, traverse the left side of the tree
        # if the bit is 1, traverse the right side of the tree
        # if the node is a leaf node, add the character to the output list
        # if the node is not a leaf node, keep traversing the tree
        # to continue traversing the tree, call decode_helper with the next bit in the bit sequence
        # the next bit in the bit sequence is the next bit in the bit sequence
        # which_bit is the index of bit_seq we are currently at
        # if the node is a leaf node, add the character to the output list

        if cur_node.p0 == None and cur_node.p1 == None:
            out.append(cur_node.char)
            # reset the current node to the root of the tree
            cur_node = self.huffman_tree
        # if the node is not a leaf node, keep traversing the tree
        else:
            # if the bit is 0, traverse the left side of the tree
            if bit_seq.get_bit(which_bit) == 0:
                self.decode_helper(bit_seq, cur_node.p0, out, which_bit + 1, path + ["0"])  # remmeber path is a list
            # if the bit is 1, traverse the right side of the tree
            elif bit_seq.get_bit(which_bit) == 1:
                self.decode_helper(bit_seq, cur_node.p1, out, which_bit + 1, path + ["1"])
        return "".join(out)


## Helper function that shows bit manipulation in Python
## Given a value (such as 2593) and the number of bits to
##   display, print the first number of bits of the  binary representation
##   of the number
## Note: you can print a number in binary in Python with the following
##  string formatting: print(format(57344, '016b'))
def display_bits(value, num_bits):
    """ Helper function that shows bit manipulation in Python. This was given """
    display_mask = 1 << 15  ## 1000 0000 0000 0000
    for c in range(num_bits):
        print('1' if (value & display_mask) else '0', end='')
        value <<= 1  ## Shift the bits in 'value' to the left by 1
        if c % 8 == 7:  ## Print out a space to make it easier on the eyes after 8 bits
            print(' ', end='')
    print()  ## Print a newline