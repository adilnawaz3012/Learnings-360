class MyHashMap:

    def __init__(self):
        from collections import defaultdict
        self.hashMap = defaultdict(int)

    def put(self, key: int, value: int) -> None:
        self.hashMap[key] = value

    def get(self, key: int) -> int:
        return self.hashMap[key] if key in self.hashMap else -1

    def remove(self, key: int) -> None:
        if key in self.hashMap:
            del self.hashMap[key]