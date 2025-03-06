from multiverse_project.data_structures.dynamicArray import Dynamic_Array

class Dictionary:
    def __init__(self):
        self.keys = Dynamic_Array()
        self.values = Dynamic_Array()
    
    def __setitem__(self, key, value):
        """Sets or updates a key-value pair in the dictionary."""
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                self.values[i] = value
                return
        self.keys.append(key)
        self.values.append(value)
    
    def __getitem__(self, key):
        """Retrieves the value associated with a given key."""
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                return self.values[i]
        raise KeyError("Key not found")
    
    def __delitem__(self, key):
        """Removes a key-value pair from the dictionary."""
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                self.keys.pop(i)  # Remove key at index i
                self.values.pop(i)  # Remove corresponding value
                return
        raise KeyError("Key not found")

    def __contains__(self, key):
        """Checks if a key exists in the dictionary."""
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                return True
        return False
    
    def __iter__(self):
        """Iterates over keys in the dictionary."""
        for i in range(len(self.keys)):
            yield self.keys[i]

    def __len__(self):
        """Returns the number of key-value pairs."""
        return len(self.keys)

    def get(self, key, default=None):
        """Retrieves a value for a key, or returns default if the key does not exist."""
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                return self.values[i]
        return default
    
    # def keys(self):
    #     """Returns a My_List containing all keys."""
    #     keys_list = Dynamic_Array()
    #     for key in self.keys:
    #         keys_list.append(key)
    #     return keys_list

    # def values(self):
    #     """Returns a My_List containing all unique values."""
    #     values_list = Dynamic_Array()
    #     for value in self.values:
    #         # Manually check if value already exists in values_list
    #         is_unique = True
    #         for existing_value in values_list:
    #             if existing_value == value:
    #                 is_unique = False
    #                 break
    #         if is_unique:
    #             values_list.append(value)
    #     return values_list

    def items(self):
        """Returns an iterator of (key, value) pairs."""
        for i in range(len(self.keys)):
            yield (self.keys[i], self.values[i])

    def pop(self, key, default=None):
        """Removes the specified key and returns its value. 
        If the key does not exist, return default (or raise KeyError if no default is provided)."""
        for i in range(len(self.keys)):
            if self.keys[i] == key:
                value = self.values.pop(i)  # Remove the value
                self.keys.pop(i)  # Remove the corresponding key
                return value
        if default is not None:
            return default
        raise KeyError(f"Key {key} not found")

    def __repr__(self):
        """String representation of the dictionary."""
        return f"{{{', '.join(f'{repr(self.keys[i])}: {repr(self.values[i])}' for i in range(len(self.keys)))}}}"
