import json

class User:
    def __init__(self):
        self.open_claims = {}
        self.open_disputes = {}
        self.total_disputes = 0
        self.won_disputes = 0
        self.total_claims = 0
        self.correct_claims = 0


class Claim:
    def __init__(self, user_address, disputing_user_address, value, last_edited, status, data_chunks):
        self.user_address = user_address
        self.disputing_user_address = disputing_user_address
        self.value = value
        self.last_edited = last_edited
        self.status = status
        self.data_chunks = data_chunks


class SimplifiedClaim:
    def __init__(self, id, status, value):
        self.id = id
        self.status = status
        self.value = value


class DataChunks:
    def __init__(self):
        self.chunks_data = {}
        self.total_chunks = 0

    def __json__(self):
        size = sum(len(chunk.data) for chunk in self.chunks_data.values())
        chunk_indexes = list(self.chunks_data.keys())
        return json.dumps({
            "totalChunks": self.total_chunks,
            "size": size,
            "chunks": chunk_indexes
        })


class Chunk:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return f"{len(self.data)}b"


class Status:
    UNDEFINED = 0
    OPEN = 1
    DISPUTING = 2
    FINALIZED = 3
    DISPUTED = 4
    VALIDATED = 5
    CONTRADICTED = 6

    _statuses = ["undefined", "open", "disputing", "finalized", "disputed", "validated", "contradicted"]

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return Status._statuses[self.value] if self.value < len(Status._statuses) else "unknown"

    def __json__(self):
        return json.dumps(str(self))
