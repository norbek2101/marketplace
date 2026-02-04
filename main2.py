import json
import os
from abc import ABC, abstractmethod
from itertools import count
from typing import List, Union

# --- CUSTOM EXCEPTIONS ---
class MarketplaceError(Exception): pass
class InsufficientFundsError(MarketplaceError): pass

# --- MODELS ---
class Product(ABC):
    _id_counter = count(1001)

    def __init__(self, name: str, price: float, quantity: int, id=None):
        self.id = id if id else next(self._id_counter)
        self.name = name
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def to_dict(self) -> dict:
        """JSONga saqlash uchun lug'at ko'rinishiga o'girish"""
        pass

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} - {self.price:,} so'm ({self.quantity} dona)"

class ElectronicProduct(Product):
    def __init__(self, name, price, quantity, warranty_years, id=None):
        super().__init__(name, price, quantity, id)
        self.warranty_years = warranty_years

    def to_dict(self):
        return {
            "type": "Electronic", "id": self.id, "name": self.name,
            "price": self.price, "quantity": self.quantity, "warranty_years": self.warranty_years
        }

class FoodProduct(Product):
    def __init__(self, name, price, quantity, expiry_date, id=None):
        super().__init__(name, price, quantity, id)
        self.expiry_date = expiry_date

    def to_dict(self):
        return {
            "type": "Food", "id": self.id, "name": self.name,
            "price": self.price, "quantity": self.quantity, "expiry_date": self.expiry_date
        }

class User:
    def __init__(self, name: str, balance: float = 0.0):
        self.name = name
        self._balance = balance

    @property
    def balance(self): return self._balance

    def deposit(self, amount: float):
        if amount <= 0: raise ValueError("Musbat summa kiriting")
        self._balance += amount

    def withdraw(self, amount: float):
        if amount > self._balance:
            raise InsufficientFundsError(f"Mablag' yetarli emas! Balans: {self._balance}")
        self._balance -= amount

    def to_dict(self):
        return {"name": self.name, "balance": self._balance}

# --- DATABASE / STORAGE ---
class Storage:
    FILE_NAME = "marketplace_data.json"

    @classmethod
    def save(cls, products: List[Product], users: List[User]):
        data = {
            "products": [p.to_dict() for p in products],
            "users": [u.to_dict() for u in users]
        }
        with open(cls.FILE_NAME, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load(cls):
        if not os.path.exists(cls.FILE_NAME):
            return [], []
        
        with open(cls.FILE_NAME, "r") as f:
            data = json.load(f)
        
        users = [User(u['name'], u['balance']) for u in data.get('users', [])]
        products = []
        for p in data.get('products', []):
            if p['type'] == "Electronic":
                products.append(ElectronicProduct(p['name'], p['price'], p['quantity'], p['warranty_years'], p['id']))
            else:
                products.append(FoodProduct(p['name'], p['price'], p['quantity'], p['expiry_date'], p['id']))
        
        # ID counter-ni yangilash
        if products:
            max_id = max(p.id for p in products)
            Product._id_counter = count(max_id + 1)
            
        return products, users

# --- MARKETPLACE ENGINE ---
class Marketplace:
    def __init__(self):
        self.products, self.users = Storage.load()
        self.current_user = self.users[0] if self.users else None

    def add_user(self, name):
        new_user = User(name)
        self.users.append(new_user)
        self.current_user = new_user
        Storage.save(self.products, self.users)

    def buy(self, prod_id, qty):
        prod = next((p for p in self.products if p.id == prod_id), None)
        if not prod or prod.quantity < qty:
            print("❌ Mahsulot topilmadi yoki omborda yetarli emas!")
            return
        
        try:
            total = prod.price * qty
            self.current_user.withdraw(total)
            prod.quantity -= qty
            Storage.save(self.products, self.users)
            print(f"✅ Xarid bajarildi! Jami: {total:,} so'm")
        except InsufficientFundsError as e:
            print(f"❌ {e}")

# --- CLI INTERFACE ---
def main():
    market = Marketplace()
    
    if not market.current_user:
        name = input("Xush kelibsiz! Ismingizni kiriting: ")
        market.add_user(name)

    while True:
        print(f"\n--- 🏪 MARKETPLACE | Foydalanuvchi: {market.current_user.name} | Balans: {market.current_user.balance:,} ---")
        print("1. Mahsulotlarni ko'rish")
        print("2. Pul kiritish (Deposit)")
        print("3. Sotib olish")
        print("4. Admin: Mahsulot qo'shish")
        print("0. Chiqish")
        
        choyce = input("Tanlang: ")
        
        if choyce == "1":
            for p in market.products: print(p)
        elif choyce == "2":
            amount = float(input("Summa: "))
            market.current_user.deposit(amount)
            Storage.save(market.products, market.users)
        elif choyce == "3":
            p_id = int(input("Mahsulot ID: "))
            qty = int(input("Nechta: "))
            market.buy(p_id, qty)
        elif choyce == "4":
            name = input("Nomi: ")
            price = float(input("Narxi: "))
            qty = int(input("Soni: "))
            # Soddalik uchun faqat elektronika qo'shamiz
            market.products.append(ElectronicProduct(name, price, qty, 1))
            Storage.save(market.products, market.users)
        elif choyce == "0":
            break

if __name__ == "__main__":
    main()