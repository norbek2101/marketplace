class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.__balance = 0

    def deposit(self, summa: float):
        if summa <= 0:
            raise ValueError("Summa musbat bo‘lishi kerak")
        self.__balance += summa
        return self.__balance

    def withdraw(self, summa: float):
        if summa <= 0:
            raise ValueError("Summa musbat bo‘lishi kerak")
        if summa > self.__balance:
            raise ValueError("Yetarli mablag‘ mavjud emas")
        self.__balance -= summa
        return self.__balance
    
    @property    
    def balance(self):
        """Read-only access"""
        return self.__balance

    def __str__(self):
        return (
            f"Name: {self.name} | "
            f"Age: {self.age} | "
            f"Balance: {self.__balance}"
        )
