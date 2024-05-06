import customtkinter as ctk
from typing import List
remaining_tickets = 100


class Ticket:
    def __calc_subtotal(self):
        return self.price * self.quantity

    def __init__(self, price: float, quantity: int):
        self.price, self.quantity = price, quantity
        self.subtotal = self.__calc_subtotal()


class Order:
    def __init__(self, tickets: List[Ticket]):
        self.total, self.quantity = sum([n.subtotal for n in tickets]), sum([n.quantity for n in tickets])


# class GUI(ctk.CTk):
#     def __init__(self):
#         ctk.set_appearance_mode('system')
