# Brought to you by Github Copilot

class StacksAndQueues:
    def __init__(self):
        self.stack = []
        self.queue = []

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        return self.stack.pop()

    def enqueue(self, data):
        self.queue.append(data)

    def dequeue(self):
        return self.queue.pop(0)

    def how_to_use_a_stack(self):
        print("\nStacks...")
        self.push(1)
        self.push(2)
        self.push(3)
        self.push(4)
        self.push(5)
        print(self.stack)
        print(self.pop())
        print(self.stack)
        print(self.pop())
        print(self.stack)
        print(self.pop())
        print(self.stack)
        print(self.pop())
        print(self.stack)
        print(self.pop())
        print(self.stack)

    def how_to_use_a_queue(self):
        print("\nQueues...")
        self.enqueue(1)
        self.enqueue(2)
        self.enqueue(3)
        self.enqueue(4)
        self.enqueue(5)
        print(self.queue)
        print(self.dequeue())
        print(self.queue)
        print(self.dequeue())
        print(self.queue)
        print(self.dequeue())
        print(self.queue)
        print(self.dequeue())
        print(self.queue)
        print(self.dequeue())
        print(self.queue)

    def example(self):
        print("Stacks and Queues")
        self.how_to_use_a_stack()
        self.how_to_use_a_queue()


if __name__ == "__main__":
    stacks_and_queues = StacksAndQueues()
    stacks_and_queues.example()
