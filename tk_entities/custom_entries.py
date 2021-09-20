import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
from consts import *


class AutocompleteEntryWithListbox(tk.Entry):

    def __init__(self, root, list_of_values, start_x, start_y, entry_width, listbox_width, font=('Calibri', 13)):
        frame = tk.Frame(root)
        super().__init__(frame, font=font, width=entry_width)
        self.root = root
        self.frame = tk.Frame(root)
        self.list_box = None
        self.list_of_values = list_of_values
        self.hints = list_of_values
        self.listbox_width = listbox_width
        self.font = font
        self.start_x = start_x
        self.start_y = start_y
        self.extension_flag = False
        self.bind('<KeyRelease>', self.autocomplete)
        self.ext_btn = tk.Button(frame, text='\u02c5', bg='white', borderwidth=1, command=self.roll_up_or_down_list_values)
        self.pack(side=tk.LEFT)
        self.ext_btn.pack(side=tk.LEFT)
        frame.place(x=start_x, y=start_y)

    def roll_up_or_down_list_values(self):
        self.roll_up_for_not_related_entry(10)

    def roll_up_for_not_related_entry(self, listbox_height):
        if not self.extension_flag:
            listbox_font = (self.font[0], self.font[1]-1)
            self.list_box = tk.Listbox(self.root, width=self.listbox_width, height=listbox_height, font=listbox_font)
            self.list_box.bind('<<ListboxSelect>>', self.fill_out)
            self.list_box.place(x=self.start_x, y=self.start_y + 26)
            self.extension_flag = True
            self.update_listbox(self.list_of_values)

        else:
            if self.list_box is not None:
                self.list_box.delete(0, tk.END)
                self.list_box.destroy()
                self.list_box = None
                self.extension_flag = False

    def update_listbox(self, values):
        if self.list_box is not None:
            self.list_box.delete(0, tk.END)
            for item in values:
                self.list_box.insert(tk.END, item)

    def fill_out(self, event):
        self.delete(0, tk.END)
        self.insert(0, self.list_box.get(tk.ANCHOR))

    def autocomplete(self, event):
        typed = self.get().lower()
        if typed == '':
            self.hints = self.list_of_values
        else:
            self.hints = [item for item in self.list_of_values if item.lower().startswith(typed)]

        self.update_listbox(self.hints)


class RelatedEntryWithListbox(AutocompleteEntryWithListbox):
    def __init__(self, root, list_of_values, start_x, start_y, related_entry, dict_of_associations, entry_width,
                 listbox_width, font=('Calibri', 13)):
        super().__init__(root, list_of_values, start_x, start_y, entry_width, listbox_width, font)
        self.related_entry = related_entry
        self.dict_of_associations = dict_of_associations

    def roll_up_or_down_list_values(self):
        related_entry_value = self.related_entry.get()
        if related_entry_value != '':
            list_of_values = self.dict_of_associations[related_entry_value]
            if list_of_values is not None and len(list_of_values) != 0:
                self.list_of_values = list_of_values
        self.roll_up_for_not_related_entry(len(self.list_of_values) if len(self.list_of_values) < 10 else 10)


class ToggledFrame(tk.Frame):

    def __init__(self, parent, text="", frame_font=font_cal_14, *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        ttk.Label(self.title_frame, text=text, font=frame_font).pack(side=tk.LEFT, fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='\u25bc', command=self.toggle,
                                             variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side=tk.LEFT)

        self.sub_frame = tk.Frame(self, borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill='both')
            self.toggle_button.configure(text='\u25b2')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='\u25bc')


class CheckBtnWithDateEntry(tk.Checkbutton):
    def __init__(self, root, text, row_index: str, col_index: str, width_entry,
                 font_entry=font_cal_10, font_checkbtn=font_cal_11):
        self.checked = tk.IntVar()
        self.frame = tk.Frame(root)
        self.row_num = None if row_index == '' else int(row_index)
        self.col_num = None if col_index == '' else int(col_index)
        super().__init__(self.frame, text=text, variable=self.checked, font=font_checkbtn)
        self.date_entry = tk.Entry(self.frame, width=width_entry, font=font_entry)
        self.frame.pack(fill='both', padx=2)
        self.pack(side=tk.LEFT)
        self.date_entry.pack(side=tk.LEFT)
        # self.place(x=start_x_checkbtn, y=start_y)
        # self.date_entry.place(x=start_x_entry, y=start_y+4)

    def get_date(self) -> str:
        date_str = self.date_entry.get()
        try:
            datetime.datetime.strptime(date_str, day_month_date_format)
        except ValueError:
            messagebox.showerror("Error", wrong_date)
            raise ValueError(wrong_date)
        return date_str

    def set_date(self, date: str):
        self.date_entry.delete(0, 'end')
        self.date_entry.insert(0, date)

    def is_checked(self) -> bool:
        return bool(self.checked.get())

    def set_checked(self, checked: bool):
        self.checked.set(int(checked))

