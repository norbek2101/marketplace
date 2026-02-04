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
        
from typing import Union

class InsufficientFundsError(Exception):
    """Balansda mablag' yetarli bo'lmaganda chaqiriladigan maxsus xatolik."""
    pass

class User:
    """
    Marketplace tizimi uchun foydalanuvchi profili.
    
    Attributes:
        name (str): Foydalanuvchi ismi.
        age (int): Foydalanuvchi yoshi (0 dan katta bo'lishi shart).
    """

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self._balance: float = 0.0  # Private attribute

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Yosh musbat butun son bo'lishi kerak")
        self._age = value

    @property
    def balance(self) -> float:
        """Balansni faqat o'qish uchun (Read-only)."""
        return self._balance

    def deposit(self, amount: Union[int, float]) -> float:
        """
        Hisobni to'ldirish.
        
        Args:
            amount: Qo'shilayotgan summa.
        Returns:
            Yangi balans.
        """
        if amount <= 0:
            raise ValueError("Depozit summasi musbat bo'lishi shart")
        
        self._balance += float(amount)
        print(f"💰 {self.name}: Hisob {amount:,} so'mga to'ldirildi.")
        return self._balance

    def withdraw(self, amount: Union[int, float]) -> float:
        """
        Hisobdan pul yechish.
        
        Raises:
            InsufficientFundsError: Balans yetarli bo'lmaganda.
        """
        if amount <= 0:
            raise ValueError("Yechiladigan summa musbat bo'lishi shart")
        
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Xatolik: Balansda yetarli mablag' yo'q. "
                f"Mavjud: {self._balance:,}, So'ralgan: {amount:,}"
            )

        self._balance -= float(amount)
        return self._balance

    def __repr__(self) -> str:
        """Developerlar uchun debug ma'lumoti."""
        return f"User(name='{self.name}', age={self.age}, balance={self._balance})"

    def __str__(self) -> str:
        """Foydalanuvchi uchun chiroyli ko'rinish."""
        return (
            f"👤 Foydalanuvchi: {self.name.title()}\n"
            f"🎂 Yoshi: {self.age}\n"
            f"💳 Balans: {self._balance:,.2f} so'm\n"
            f"{'-'*30}"
        )


class Marketplace:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        """Omborga mahsulot qo'shish"""
        self.products.append(product)
        print(f"✅ Mahsulot qo'shildi: {product.name}")

    def show_products(self):
        """Barcha mahsulotlarni ko'rsatish"""
        print("\n--- 🛒 Marketplace Mahsulotlari ---")
        for p in self.products:
            status = "Sotuvda bor" if p.quantity > 0 else "Tugagan"
            print(f"{p} | Holati: {status}")
        print("----------------------------------\n")

    def sell_product(self, product_id: int, user: User, amount: int):
        """Mahsulotni foydalanuvchiga sotish"""
        # Mahsulotni ID bo'yicha topish
        product = next((p for p in self.products if p.id == product_id), None)

        if not product:
            print("❌ Xato: Mahsulot topilmadi!")
            return

        if product.quantity < amount:
            print(f"❌ Xato: Omborimizda yetarli {product.name} yo'q!")
            return

        total_cost = product.price * amount

        if user.balance < total_cost:
            print(f"❌ Xato: {user.name}, balansingizda yetarli mablag' yo'q!")
            print(f"Kerak: {total_cost}, Mavjud: {user.balance}")
            return

        # Pulni yechish va mahsulot sonini kamaytirish
        user.withdraw(total_cost)
        product.quantity -= amount
        print(f"🎉 Xarid muvaffaqiyatli! {user.name} {amount} ta {product.name} sotib oldi.")
        print(f"Qolgan balans: {user.balance}")

# --- ISHLATIB KO'RAMIZ ---

# 1. Marketplace yaratamiz
bozor = Marketplace()

# 2. Mahsulotlar qo'shamiz
laptop = ElectronicProduct("MacBook Pro", 2000, 5, 2)
olma = FoodProduct("Olma", 2, 50, "2026-05-10")

bozor.add_product(laptop)
bozor.add_product(olma)

# 3. Foydalanuvchi yaratamiz va pul solamiz
bekzod = User("Bekzod", 25)
bekzod.deposit(5000)

# 4. Sotuv jarayoni
bozor.show_products()

# MacBook sotib olamiz (ID: 1001)
bozor.sell_product(1001, bekzod, 2)

# Olma sotib olamiz (ID: 1002)
bozor.sell_product(1002, bekzod, 10)

# Yakuniy holat
bozor.show_products()
print(f"Foydalanuvchi yakuniy holati: {bekzod}")