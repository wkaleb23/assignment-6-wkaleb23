
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
        self.MAX_BITS_PER_INT = max_bits_per_int

    ## Only returns the first num_bits_in_seq characters
    ## e.g. get_bits_as_string() returns "1111"
    def get_bits_as_string(self):
        """Returns a string that represents the bits stored in this BitSeq"""
        pass

    ## e.g. pack_bits("1111") will put the bits 1111 in the first available spot
    def pack_bits(self, new_bits_as_chars: str):
        """Given a string of 1s and 0s, packs relevant bits into this BitSeq"""
        ## For each bit/char in the input string:
        ##  determine if the we need a new int in self.bits to hold more bits
        ##  Add a new bit to the last int
        pass

    def get_bit(self, which_bit: int) -> int:
        ## 0-based indexing
        ## If which_bit >= num_bits_in_seq throw an IndexError
        pass

class FreqTable:
    def __init__(self, input_str: str = ""):
        self.char_count = [0] * 256
        self.populate(input_str)

    def clear(self):
        """Resets the frequency counts"""
        pass

    def populate(self, input_str):
        ## Updates the current frequency counts with the input string
        for c in input_str:
            self.char_count[ord(c)] += 1
        pass

    def get_char_count(self, char):
        """Returns the current frequency count for the given char"""
        pass

    def print_freq_table(self):
        ## Print the frequency table in a easy to view format
        pass



class HTree:
    def __init__(self, c=None, freq=0, p0=None, p1=None):
        self.char = c
        self.freq = freq
        self.p0 = p0
        self.p1 = p1

    def print_tree(self, level=0, path: str = ""):
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
    ## I used this as a helper; you can probably get away
    ##   without implementing it, but you'll have to update the
    ##   tests accordingly.
    def get_char_count(self, char):
        pass

    ## For a specified tree and character,
    ##  determine if the character is in the tree,
    ##  and if so, the path to get to it.
    ## Returns "" if the character is not in the tree
    ## I used this as a helper; you can probably get away
    ##   without implementing it, but you'll have to update the
    ##   tests accordingly.
    def get_char_path(self, target, path=""):
        pass

    ## Produces a serialized output of the tree, in the format:
    ## A0C1000D1001E1010F1011G1100H1101B111
    ## where it's [char][pathToChar][char][pathToChar]
    ## This is a LOW priority; this should be the last thing to implement
    def serialize(self, path: str = ""):
        pass

    ## Assumes all 1s and 0s are bits;
    ## A0C1000D1001E1010F1011G1100H1101B111
    ## Builds a tree based on the provided serialized tree string
    ## Doesn't populate it with frequencies, just the chars
    ## This isn't high priority, but can be helpful to easily
    ## create a new tree for testing
    def deserialize(self, tree_string):
        pass

    ## If the path exists, check if the char is the same and returns true/false
    ## If the path doesn't exist, creates the path and creates leaf node with the given char
    ## I used this as a helper for the deserialize process, but you may find
    ## it helpful.
    ## If you don't get around to implementing deserialize(), you probably don't need it.
    def create_path(self, char: str, path: str):
        pass



class LUT:
    def __init__(self):
        self.representation = [""] * 256

    def print_lookup_table(self):
        ## Print the table out in a nice to view manner
        pass

    ## Saves the path for a given char
    ## e.g. set_encoding('A', '10010')
    def set_encoding(self, char, path):
        self.representation[ord(char)] = path

    ## Returns the path for a given char
    ## e.g. get_encoding('A') returns '10010'
    def get_encoding(self, char):
        pass

    ## Given the root of a Huffman Tree, populate this lookup table.
    def populate_from_huffman_tree(self, htree_root: HTree):
        pass


    ## I found it helpful to have a function such as this to help
    ## traverse the HTree to populate the table.
    ## Feel free to ignore it if you'd like, or write something for yourself.
    def create_lookup_table_helper(self, node, path, which_step):
        pass


## We use this to bundle up an encoded message and the Huffman Tree used to encode it.
class SecretMessage:
    def __init__(self, encoded_message: BitSeq, huffman_tree: HTree):
        self.encoded_bit_sequence = encoded_message
        self.huffman_tree = huffman_tree

## The Encoder class is used to do encoding;
## It holds all the things we need to encode.
## This makes it helpful to inspect and test that
## all the pieces are working as expected.
class Encoder:
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
        pass

    ## This is the function that actually creates the HuffmanTree.
    ## Follow the process outlined in the README,
    ## in the "Creating the mapping: The Huffman Tree" section.
    def create_encoding_tree(self):
        pass


## This is like the Encoder, but Decoding.
##
class Decoder:
    def __init__(self, huffman_tree: HTree):
        self.huffman_tree = huffman_tree

    ## Do the decoding of the provided message, using the
    ## self.huffman_tree.
    def decode(self, secret_message: BitSeq):
        pass

    ## This is a helper function to make decoding easier.
    ## I kept it in as a starter, but if you don't find it helpful,
    ## feel free to ignore it and take your own approach.
    ##
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
    def decode_helper(self, bit_seq: BitSeq, cur_node, out: [], which_bit: int, path:[]):
        pass


## Helper function that shows bit manipulation in Python
## Given a value (such as 2593) and the number of bits to
##   display, print the first number of bits of the  binary representation
##   of the number
## Note: you can print a number in binary in Python with the following
##  string formatting: print(format(57344, '016b'))
def display_bits(value, num_bits):
    display_mask = 1 << 15 ## 1000 0000 0000 0000
    for c in range(num_bits):
        print('1' if (value & display_mask) else '0', end='')
        value <<= 1  ## Shift the bits in 'value' to the left by 1
        if c % 8 == 7:  ## Print out a space to make it easier on the eyes after 8 bits
            print(' ', end='')
    print() ## Print a newline