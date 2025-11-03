import tkinter as tk
from tkinter import ttk
from datetime import date

PRIMARY_COLOR = "#EABE0D"
DARK_COLOR = "#4D4D4D"
WHITE = "#FFFFFF"
FONT = ("Segoe UI", 10, "bold")


class TitleBlock(ttk.Frame):
    def __init__(self, parent, company="", content="", project="", made_by="", **kwargs):
        super().__init__(parent, **kwargs)

        today = date.today().strftime("%Y-%m-%d")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TitleBlock.TFrame", background=WHITE, borderwidth=2, relief="groove")
        style.configure("TitleBlock.TLabel", background=WHITE, foreground=DARK_COLOR, font=FONT)
        style.configure("TitleBlock.TEntry", font=FONT, # Background inside entry
                borderwidth=0,
                relief="ridge",
                padding=5)

        self.configure(style="TitleBlock.TFrame", padding=5)

        # Variables (editable fields)
        self.company_var = tk.StringVar(value=company)
        self.content_var = tk.StringVar(value=content)
        self.project_var = tk.StringVar(value=project)
        self.date_var = tk.StringVar(value=today)
        self.made_by_var = tk.StringVar(value=made_by)

        ttk.Label(self, text="Company: ", style="TitleBlock.TLabel", anchor="e", width=12)\
            .grid(row=1, column=0, sticky="e", padx=4, pady=2)
        ttk.Entry(self, textvariable=self.company_var, width=80)\
            .grid(row=1, column=1, sticky="w", padx=4, pady=2)
        
        # Layout
        self._add_row("Content:", self.content_var, 0)
        self._add_row("Project:", self.project_var, 1)
        self._add_row("Date:", self.date_var, 2)
        self._add_row("Made by:", self.made_by_var, 3)


    def _add_row(self, label, var, row):
        ttk.Label(self, text=label, style="TitleBlock.TLabel", anchor="e", width=12)\
            .grid(row=row, column=2, sticky="e", padx=4, pady=2)
        ttk.Entry(self, textvariable=var, width=80, style="TitleBlock.TEntry")\
            .grid(row=row, column=3, sticky="w", padx=4, pady=2)



# Test the widget standalone
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Title Block Example")

    tb = TitleBlock(
        root,
        company="Company Name",
        content="Sensor Wiring Diagram",
        project="Weather Station CR1000X",
        made_by="CS"
    )
    tb.pack(padx=20, pady=20, fill="x")

    root.mainloop()
