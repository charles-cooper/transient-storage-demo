import boa
import boa.environment

# something to keep track of transactions (in the transient storage sense)
class TransactionManager:
    def __init__(self):
        self.transient_storage = {}

    def begin_transaction(self):
        return self

    def __enter__(self):
        pass

    def end_transaction(self):
        self.transient_storage = {}

    def __exit__(self, *args):
        self.end_transaction()

class TLOAD:
    opcode = 0xB3
    mnemonic = "TLOAD"

    GAS_COST = 100  # stub

    def __init__(self, txn_manager):
        self.txn_manager = txn_manager

    def __call__(self, computation):
        slot = computation._stack.pop1_int()
        computation.consume_gas(self.GAS_COST, self.mnemonic)

        res = self.txn_manager.transient_storage.get(slot, 0)
        computation._stack.push_int(res)

class TSTORE:
    opcode = 0xB4
    mnemonic = "TSTORE"

    GAS_COST = 100  # stub

    def __init__(self, txn_manager):
        self.txn_manager = txn_manager

    def __call__(self, computation):
        slot = computation._stack.pop1_int()
        val = computation._stack.pop1_int()
        computation.consume_gas(self.GAS_COST, self.mnemonic)

        res = self.txn_manager.transient_storage[slot] = val

transaction_manager = TransactionManager()

# patch py-evm using patch_opcodes util
boa.environment.patch_opcode(TLOAD.opcode, TLOAD(transaction_manager))
boa.environment.patch_opcode(TSTORE.opcode, TSTORE(transaction_manager))

t = boa.load("contracts/transient.vy")

with transaction_manager.begin_transaction():
    t.run_one()
    t.run_one()

