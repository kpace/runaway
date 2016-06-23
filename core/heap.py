import heapq

class Heap:
    def __init__(self, key=lambda x: x):
        self._data = []
        self.key = key

    def push(self, item):
        heapq.heappush(self._data, (self.key(item), item))

    def pop(self):
        return heapq.heappop(self._data)[1]

    def __contains__(self, item):
        return item in [x[1] for x in self._data]

    def __len__(self):
        return len(self._data)

    def empty(self):
        return len(self) == 0