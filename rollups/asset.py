import util
import binascii
from decimal import Decimal

class EtherDeposit:
    def __init__(self, depositor, amount, data):
        self.depositor = depositor
        self.amount = amount
        self.data = data

class Erc20Deposit:
    def __init__(self, depositor, token_address, amount, data):
        self.depositor = depositor
        self.token_address = token_address
        self.amount = amount
        self.data = data

class Erc721Deposit:
    def __init__(self, depositor, token_address, token_id, data):
        self.depositor = depositor
        self.token_address = token_address
        self.token_id = token_id
        self.data = data

class Erc1155SingleDeposit:
    def __init__(self, depositor, token_address, token_id, amount, base_layer_data, exec_layer_data):
        self.depositor = depositor
        self.token_address = token_address
        self.token_id = token_id
        self.amount = amount
        self.base_layer_data = base_layer_data
        self.exec_layer_data = exec_layer_data

class Erc1155BatchDeposit:
    def __init__(self, depositor, token_address, token_ids, amounts, base_layer_data, exec_layer_data):
        self.depositor = depositor
        self.token_address = token_address
        self.token_ids = token_ids
        self.amounts = amounts
        self.base_layer_data = base_layer_data
        self.exec_layer_data = exec_layer_data

def decode_ether_deposit(payload_hex):
    bin_data = util.hex2bin(payload_hex)
    amount = int.from_bytes(bin_data[20:52], byteorder='big')
    return EtherDeposit(util.bin2hex(bin_data[:20]), amount, bin_data[52:])

def decode_erc20_deposit(payload_hex):
    bin_data = util.hex2bin(payload_hex)
    amount = int.from_bytes(bin_data[41:73], byteorder='big')
    return Erc20Deposit(util.bin2hex(bin_data[21:41]), util.bin2hex(bin_data[1:21]), amount, bin_data[73:])

def decode_erc721_deposit(payload_hex):
    bin_data = util.hex2bin(payload_hex)
    token_id = int.from_bytes(bin_data[40:72], byteorder='big')
    return Erc721Deposit(util.bin2hex(bin_data[20:40]), util.bin2hex(bin_data[:20]), token_id, bin_data[72:])

def decode_erc1155_single_deposit(payload_hex):
    bin_data = util.hex2bin(payload_hex)
    token_id = int.from_bytes(bin_data[40:72], byteorder='big')
    amount = int.from_bytes(bin_data[72:104], byteorder='big')

    all_data = bin_data[104:]
    bl_data_position = int.from_bytes(all_data[0:32], byteorder='big')
    bl_data_size = int.from_bytes(all_data[bl_data_position:bl_data_position+32], byteorder='big')
    bl_data = all_data[bl_data_position+32:bl_data_position+32+bl_data_size]

    el_data_position = int.from_bytes(all_data[32:64], byteorder='big')
    el_data_size = int.from_bytes(all_data[el_data_position:el_data_position+32], byteorder='big')
    el_data = all_data[el_data_position+32:el_data_position+32+el_data_size]

    return Erc1155SingleDeposit(util.bin2hex(bin_data[20:40]), util.bin2hex(bin_data[:20]), token_id, amount, bl_data, el_data)

def decode_erc1155_batch_deposit(payload_hex):
    bin_data = util.hex2bin(payload_hex)
    token_address = util.bin2hex(bin_data[:20])
    depositor = util.bin2hex(bin_data[20:40])

    all_data = bin_data[40:]
    ids_position = int.from_bytes(all_data[0:32], byteorder='big')
    ids_size = int.from_bytes(all_data[ids_position:ids_position+32], byteorder='big')
    token_ids = [int.from_bytes(all_data[ids_position+32*(i+1):ids_position+32*(i+2)], byteorder='big') for i in range(ids_size)]

    amounts_position = int.from_bytes(all_data[32:64], byteorder='big')
    amounts_size = int.from_bytes(all_data[amounts_position:amounts_position+32], byteorder='big')
    amounts = [int.from_bytes(all_data[amounts_position+32*(i+1):amounts_position+32*(i+2)], byteorder='big') for i in range(amounts_size)]

    bl_data_position = int.from_bytes(all_data[64:96], byteorder='big')
    bl_data_size = int.from_bytes(all_data[bl_data_position:bl_data_position+32], byteorder='big')
    bl_data = all_data[bl_data_position+32:bl_data_position+32+bl_data_size]

    el_data_position = int.from_bytes(all_data[96:128], byteorder='big')
    el_data_size = int.from_bytes(all_data[el_data_position:el_data_position+32], byteorder='big')
    el_data = all_data[el_data_position+32:el_data_position+32+el_data_size]

    return Erc1155BatchDeposit(depositor, token_address, token_ids, amounts, bl_data, el_data)

def ether_withdrawal_voucher(sender, receiver, amount):
    payload = "0x522f6815" + util.bin2hex(util.address2bin(receiver) + util.pad_bytes(amount.to_bytes(32, byteorder='big'), 32))
    return {"destination": sender, "payload": payload}

def erc20_transfer_voucher(receiver, token_address, amount):
    payload = "0xa9059cbb" + util.bin2hex(util.address2bin(receiver) + util.pad_bytes(amount.to_bytes(32, byteorder='big'), 32))
    return {"destination": token_address, "payload": payload}

def erc721_safe_transfer_voucher(sender, receiver, token_address, token_id):
    payload_bytes = util.address2bin(sender) + util.address2bin(receiver) + util.pad_bytes(token_id.to_bytes(32, byteorder='big'), 32)
    payload = "0x42842e0e" + util.bin2hex(payload_bytes)
    return {"destination": token_address, "payload": payload}

def erc1155_safe_transfer_from_voucher(sender, receiver, token_address, token_id, amount, data):
    data_position = 160
    len_data = len(data)
    slots = len_data // 32 + (1 if len_data % 32 > 0 else 0)

    payload_bytes = util.address2bin(sender) + util.address2bin(receiver)
    payload_bytes += util.pad_bytes(token_id.to_bytes(32, byteorder='big'), 32)
    payload_bytes += util.pad_bytes(amount.to_bytes(32, byteorder='big'), 32)
    payload_bytes += util.pad_bytes(data_position.to_bytes(32, byteorder='big'), 32)
    payload_bytes += util.pad_bytes(len_data.to_bytes(32, byteorder='big'), 32)
    payload_bytes += util.pad_bytes_right(data, slots)

    payload = "0xf242432a" + util.bin2hex(payload_bytes)
    return {"destination": token_address, "payload": payload}

def erc1155_safe_batch_transfer_from_voucher(sender, receiver, token_address, token_ids, amounts, data):
    len_ids = len(token_ids)
    len_amounts = len(amounts)
    len_data = len(data)

    ids_position = 160
    amounts_position = ids_position + 32 + len_ids * 32
    data_position = amounts_position + 32 + len_amounts * 32

    payload_bytes = util.address2bin(sender) + util.address2bin(receiver)
    payload_bytes += util.pad_bytes(ids_position.to_bytes(32, byteorder='big'), 32)
    payload_bytes += util.pad_bytes(amounts_position.to_bytes(32, byteorder='big'), 32)
    payload_bytes += util.pad_bytes(data_position.to_bytes(32, byteorder='big'), 32)

    payload_bytes += util.pad_bytes(len_ids.to_bytes(32, byteorder='big'), 32)
    for id in token_ids:
        payload_bytes += util.pad_bytes(id.to_bytes(32, byteorder='big'), 32)

    payload_bytes += util.pad_bytes(len_amounts.to_bytes(32, byteorder='big'), 32)
    for amount in amounts:
        payload_bytes += util.pad_bytes(amount.to_bytes(32, byteorder='big'), 32)

    payload_bytes += util.pad_bytes(len_data.to_bytes(32, byteorder='big'), 32)
    payload_bytes += util.pad_bytes_right(data, len_data // 32 + (1 if len_data % 32 > 0 else 0))

    payload = "0x2eb2c2d6" + util.bin2hex(payload_bytes)
    return {"destination": token_address, "payload": payload}
