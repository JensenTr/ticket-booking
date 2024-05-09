import customtkinter as ctk
from typing import List
remaining_tickets = 100


class Ticket:
    def __calc_subtotal(self):
        return self.price * self.quantity

    def __init__(self, price: float, quantity: int):
        self.price, self.quantity = price, quantity
        self.subtotal = self.__calc_subtotal()


def process_order(tickets: List[Ticket]):
    """
        Processes an order with the given tickets.

        :param tickets: :class:`list` [:class:`Ticket`, ...]
        :returns: :class:`bool` Whether the order was successful
    """
    global remaining_tickets
    total, quantity = sum([n.subtotal for n in tickets]), sum([n.quantity for n in tickets])
    if (remaining_tickets - quantity) < 0:
        return False
    else:
        remaining_tickets -= quantity
        return True


# class GUI(ctk.CTk):
#     def __init__(self):
#         ctk.set_appearance_mode('system')
