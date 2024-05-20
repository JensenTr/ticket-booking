"""
    Ticket Booking system

    - Jensen Trillo, **v3.0**, 21/05/2024
    - ``Python 3.11.6``
"""
import customtkinter as ctk
from ujson import dumps, loads
from typing import List
from signal import signal, SIGINT, SIGTERM
from atexit import register as exit_register
from datetime import datetime

# Tickets: list[tuple(name, price)]
TICKETS = [('Child', 5), ('Student/Senior', 10), ('Adult', 15)]
JSON_PATH = 'data.json'
TOTAL_TICKETS = 100  # Total tickets by default

ctk.set_appearance_mode('system')
ctk.FontManager().load_font('assets/JetBrainsMonoNL-Bold.ttf')
ctk.FontManager().load_font('assets/JetBrainsMonoNL-Regular.ttf')
ctk.FontManager().load_font('assets/segoeui.ttf')


class GUI(ctk.CTk):
    """
        Initializes the GUI.

        :param tickets: :class:`list` [:class:`tuple` (:class:`str` ``name``, :class:`float` ``price``), ...]
    """
    @staticmethod
    def __read_json() -> dict:
        with open(JSON_PATH, 'rb') as f:
            json = loads(f.read())
            return json

    @staticmethod
    def __write_json(obj: dict):
        with open(JSON_PATH, 'w') as f:
            f.write(dumps(obj, indent=4))

    def __kill_handler(self, *_):
        self.quit()
        self.__write_json(self.json)

    def __init__(self, tickets: List[tuple[str, float]]):
        try:
            self.json = self.__read_json()
        except FileNotFoundError:  # Set default JSON
            self.json = {
                'tickets': TOTAL_TICKETS,
                'orders': {}
            }
            self.__write_json(self.json)

        def no_tickets_widgets():
            # No remaining tickets
            for w in self.winfo_children():  # Destroy all widgets
                w.destroy()
            # Place message
            ctk.CTkLabel(self, text='All tickets have been purchased, sorry!', text_color="#cc0000",
                         font=('JetBrains Mono NL', 26), wraplength=450).grid()

        def process_order(data: list, quantity: int, total: float):  # 'total' will be used for v3.0
            if (self.json['tickets'] - quantity) <= 0:  # No tickets remaining
                no_tickets_widgets()
                self.json['tickets'] = 0
            else:
                self.json['tickets'] -= quantity
                # Save order to JSON
                self.json['orders'][date := datetime.now().strftime('%a %d %b, %I:%M %p')] = {n: {
                    'quantity': q,
                    'price_per_ticket': p,
                    'total': q * p
                } for q, p, n in data if q > 0}
                self.json['orders'][date]['total'] = total
                #
                calculate.c2.configure(text='$0.00')  # Reset price
                # Change remaining tickets
                remaining.configure(text=f'Tickets Remaining: #{self.json["tickets"]}')
                for o in ticket_objects:  # Clear entry
                    o.entry.delete(0, 'end')

        def get_values() -> List[tuple[int, float]]:
            return [(int(q) if not (q := o.entry.get()).isspace() and q != '' else 0, o.price, o.name)
                    for o in ticket_objects]

        def update():  # Update calculation
            def err(msg: str):
                calculate.c1.configure(text=msg, text_color="#cc0000", font=('JetBrains Mono NL', 18))
                calculate.c2.configure(text='')
                button.configure(state='disabled', border_color='#979797')
                self._err_state = True

            def err_reset():
                calculate.c1.configure(text='Total Price:', text_color='#676767', font=('JetBrains Mono NL', 24))
                calculate.c2.configure(text='$0.00')
                button.configure(state='normal', border_color='#40ACE3')
                self._err_state = False

            if self._err_state:
                err_reset()
            values = get_values()
            if (total_q := sum([q for q, _, _ in values])) > self.json['tickets']:
                err('Your order exceeds the amount of remaining tickets!')
            elif total_q == 0:  # Gray out button on 0 quantity
                button.configure(state='disabled', border_color='#979797')
            else:
                button.configure(state='normal', border_color='#40ACE3')
                calculate.c2.configure(text=f'${sum([p * q for p, q, _ in values]):,.2f}')

        class TicketsFrame(ctk.CTkFrame):
            """ Frame for containing tickets & information. """
            def __init__(self, master):
                class TicketObj(ctk.CTkFrame):
                    """ Ticket object for the scroll frame. """
                    def __init__(self, _master, name: str, price: float):
                        def _v(s: str, a) -> bool:  # Validate command
                            if int(a) == 1:  # Input
                                return s.isdigit() and int(s) <= master.json['tickets']
                            else:  # Deletion
                                return True

                        super().__init__(_master, 450, 95, 0, fg_color='#F4F4F4')
                        self.grid_propagate(False)
                        self.name, self.price = name, price
                        ctk.CTkLabel(self, text=name, text_color="#434343", font=('Segoe UI', 24)).grid(
                            row=0, column=0, sticky='w', padx=(20, 0), pady=(15, 0))
                        ctk.CTkLabel(self, text=f'${price:.2f}', text_color="#245A23", font=('Segoe UI', 24)).grid(
                            row=1, column=0, sticky='w', padx=(20, 0))
                        # Instance attribute to allow the entry (quantity) to be gathered
                        self.entry = ctk.CTkEntry(self, width=150, height=95, fg_color='#CACACA', corner_radius=0,
                                                  font=('JetBrains Mono NL', 40), text_color='#302265', justify='c',
                                                  validate='key', validatecommand=(_master.register(_v), '%P', '%d'))
                        # 1ms to allow .get() to get new value
                        self.entry.bind('<KeyPress>', lambda _: self.after(1, update))
                        self.entry.place(x=self.winfo_x() + 300, y=0)

                class ScrollFrame(ctk.CTkScrollableFrame):
                    """ Scrollable frame for all tickets to be placed within. """
                    def __init__(self, _master):
                        super().__init__(_master, 450, 310, 0, fg_color='transparent')
                        for i, (name, price) in enumerate(tickets):
                            ticket_objects.append(o := TicketObj(self, name, price))
                            o.grid(row=i, column=0, pady=(0, 8))

                super().__init__(master, 450, 350, 0, fg_color='transparent')
                self.grid_propagate(False)
                # Header texts
                ctk.CTkLabel(self, text='Ticket', text_color='#000000', font=('JetBrains Mono NL', 16)).grid(
                    row=0, column=0, sticky='w')
                ctk.CTkLabel(self, text='Quantity', text_color='#000000', font=('JetBrains Mono NL', 16)).grid(
                    row=0, column=1)
                # Scroll frame
                ScrollFrame(self).grid(row=1, column=0, columnspan=2)

        class Calculate(ctk.CTkFrame):
            def __init__(self, master):
                super().__init__(master, 450, 70, fg_color='transparent')
                self.grid_propagate(False), self.grid_anchor('w')
                # Component 1 & 2: text and value respectively
                self.c1 = ctk.CTkLabel(self, text='Total Price:', text_color='#000000', font=('JetBrains Mono NL', 24),
                                       height=70, wraplength=450, justify='left')
                self.c2 = ctk.CTkLabel(self, text='$0.00', text_color='#2D932B', font=('JetBrains Mono NL Bold', 24),
                                       height=70)
                self.c1.grid(row=0, column=0), self.c2.grid(row=0, column=1, padx=(10, 0))

        super().__init__(fg_color='#FFFCFC')
        signal(SIGINT, self.__kill_handler), signal(SIGTERM, self.__kill_handler)
        exit_register(self.__kill_handler)
        self.geometry('500x612'), self.resizable(False, False), self.title('Ticket Booking')
        self.grid_anchor('center'), self.grid_propagate(False)
        #
        # ---
        # Objects and components
        if self.json['tickets'] <= 0:  # On startup, if tickets <= 0 display error screen
            no_tickets_widgets()
        else:
            ticket_objects = []  # Holds all ticket objects for calculation
            # Header
            ctk.CTkLabel(self, text='Ticket Booking', text_color='#000000', font=('JetBrains Mono NL Bold', 32)).grid(
                row=0, column=0, pady=(50, 25), sticky='w')
            TicketsFrame(self).grid(row=1, column=0)
            # Calculation frame where values are shown, _err_state used for determining entry errors
            calculate, self._err_state = Calculate(self), False
            calculate.grid(row=2, column=0)
            remaining = ctk.CTkLabel(self, text=f'Tickets Remaining: #{self.json["tickets"]}', text_color='#676767',
                                     font=('Segoe UI', 17))
            remaining.grid(row=3, column=0, sticky='w', pady=(0, 60))
            button = ctk.CTkButton(self, 150, 40, fg_color='transparent', border_color='#979797', border_width=2,
                                   text='Place Order', text_color='#40ACE3', hover_color='#e4f1f7',
                                   font=('Segoe UI', 18), state='disabled',
                                   command=lambda: process_order(data := get_values(),
                                                                 sum([q for q, _, _ in data]),  # Quantity
                                                                 # Get the total price
                                                                 float(calculate.c2.cget('text').replace('$', ''))))
            button.place(x=325, y=525)
        # ---
        self.mainloop()
        

if __name__ == '__main__':
    GUI(TICKETS)
