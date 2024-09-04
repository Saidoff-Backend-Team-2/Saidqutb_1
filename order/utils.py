import random

def generate_order_number():
    return f"#{random.randint(100000, 999999)}"
