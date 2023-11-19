# util.py
import binascii

def hex2bin(hx):
    """
    Converts a hex string to binary. Assumes hex string starts with '0x'.
    """
    if hx.startswith("0x"):
        hx = hx[2:]
    try:
        return binascii.unhexlify(hx)
    except binascii.Error as e:
        raise ValueError("Invalid hex string") from e

def bin2hex(bin_data):
    """
    Converts binary data to a hex string, prefixed with '0x'.
    """
    return "0x" + binascii.hexlify(bin_data).decode()

def hex2str(hx):
    """
    Converts a hex string to a string (assuming UTF-8 encoding).
    """
    try:
        bin_data = hex2bin(hx)
        return bin_data.decode('utf-8')
    except ValueError as e:
        raise ValueError("Invalid hex string") from e

def str2hex(s):
    """
    Converts a string to a hex string.
    """
    return bin2hex(s.encode('utf-8'))

def address2bin(address):
    """
    Converts an Ethereum address in hex format to binary, padding to 32 bytes.
    """
    address_bin = hex2bin(address)
    return address_bin.rjust(32, b'\x00')

def pad_bytes(bin_data, size):
    """
    Pads binary data to the specified size.
    """
    return bin_data.rjust(size, b'\x00')

def pad_bytes_left(bin_data, size):
    """
    Pads binary data to the specified size, padding on the left.
    """
    return pad_bytes(bin_data, size)

def pad_bytes_right(bin_data, size):
    """
    Pads binary data to the specified size, padding on the right.
    """
    return bin_data.ljust(size, b'\x00')
