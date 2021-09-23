import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
from consts import *


class AutocompleteEntryWithListbox(tk.Entry):

    def __init__(self, root, list_of_values, entry_width,
                 entry_font=('Calibri', 13), listbox_font=('Calibri', 12)):
        self.full_frame = tk.Frame(root)
        entry_frame = tk.Frame(self.full_frame)
        super().__init__(entry_frame, font=entry_font, width=entry_width)
        self.root = root
        self.list_box = None
        self.list_of_values = list_of_values
        self.hints = list_of_values
        self.listbox_font = listbox_font
        self.extension_flag = False
        self.bind('<KeyRelease>', self.autocomplete)
        self.ext_btn = tk.Button(entry_frame, text='\u02c5', bg='white', borderwidth=1, command=self.roll_up_or_down_list_values)
        self.pack(side=tk.LEFT)
        self.ext_btn.pack(side=tk.LEFT)
        entry_frame.pack()

    def roll_up_or_down_list_values(self):
        self.roll_up_for_not_related_entry(10)

    def roll_up_for_not_related_entry(self, listbox_height):
        if not self.extension_flag:
            self.list_box = tk.Listbox(self.full_frame, height=listbox_height, font=self.listbox_font)
            self.list_box.bind('<<ListboxSelect>>', self.fill_out)
            self.list_box.pack(fill='both')
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

    def place(self, x, y):
        self.full_frame.place(x=x, y=y)


class RelatedEntryWithListbox(AutocompleteEntryWithListbox):
    def __init__(self, root, list_of_values, related_entry, dict_of_associations, entry_width,
                 entry_font=('Calibri', 13), listbox_font=('Calibri', 12)):
        super().__init__(root, list_of_values, entry_width, entry_font, listbox_font)
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
    def __init__(self, root, text, row_index: str, col_index: str, entry_width,
                 entry_font=font_cal_10, checkbtn_font=font_cal_11):
        self.checked = tk.IntVar()
        self.frame = tk.Frame(root)
        self.row_num = None if row_index == '' else int(row_index)
        self.col_num = None if col_index == '' else int(col_index)
        super().__init__(self.frame, text=text, variable=self.checked, font=checkbtn_font)
        self.date_entry = tk.Entry(self.frame, width=entry_width, font=entry_font)
        self.frame.pack(fill='both', padx=2)
        self.pack(side=tk.LEFT)
        self.date_entry.pack(side=tk.LEFT)

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

