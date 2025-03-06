class Zn_verse:
    def __init__(self, a, n):
        if not (isinstance(a, int) and isinstance(n, int)):
            raise TypeError("Both a and n must be integers.")
        if n <= 1:
            raise ValueError("n must be greater than 1.")
        if not (0 <= a < n):
            raise ValueError("a must be in the range 0 <= a < n.")
        
        self.a = a
        self.n = n
    
    def contains(self, k):
        return isinstance(k, int) and (k - self.a) % self.n == 0
    
    def generate(self, lower, upper):
        if not (isinstance(lower, int) and isinstance(upper, int)):
            raise TypeError("Bounds must be integers.")
        if lower > upper:
            raise ValueError("Lower bound must be <= upper bound.")
        start = self.a if self.a >= lower else lower + (self.n - (lower - self.a) % self.n) % self.n
        return [k for k in range(start, upper + 1, self.n)]
    
    def __repr__(self):
        return f"[{self.a}]ℤ{self.n}"
    
    def __contains__(self, k):
        return self.contains(k)
    
    def __eq__(self, other):
        return isinstance(other, Zn_verse) and self.n == other.n and self.a % self.n == other.a % self.n
    
    def __hash__(self):
        return hash((self.a % self.n, self.n))

