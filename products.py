from itertools import count
from abc import ABC, abstractmethod


class Product(ABC):
    _id_counter = count(1001)

    def __init__(self, name: str, price: float, quantity: int):
        if price < 0:
            raise ValueError("Price manfiy bo‘lishi mumkin emas")
        if quantity < 0:
            raise ValueError("Quantity manfiy bo‘lishi mumkin emas")

        self.id = next(Product._id_counter)
        self.name = name
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self) -> str:
        """Har bir product o‘ziga xos str formatga ega bo‘lishi shart"""
        pass

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, name='{self.name}', "
            f"price={self.price}, quantity={self.quantity})"
        )

    def total_price(self):
        """Mahsulot umumiy narxi"""
        return self.price * self.quantity


class ElectronicProduct(Product):
    def __init__(self, name, price, quantity, warranty_years: int):
        if warranty_years < 0:
            raise ValueError("Warranty yillari manfiy bo‘lishi mumkin emas")

        super().__init__(name, price, quantity)
        self.warranty_years = warranty_years

    def __str__(self):
        return (
            f"ID: {self.id} | NAME: {self.name} | "
            f"PRICE: {self.price} | QUANTITY: {self.quantity} | "
            f"WARRANTY_YEARS: {self.warranty_years}"
        )


class FoodProduct(Product):
    def __init__(self, name, price, quantity, expiry_date: str):
        super().__init__(name, price, quantity)
        self.expiry_date = expiry_date

    def __str__(self):
        return (
            f"ID: {self.id} | NAME: {self.name} | "
            f"PRICE: {self.price} | QUANTITY: {self.quantity} | "
            f"EXPIRY_DATE: {self.expiry_date}"
        )
        
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.__balance = 0
    
    def deposit(self, summa):
        self.__balance += summa
        return f"Balance: {self.__balance}"
        
    def withdraw(self, summa):
        if summa < 0:
            raise ValueError("Summa manfiy bo'lishi mumkin emas")
        if summa > self.__balance:
            raise ValueError("Yetarli mablag' mavjud emas")
        self.__balance += summa
        return f"Balance: {self.__balance}"
        
    def __str__(self) -> str:
        return (
            f"name: {self.name} "
            f"age: {self.age}"
            f"balance: {self.__balance}"
        )
        

if __name__ == '__main__':
    iphone = ElectronicProduct("Iphone 17 Pro Max", 18_000_000, 1, 1)
    konserva = FoodProduct("Konserva", 78_000, 1, "21-01-2028")
    
    print(iphone)
    print(konserva)
    
    print(repr(iphone))
    print("Total:", iphone.total_price())
