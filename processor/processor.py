import csv
import io
import gzip
import hex
import struct
from ipfs_cid import cid_sha256_hash, cid_sha256_unwrap_digest
from model import Chunk

def csv_blank_cell_percentage(csv_string, nil_fields=None):
    if nil_fields is None:
        nil_fields = []

    nil_fields_map = {field.lower(): True for field in nil_fields}

    total_cells = 0
    empty_cells = 0

    reader = csv.reader(io.StringIO(csv_string))
    first_row = True
    for record in reader:
        if first_row:
            first_row = False
            continue

        for value in record:
            total_cells += 1
            if value == "" or nil_fields_map.get(value.lower()):
                empty_cells += 1

    n_data_cells = total_cells - empty_cells
    value = 1000000 * n_data_cells // total_cells

    return value

def get_data_cid(data):
    return cid_sha256_hash(data.encode())

def compare_cid_with_string(data_cid, marshaled_string):
    try:
        cid_digest = cid_sha256_unwrap_digest(data_cid)
        return cid_digest == cid_sha256_unwrap_digest(marshaled_string)
    except AttributeError:
        return False

def compress_data(data):
    try:
        buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode="wb") as gzip_file:
            gzip_file.write(data)
        return buffer.getvalue()
    except Exception as e:
        raise Exception(f"CompressData: error compressing data: {e}")

def decompress_data(data):
    try:
        with gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb") as gzip_file:
            return gzip_file.read()
    except Exception as e:
        raise Exception(f"DecompressData: error decompressing data: {e}")

def prepare_data_to_send(data, max_size):
    if not data:
        raise ValueError("PrepareData: Invalid empty data")

    try:
        compressed = compress_data(data)
    except Exception as e:
        raise Exception(f"PrepareData: error compressing data: {e}")

    size_data = len(compressed)
    total_chunks = size_data // max_size
    if size_data % max_size == 0:
        total_chunks -= 1

    prepared_data = []
    for chunk_index in range(total_chunks + 1):
        metadata = struct.pack(">II", chunk_index, total_chunks)
        top = (chunk_index + 1) * max_size
        top = min(top, size_data)
        all_data = metadata + compressed[chunk_index * max_size:top]
        all_data_hex = "0x" + hex.encode(all_data)
        prepared_data.append(all_data_hex)

    return prepared_data

def update_data_chunks(data_chunks, chunk_hex):
    chunk = bytes.fromhex(chunk_hex[2:])
    chunk_index = struct.unpack(">I", chunk[:4])[0]
    total_chunks = struct.unpack(">I", chunk[4:8])[0] + 1
    data = chunk[8:]

    if chunk_index > total_chunks:
        raise ValueError("Inconsistent chunk index, greater than total")

    if data_chunks.total_chunks == 0:
        data_chunks.chunks_data = {}
        data_chunks.total_chunks = total_chunks
    elif total_chunks != data_chunks.total_chunks:
        raise ValueError("Inconsistent number of chunks")

    data_chunks.chunks_data[chunk_index] = Chunk(data)

def compose_data_from_chunks(data_chunks):
    if len(data_chunks.chunks_data) != data_chunks.total_chunks:
        raise ValueError("Wrong number of chunks")

    ordered_chunks = [data_chunks.chunks_data[i].data for i in range(data_chunks.total_chunks)]
    compressed_data = b''.join(ordered_chunks)

    return decompress_data(compressed_data)
