import pytest
from a6 import *

class TestBitSeq:

    def test_bitpacking_16bits(self):
        out = BitSeq()
        out.pack_bits("1111")
        ## First int should be 0b1111000000000000, which is 61440
        assert out.bits[0] == 61440
        assert out.bits[0] == 0b1111000000000000
        assert out.get_bits_as_string() == "1111"

        out.pack_bits("110")
        assert out.bits[0] == 64512
        assert out.bits[0] == 0b1111110000000000
        assert out.get_bits_as_string() == "1111110"

        out.pack_bits("001")
        assert out.bits[0] == 64576
        assert out.bits[0] == 0b1111110001000000
        assert out.get_bits_as_string() == "1111110001"

        out.pack_bits("101")
        assert out.bits[0] == 64616
        assert out.bits[0] == 0b1111110001101000
        assert out.get_bits_as_string() == "1111110001101"

        out.pack_bits("1110")
        assert out.bits[0] == 64623
        assert out.get_bits_as_string() == "1111110001101111 0"

        out.pack_bits("000")
        out.pack_bits("110")
        out.pack_bits("100")
        out.pack_bits("011")
        assert out.bits[0] == 64623
        assert out.bits[1] == 3352
        assert out.get_bits_as_string() == "1111110001101111 0000110100011"

    def test_two(self):
        out = BitSeq()
        out.pack_bits("1000011101001000")
        assert out.bits[0] == 0b1000011101001000

        out.pack_bits("1100100111011001")
        assert out.bits[1] == 0b1100100111011001

        out.pack_bits("1100100100011111")
        assert out.bits[2] == 0b1100100100011111

        out.pack_bits("0010011111011111")
        assert out.bits[3] == 0b0010011111011111

        out.pack_bits("1000100011111101")
        assert out.bits[4] == 0b1000100011111101

        out.pack_bits("0011100100101111")
        assert out.bits[5] == 0b0011100100101111

        out.pack_bits("1011101000111111")
        assert out.bits[6] == 0b1011101000111111

    def test_three(self):
        out = BitSeq()
        out.pack_bits("100001110")  # 9 bits
        out.pack_bits("1001000110010011101")  # 19 bits
        out.pack_bits("1001110010010")  # 13 bits
        out.pack_bits("0011111")  # 7 bits

        assert out.bits[0] == 34632

        assert out.bits[0] == 0b1000011101001000
        assert out.bits[1] == 0b1100100111011001
        assert out.bits[2] == 0b1100100100011111

    def test_get_bit_16bits(self):
        out = BitSeq()
        out.pack_bits("100001110")

        assert out.get_bit(0) == 1
        assert out.get_bit(1) == 0
        assert out.get_bit(2) == 0
        assert out.get_bit(3) == 0
        assert out.get_bit(4) == 0
        assert out.get_bit(5) == 1

    def test_get_bit_8bits(self):
        out = BitSeq(8)
        out.pack_bits("1000 0111 0100")
        assert out.get_bits_as_string() == "10000111 0100"

        assert out.get_bit(0) == 1
        assert out.get_bit(1) == 0
        assert out.get_bit(2) == 0
        assert out.get_bit(3) == 0

        assert out.get_bit(4) == 0
        assert out.get_bit(5) == 1
        assert out.get_bit(6) == 1
        assert out.get_bit(7) == 1

        assert out.get_bit(8) == 0
        assert out.get_bit(9) == 1
        assert out.get_bit(10) == 0
        assert out.get_bit(11) == 0

        with pytest.raises(IndexError):
            assert out.get_bit(12) == 1

    def test_pack_bits_all_ones_only4(self):
        bits = BitSeq(8)
        bits.pack_bits("1111")
        assert bits.num_bits_in_seq == 4
        assert len(bits.bits) == 1
        assert bits.bits[0] == 0b11110000  # 240

    def test_pack_bits_all_ones(self):
        bits = BitSeq(8)
        bits.pack_bits("1111 1111")
        assert bits.num_bits_in_seq == 8
        assert len(bits.bits) == 1
        assert bits.bits[0] == 0b11111111  # 255

    def test_pack_bits_8bits_with_zeroes(self):
        bits = BitSeq(8)
        bits.pack_bits("1000 0110")
        assert bits.num_bits_in_seq == 8
        assert bits.bits[0] == 0b10000110

        bits.pack_bits("0010 10")
        assert bits.num_bits_in_seq == 14
        assert bits.bits[0] == 0b10000110
        assert bits.bits[1] == 0b00101000

    def test_eight_bit_seqs(self):
        out = BitSeq(8)
        out.pack_bits("1111")
        ## First int should be 0b11110000, which is 240 in 8 bit
        assert out.bits[0] == 240
        assert out.bits[0] == 0b11110000
        assert out.get_bits_as_string() == "1111"
        assert len(out.bits) == 1
        assert out.num_bits_in_seq == 4

        out.pack_bits("110")
        ## First int should be 0b11111100, which is 252 in 8 bit
        assert out.bits[0] == 0b11111100
        assert out.bits[0] == 252
        assert out.num_bits_in_seq == 7
        assert out.get_bits_as_string() == "1111110"

        out.pack_bits("001")
        ## First int should be 0b1111 1100, which is 252 in 8 bit
        ## Second int should be 0b01000000, which is 64 in 8 bit
        assert len(out.bits) == 2
        assert out.bits[0] == 252
        assert out.bits[1] == 64
        assert out.bits[0] == 0b11111100
        assert out.bits[1] == 0b01000000
        assert out.get_bits_as_string() == "11111100 01"

        out.pack_bits("101")
        assert out.get_bits_as_string() == "11111100 01101"
        assert len(out.bits) == 2
        assert out.bits[0] == 0b11111100
        assert out.bits[1] == 0b01101000  # 104

        out.pack_bits("1110")
        assert out.num_bits_in_seq == 17
        assert len(out.bits) == 3
        assert out.get_bits_as_string() == "11111100 01101111 0"

        assert out.bits[0] == 0b11111100
        assert out.bits[1] == 0b01101111  # 111
        assert out.bits[2] == 0b00000000

        out.pack_bits("000")
        out.pack_bits("110")
        out.pack_bits("100")
        out.pack_bits("011")
        assert out.num_bits_in_seq == 29
        assert len(out.bits) == 4
        assert out.get_bits_as_string() == "11111100 01101111 00001101 00011"
        assert out.bits[0] == 0b11111100
        assert out.bits[1] == 0b01101111  # 111
        assert out.bits[2] == 0b00001101
        assert out.bits[3] == 0b00011000

    def test_get_bits(self):
        bitstring = '1110100001001010 10010110111111000110001101'
        bit_seq = BitSeq()
        bit_seq.pack_bits(bitstring)
        assert bit_seq.num_bits_in_seq == 42
        assert bit_seq.get_bit(0) == 1
        assert bit_seq.get_bit(41) == 1

        with pytest.raises(IndexError):
            assert bit_seq.get_bit(42) == 1


class TestFreqTable:

    def test_freq_table_empty(self):
        freq_table = FreqTable()
        assert freq_table.get_char_count('a') == 0
        assert freq_table.get_char_count('A') == 0

    def test_freq_table_start_populated(self):
        freq_table = FreqTable("AaBbCcAaAa")
        assert freq_table.get_char_count('a') == 3
        assert freq_table.get_char_count('A') == 3
        assert freq_table.get_char_count('B') == 1
        assert freq_table.get_char_count('b') == 1
        assert freq_table.get_char_count('C') == 1
        assert freq_table.get_char_count('c') == 1
        assert freq_table.get_char_count('q') == 0
        assert freq_table.get_char_count('X') == 0

    def test_freq_table_start_populated_clear(self):
        freq_table = FreqTable("AaBbCcAaAa")
        ## Not checking that it's populated because I did this in another test
        freq_table.clear()
        assert freq_table.get_char_count('a') == 0
        assert freq_table.get_char_count('A') == 0
        assert freq_table.get_char_count('B') == 0
        assert freq_table.get_char_count('b') == 0
        assert freq_table.get_char_count('C') == 0
        assert freq_table.get_char_count('c') == 0

    def test_printing(self):
        freq_table = FreqTable("AaBbCcAaAa")
        freq_table.print_freq_table()
        print("Please inspect the output")

    def test_freq_table(self):
        test_string = "A DEAD DAD CEDED A BAD BABE A BEADED ABACA BED"
        freq_table = FreqTable(test_string)
        freq_table.print_freq_table()
        assert freq_table.char_count[ord('A')] == 11
        assert freq_table.char_count[ord('B')] == 6
        assert freq_table.char_count[ord('C')] == 2
        assert freq_table.char_count[ord('D')] == 10
        assert freq_table.char_count[ord('E')] == 7
        assert freq_table.char_count[ord('F')] == 0
        assert freq_table.char_count[ord('G')] == 0
        assert freq_table.char_count[ord('H')] == 0
        assert freq_table.char_count[ord(' ')] == 10


class TestHTree:
    def test_basic(self):
        ## For this test, I'm just inspecting that a tree with no children works
        ## We'll test that the tree is built in the right way later.
        root = HTree()
        left_child = HTree(c="A", freq=3)
        right_child = HTree(c="B", freq=5)

        assert root.freq == 0
        assert left_child.freq == 3
        assert left_child.char == "A"
        assert right_child.freq == 5
        assert right_child.char == "B"
        assert left_child.p0 is None
        assert left_child.p1 is None

        assert right_child.p0 is None
        assert right_child.p1 is None

    def test_basic_char_count(self):
        ## For this test, I'm just inspecting that a tree with no children works
        ## We'll test that the tree is built in the right way later.
        root = HTree()
        left_child = HTree(c="A", freq=3)
        right_child = HTree(c="B", freq=5)

        assert left_child.get_char_count("A") == 3
        assert right_child.get_char_count("A") == -1
        assert right_child.get_char_count("B") == 5
        assert root.get_char_count("A") == -1

    def test_get_char_count_2_levels(self):
        ## For this test, I'm manually building up a tree to test that
        ##  the functionality works
        ## We'll test that the tree is built in the right way later.
        root = HTree()
        left_child = HTree(c="A", freq=3)
        right_child = HTree(c="B", freq=5)
        root.p0 = left_child
        root.p1 = right_child

        assert left_child.get_char_count("A") == 3
        assert right_child.get_char_count("A") == -1
        assert right_child.get_char_count("B") == 5

        assert root.get_char_count("A") == 3
        assert root.get_char_count("B") == 5
        assert root.get_char_count("C") == -1

    def test_get_path_2_levels(self):
        ## For this test, I'm manually building up a tree to test that
        ##  the functionality works
        ## We'll test that the tree is built in the right way later.
        root = HTree()
        left_child = HTree(c="A", freq=3)
        right_child = HTree(c="B", freq=5)
        root.p0 = left_child
        root.p1 = right_child

        assert left_child.get_char_path("A") == ""
        assert right_child.get_char_path("B") == ""
        assert root.get_char_path("A") == "0"
        assert root.get_char_path("B") == "1"

    def test_printing(self):
        root = HTree()
        left_child = HTree(c="A", freq=3)
        right_child = HTree(c="B", freq=5)
        root.p0 = left_child
        root.p1 = right_child

        root.print_tree()
        print("Inspect the output")

    def test_serialize(self):
        root = HTree()
        left_child = HTree(c="A", freq=3)  # path = 0
        right_child = HTree()
        right_left_child = HTree(c="B", freq=5)  # path = 10
        right_right_child = HTree(c="C", freq=5)  # path = 11
        root.p0 = left_child
        root.p1 = right_child

        right_child.p0 = right_left_child
        right_child.p1 = right_right_child

        expected_serialize = "A0B10C11"

        assert root.serialize() == expected_serialize

    def test_serialize_and_deserialize(self):
        serialized_tree = "A0B10C11"

        new_tree = HTree()
        new_tree.deserialize(serialized_tree)

        assert new_tree.p0.char == "A"
        assert new_tree.p1.p0.char == "B"
        assert new_tree.p1.p1.char == "C"

        assert serialized_tree == new_tree.serialize()


class TestLookupTable:

    def test_basic(self):
        lut = LUT()
        lut.set_encoding('b', "00")
        lut.set_encoding('i', "10")
        lut.set_encoding('k', "11")
        lut.set_encoding('e', "01")

        assert lut.get_encoding('b') == "00"
        assert lut.get_encoding('e') == "01"
        assert lut.get_encoding('i') == "10"
        assert lut.get_encoding('k') == "11"


class TestEncoder:

    def test_the_whole_shebang(self):
        encoder = Encoder()
        encoded_message = encoder.encode("bike")
        assert encoder.freq_table.char_count[ord('b')] == 1
        assert encoder.freq_table.char_count[ord('i')] == 1
        assert encoder.freq_table.char_count[ord('k')] == 1
        assert encoder.freq_table.char_count[ord('e')] == 1

        message = encoded_message.encoded_bit_sequence.get_bits_as_string()

        assert message == "00101101"

    def test_encode_alt(self):
        test_string = "BACADAEAFABBAAAGAH"
        expected_bit_sequence = '1110100001001010 1001011011111100 0110001101'
        encoder = Encoder()
        encoded_message = encoder.encode(test_string)

        message = encoded_message.encoded_bit_sequence.get_bits_as_string()
        assert message == expected_bit_sequence

class TestDecoder:

    def test_decode(self):
        print("Test: Decode")
        test_string = "BACADAEAFABBAAAGAH"
        from_table = '1110100001001010 10010110111111000110001101'
        encoder = Encoder()
        secret_message = encoder.encode(test_string)

        decoder = Decoder(secret_message.huffman_tree)
        decoded_message = decoder.decode(secret_message.encoded_bit_sequence)

        assert decoded_message == test_string


