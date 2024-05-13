"""
    Ticket Booking system

    - Jensen Trillo, **pre-v2**, 14/05/2024
    - ``Python 3.11.6``
"""
import customtkinter as ctk
from typing import List
TICKETS = [('Child', 5), ('Student/Senior', 10), ('Adult', 15)]
remaining_tickets = 100


class Ticket:
    def __calc_subtotal(self):
        return self.price * self.quantity

    def __init__(self, name: str, price: float, quantity: int):
        self.name, self.price, self.quantity = name, price, quantity
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
    """
        Initializes the GUI.

        :param tickets: :class:`list` [:class:`tuple` (:class:`str` ``name``, :class:`float` ``price``), ...]
    """
    def __init__(self, tickets: List[tuple[str, float]]):
        class TicketsFrame(ctk.CTkFrame):
            """ Frame for containing tickets & information. """

            class ScrollFrame(ctk.CTkScrollableFrame):
                """ Scrollable frame for all tickets to be placed within. """

                class TicketObj(ctk.CTkFrame):
                    """ Ticket object for the scroll frame. """

                    def __init__(self, master, name: str, price: float):
                        def _v(s: str, a) -> bool:  # Validate command
                            if int(a) == 1:  # Input
                                return s.isdigit() and int(s) <= remaining_tickets
                            else:  # Deletion
                                return True

                        super().__init__(master, width=450, height=95, fg_color='#F4F4F4', corner_radius=0)
                        self.grid_propagate(False)
                        ctk.CTkLabel(self, text=name, text_color="#434343", font=('Segoe UI', 24)).grid(
                            row=0, column=0, sticky='w', padx=(20, 0), pady=(15, 0))
                        ctk.CTkLabel(self, text=f'${price:.2f}', text_color="#245A23", font=('Segoe UI', 24)).grid(
                            row=1, column=0, sticky='w', padx=(20, 0))
                        # Instance attribute to allow the entry (quantity) to be gathered
                        self.entry = ctk.CTkEntry(self, width=150, height=95, fg_color='#CACACA', corner_radius=0,
                                                  font=('JetBrains Mono NL', 40), text_color='#302265', justify='c',
                                                  validate='key', validatecommand=(master.register(_v), '%P', '%d'))
                        self.entry.place(x=self.winfo_x() + 300, y=0)

                def __init__(self, master):
                    super().__init__(master, width=450, height=310, fg_color='transparent', corner_radius=0)
                    for i, (name, price) in enumerate(tickets):
                        ticket_objects.append(o := self.TicketObj(self, name, price))
                        o.grid(row=i, column=0, pady=(0, 8))

            def __init__(self, master):
                super().__init__(master, width=450, height=350, fg_color='transparent', corner_radius=0)
                self.grid_propagate(False)
                # Header texts
                ctk.CTkLabel(self, text='Ticket', text_color='#000000', font=('JetBrains Mono NL', 16)).grid(
                    row=0, column=0, sticky='w')
                ctk.CTkLabel(self, text='Quantity', text_color='#000000', font=('JetBrains Mono NL', 16)).grid(
                    row=0, column=1)
                # Scroll frame
                self.ScrollFrame(self).grid(row=1, column=0, columnspan=2)

        class Calculate(ctk.CTkFrame):
            def __init__(self, master):
                super().__init__(master, width=450, height=70, fg_color='transparent')
                self.grid_propagate(False), self.grid_anchor('w')
                ctk.CTkLabel(self, text='Total Price:', text_color='#676767', font=('JetBrains Mono NL', 24),
                             height=70).grid(row=0, column=0)

        ctk.set_appearance_mode('system'), super().__init__(fg_color='#FFFCFC')
        self.geometry('500x612'), self.resizable(False, False)
        self.title('Ticket Booking')
        ctk.FontManager().load_font('assets/JetBrainsMonoNL-Bold.ttf')
        ctk.FontManager().load_font('assets/JetBrainsMonoNL-Regular.ttf')
        ctk.FontManager().load_font('assets/segoeui.ttf')
        #
        # Objects and components
        ticket_objects = []  # Holds all ticket objects for calculation
        self.grid_anchor('c'), self.grid_propagate(False)
        ctk.CTkLabel(self, text='Ticket Booking', text_color='#000000', font=('JetBrains Mono NL Bold', 32)).grid(
            row=0, column=0, pady=(50, 25), sticky='w')
        TicketsFrame(self).grid(row=1, column=0)
        Calculate(self).grid(row=2, column=0)
        #
        self.mainloop()
        

if __name__ == '__main__':
    GUI(TICKETS)
