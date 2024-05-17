"""
    Ticket Booking system

    - Jensen Trillo, **v2.0**, 17/05/2024
    - ``Python 3.11.6``
"""
import customtkinter as ctk
from typing import List
TICKETS = [('Child', 5), ('Student/Senior', 10), ('Adult', 15)]
total_tickets = 100


class GUI(ctk.CTk):
    """
        Initializes the GUI.

        :param tickets: :class:`list` [:class:`tuple` (:class:`str` ``name``, :class:`float` ``price``), ...]
    """
    def __init__(self, tickets: List[tuple[str, float]]):
        def _process_order(quantity: int, total: float):  # 'total' will be used for v3.0
            global total_tickets
            if (total_tickets - quantity) <= 0:
                # No remaining tickets
                for w in self.winfo_children():  # Destroy all widgets
                    w.destroy()
                # Place message
                ctk.CTkLabel(self, text='All tickets have been purchased, sorry!', text_color="#cc0000",
                             font=('JetBrains Mono NL', 26), wraplength=450).grid()
            else:
                total_tickets -= quantity
                calculate.c2.configure(text='$0.00')
                remaining.configure(text=f'Tickets Remaining: #{total_tickets}')
                for o in ticket_objects:  # Clear entry
                    o.entry.delete(0, 'end')

        def _get_values() -> List[tuple[int, float]]:
            return [(int(q) if not (q := o.entry.get()).isspace() and q != '' else 0, o.price)
                    for o in ticket_objects]

        def _update():  # Update calculation
            def _err(msg: str):
                calculate.c1.configure(text=msg, text_color="#cc0000", font=('JetBrains Mono NL', 18))
                calculate.c2.configure(text='')
                button.configure(state='disabled', border_color='#979797')
                self._err_state = True

            def _err_reset():
                calculate.c1.configure(text='Total Price:', text_color='#676767', font=('JetBrains Mono NL', 24))
                calculate.c2.configure(text='$0.00')
                button.configure(state='normal', border_color='#40ACE3')
                self._err_state = False

            if self._err_state:
                _err_reset()
            values = _get_values()
            if sum([q for q, _ in values]) > total_tickets:
                _err('Your order exceeds the amount of remaining tickets!')
            else:
                total = sum([p * q for p, q in values])
                calculate.c2.configure(text=f'${total:,.2f}')

        class TicketsFrame(ctk.CTkFrame):
            """ Frame for containing tickets & information. """

            class ScrollFrame(ctk.CTkScrollableFrame):
                """ Scrollable frame for all tickets to be placed within. """

                class TicketObj(ctk.CTkFrame):
                    """ Ticket object for the scroll frame. """

                    def __init__(self, master, name: str, price: float):
                        def _v(s: str, a) -> bool:  # Validate command
                            if int(a) == 1:  # Input
                                return s.isdigit() and int(s) <= total_tickets
                            else:  # Deletion
                                return True

                        super().__init__(master, width=450, height=95, fg_color='#F4F4F4', corner_radius=0)
                        self.grid_propagate(False)
                        self.price = price
                        ctk.CTkLabel(self, text=name, text_color="#434343", font=('Segoe UI', 24)).grid(
                            row=0, column=0, sticky='w', padx=(20, 0), pady=(15, 0))
                        ctk.CTkLabel(self, text=f'${price:.2f}', text_color="#245A23", font=('Segoe UI', 24)).grid(
                            row=1, column=0, sticky='w', padx=(20, 0))
                        # Instance attribute to allow the entry (quantity) to be gathered
                        self.entry = ctk.CTkEntry(self, width=150, height=95, fg_color='#CACACA', corner_radius=0,
                                                  font=('JetBrains Mono NL', 40), text_color='#302265', justify='c',
                                                  validate='key', validatecommand=(master.register(_v), '%P', '%d'))
                        # 1ms to allow .get() to get new value
                        self.entry.bind('<KeyPress>', lambda _: self.after(1, _update))
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
                # Component 1 & 2: text and value respectively
                self.c1 = ctk.CTkLabel(self, text='Total Price:', text_color='#000000', font=('JetBrains Mono NL', 24),
                                       height=70, wraplength=450, justify='left')
                self.c2 = ctk.CTkLabel(self, text='$0.00', text_color='#2D932B', font=('JetBrains Mono NL Bold', 24),
                                       height=70)
                self.c1.grid(row=0, column=0), self.c2.grid(row=0, column=1, padx=(10, 0))

        ctk.set_appearance_mode('system'), super().__init__(fg_color='#FFFCFC')
        self.geometry('500x612'), self.resizable(False, False)
        self.title('Ticket Booking')
        ctk.FontManager().load_font('assets/JetBrainsMonoNL-Bold.ttf')
        ctk.FontManager().load_font('assets/JetBrainsMonoNL-Regular.ttf')
        ctk.FontManager().load_font('assets/segoeui.ttf')
        #
        # ---
        # Objects and components
        ticket_objects = []  # Holds all ticket objects for calculation
        self.grid_anchor('center'), self.grid_propagate(False)
        # Header
        ctk.CTkLabel(self, text='Ticket Booking', text_color='#000000', font=('JetBrains Mono NL Bold', 32)).grid(
            row=0, column=0, pady=(50, 25), sticky='w')
        TicketsFrame(self).grid(row=1, column=0)
        # Calculation frame where values are shown, _err_state used for determining entry errors
        calculate, self._err_state = Calculate(self), False
        calculate.grid(row=2, column=0)
        # noinspection PyUnboundLocalVariable
        remaining = ctk.CTkLabel(self, text=f'Tickets Remaining: #{total_tickets}', text_color='#676767',
                                 font=('Segoe UI', 17))
        remaining.grid(row=3, column=0, sticky='w', pady=(0, 60))
        button = ctk.CTkButton(self, fg_color='transparent', border_color='#40ACE3', border_width=2,
                               text='Place Order', text_color='#40ACE3', width=150, height=40,
                               hover_color='#e4f1f7', font=('Segoe UI', 18),
                               command=lambda: _process_order(sum([q for q, _ in _get_values()]),  # Quantity
                                                              # Get the total price
                                                              float(calculate.c2.cget('text').replace('$', ''))))
        button.place(x=325, y=525)
        # ---
        #
        self.mainloop()
        

if __name__ == '__main__':
    GUI(TICKETS)
