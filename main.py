"""
    Ticket Booking system

    - Jensen Trillo, **v1.1**, 13/05/2024
    - ``Python 3.11.6``
"""
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
        return total, quantity


class GUI(ctk.CTk):
    class TicketsFrame(ctk.CTkFrame):
        """ Frame for containing tickets & information. """
        class ScrollFrame(ctk.CTkScrollableFrame):
            """ Scrollable frame for all tickets to be placed within. """
            class TicketObj(ctk.CTkFrame):
                """ Ticket object for the scroll frame. """
                def __init__(self, master):
                    super().__init__(master)

            def __init__(self, master, tickets: List[Ticket]):
                super().__init__(master, width=450, height=330, fg_color='#FFFFFF', corner_radius=0)
                for i, obj in enumerate(tickets):
                    # Pass ticket here in next ver
                    self.TicketObj(self).grid(row=i, column=0)

        def __init__(self, master, tickets: List[Ticket]):
            super().__init__(master, width=450, height=350, fg_color='#FFFFFF', corner_radius=0)
            self.grid_propagate(False)
            # Header texts
            ctk.CTkLabel(self, text='Ticket', text_color='#000000', font=('JetBrains Mono NL', 16)).grid(
                row=0, column=0, sticky='w', padx=(10, 0))
            ctk.CTkLabel(self, text='Quantity', text_color='#000000', font=('JetBrains Mono NL', 16)).grid(
                row=0, column=1, padx=(0, 5))
            # Scroll frame
            self.ScrollFrame(self, tickets).grid(row=1, column=0, columnspan=2)

    def __init__(self, tickets: List[Ticket]):
        ctk.set_appearance_mode('system')
        super().__init__(fg_color='#FFFCFC')
        self.geometry('500x612'), self.resizable(False, False)
        self.title('Ticket Booking')
        ctk.FontManager().load_font('assets/JetBrainsMonoNL-Bold.ttf')
        ctk.FontManager().load_font('assets/JetBrainsMonoNL-Regular.ttf')
        #
        self.grid_anchor('c'), self.grid_propagate(False)
        ctk.CTkLabel(self, text='Ticket Booking', text_color='#000000', font=('JetBrains Mono NL Bold', 24)).grid(
            row=0, column=0, pady=(50, 0), sticky='w')
        self.TicketsFrame(self, tickets).grid(row=1, column=0)
        #
        self.mainloop()
        

if __name__ == '__main__':
    GUI()
