import hashlib
from enum import Enum

from .boxes import Direction


class Role(Enum):
    SERVER = 0
    CLIENT = 1

class Generator(object):
    def __init__(self, role, queues, messages, programs):
        # Parser data
        self.role = role
        self.queues = queues
        self.messages = messages
        self.programs = programs

        # Generated data
        self.opcodes = {}
        self.message_packer = {}
        self.message_unpacker = {}
        self.message_sizes = {}
        self.generated_programs = []
        self.recv_list = []
        self.send_list = []

    # Generates a deterministic (given the same inputs in the same order) opcode from a name
    def get_opcode(self, program_name):
        if program_name in self.opcodes:
            return self.opcodes[program_name]

        def get_digest(h, encoded):
            h.update(encoded)
        
            # Keep higher most byte reserved for encryption flag
            digest = bytearray(h.digest())
            digest[0] = digest[0] & (~(1 << 7))
            digest = bytearray.hex(digest)
            return digest
        
        encoded = program_name.encode('utf-8')
        h = hashlib.blake2b(digest_size=2)
        digest = get_digest(h, encoded)
        while digest in self.USED_OPCODES.values():
            digest = get_digest(h, encoded)

        self.opcodes[program_name] = digest
        return digest

    
    def generate_message_packer(self, message):
        message_name = message.identifier.eval()
        if message_name in self.message_packer:
            return self.message_packer[message_name]

        packer = self._generate_message_packer(self, message)
        self.message_packer[message_name] = packer
        return packer
    
    def generate_message_unpacker(self, message):
        message_name = message.identifier.eval()
        if message_name in self.message_unpacker:
            return self.message_unpacker[message_name]

        packer = self._generate_message_unpacker(self, message)
        self.message_unpacker[message_name] = packer
        return packer

    def generate_message_size(self, message):
        message_name = message.identifier.eval()
        if message_name in self.message_size:
            return self.message_size[message_name]

        method = self._generate_message_size(self, message)
        self.message_size[message_name] = method
        return packer

    def generate_program(self, program):
        program_name = program.name.eval()

        # Get an opcode for the RPC
        opcode = self.get_opcode(program_name)

        # Message packer/unpacker according to direction
        direction = program.direction
        if direction == Direction.BOTH or \
            (direction == Direction.S2C and self.role == Role.SERVER) or \
            (direction == Direction.C2S and self.role == Role.CLIENT):

            self.generate_message_packer(self.messages[program.arg.eval()])
            self._generate_program_send(program)
            self.send_list.append(program_name)

        if direction == Direction.BOTH or \
            (direction == Direction.C2S and self.role == Role.SERVER) or \
            (direction == Direction.S2C and self.role == Role.CLIENT):

            self.generate_message_unpacker(self.messages[program.arg.eval()])
            self._generate_program_recv(program)
            self.recv_list.append(program_name)

        # Message size calculation
        self.generate_message_size(message)

        # Done
        self.generated_programs.append(program_name)

    def generate(self):
        for program in self.programs:
            self.generate_program(program)
    