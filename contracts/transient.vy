
counter: transient(HashMap[address, uint256])

@external
def run_one():
    print("ENTER", self.counter[msg.sender])
    self.counter[msg.sender] += 1
