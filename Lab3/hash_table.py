class HashTableElement:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, number_keys=200):
        self.__number_keys = number_keys
        self.__buckets = [[] for i in range(number_keys)]
        self.size = 0

    def hash(self, key):
        hash_ = 0
        for char in key:
            hash_ = (hash_ * 256 + ord(char)) % self.__number_keys
        return hash_

    def add(self, key, value):
        index = self.hash(key)
        self.size += 1
        self.__buckets[index].append(HashTableElement(key, value))

    def get(self, key):
        index = self.hash(key)
        keys = [*filter(lambda n: n.key == key, self.__buckets[index])]
        if keys:
            return keys[0].value
        else:
            return None

    def get_all(self):
        result = []
        for bucket in self.__buckets:
            result += bucket
        return result


if __name__ == "__main__":
    t = HashTable()
    hash_result = t.hash("asb")
    print(hash_result)
    for i in range(100, 201):
        t.add(str(i), {"a": "b"})

    for i in range(99, 105):
        for j in range(5):
            values = t.get(str(i))
            if i < 100:
                assert values is None
            else:
                assert values == {"a": "b"}