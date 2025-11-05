from tkinter import *
from tkinter import ttk
import pandas as pd

class DataSetViewer:
    def __init__(self, parent=None):
        self.parent = parent

    def create_ui(self):
        # dùng Toplevel thay vì Tk()
        self.win = Toplevel(self.parent) if self.parent else Toplevel()
        self.win.title("Dataset viewer - House Pricing Prediction")
        self.win.geometry("800x600")

        main_panel = PanedWindow(self.win, bg="yellow")
        main_panel.pack(fill=BOTH, expand=True)

        columns = (
            'Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
            'Avg. Area Number of Bedrooms', 'Area Population', 'Price'
        )

        self.tree = ttk.Treeview(main_panel, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=CENTER, width=140, stretch=False)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = ttk.Scrollbar(main_panel, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)  # <-- sửa
        scrollbar.pack(side=RIGHT, fill=Y)                 # <-- sửa

    def show_ui(self):
        # không cần mainloop mới; chỉ “giữ” cửa sổ con
        self.win.grab_set()
        self.win.focus_set()

    def show_data_listview(self, fileName):
        df = pd.read_csv(fileName)

        # đảm bảo các cột tồn tại, và chèn bằng tên cột
        cols = list(self.tree["columns"])
        for _, row in df[cols].iterrows():
            self.tree.insert('', END, values=[row[c] for c in cols])
