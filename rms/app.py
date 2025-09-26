# app.py
import tkinter as tk
from tkinter import ttk, messagebox
from services import RMS


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Record Management System (Minimal)")
        self.geometry("720x420")
        self.rms = RMS()

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True)

        self.client_tab = ClientTab(nb, self.rms)
        self.airline_tab = AirlineTab(nb, self.rms)
        self.flight_tab = FlightTab(nb, self.rms)

        nb.add(self.client_tab, text="Clients")
        nb.add(self.airline_tab, text="Airlines")
        nb.add(self.flight_tab, text="Flights")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        try:
            self.rms.save()
        except Exception as e:
            messagebox.showerror("Save error", str(e))
        self.destroy()


class ClientTab(ttk.Frame):
    def __init__(self, parent, rms: RMS):
        super().__init__(parent)
        self.rms = rms

        frm = ttk.Frame(self)
        frm.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frm, text="Name").grid(row=0, column=0, sticky="w")
        self.ent_name = ttk.Entry(frm, width=25)
        self.ent_name.grid(row=0, column=1)

        ttk.Button(frm, text="Create", command=self.create).grid(row=1, column=0)
        ttk.Button(frm, text="Delete", command=self.delete).grid(row=1, column=1)

        ttk.Label(frm, text="Search").grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.ent_search = ttk.Entry(frm, width=25)
        self.ent_search.grid(row=2, column=1)
        ttk.Button(frm, text="Go", command=self.search).grid(row=2, column=2)

        self.list = tk.Listbox(self, width=60)
        self.list.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.refresh()

    def refresh(self, rows=None):
        rows = rows if rows is not None else self.rms.clients
        self.list.delete(0, tk.END)
        for c in rows:
            self.list.insert(tk.END, f'ID={c["ID"]}  Name={c.get("Name","")}')

    def create(self):
        name = self.ent_name.get().strip()
        if not name:
            messagebox.showwarning("Input", "Name required")
            return
        self.rms.create_client({"Type": "client", "Name": name})
        self.refresh()

    def delete(self):
        cur = self.list.curselection()
        if not cur:
            return
        # 取出选中行的 ID
        text = self.list.get(cur[0])
        cid = int(text.split()[0].split("=")[1])
        self.rms.delete_client(cid)
        self.refresh()

    def search(self):
        k = self.ent_search.get()
        rows = self.rms.search_clients(k)
        self.refresh(rows)


class AirlineTab(ttk.Frame):
    def __init__(self, parent, rms: RMS):
        super().__init__(parent)
        self.rms = rms

        frm = ttk.Frame(self)
        frm.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frm, text="Company Name").grid(row=0, column=0, sticky="w")
        self.ent_name = ttk.Entry(frm, width=25)
        self.ent_name.grid(row=0, column=1)

        ttk.Button(frm, text="Create", command=self.create).grid(row=1, column=0)
        ttk.Button(frm, text="Delete", command=self.delete).grid(row=1, column=1)

        ttk.Label(frm, text="Search").grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.ent_search = ttk.Entry(frm, width=25)
        self.ent_search.grid(row=2, column=1)
        ttk.Button(frm, text="Go", command=self.search).grid(row=2, column=2)

        self.list = tk.Listbox(self, width=60)
        self.list.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.refresh()

    def refresh(self, rows=None):
        rows = rows if rows is not None else self.rms.airlines
        self.list.delete(0, tk.END)
        for a in rows:
            self.list.insert(tk.END, f'ID={a["ID"]}  Company={a.get("CompanyName","")}')

    def create(self):
        name = self.ent_name.get().strip()
        if not name:
            messagebox.showwarning("Input", "Company Name required")
            return
        self.rms.create_airline({"Type": "airline", "CompanyName": name})
        self.refresh()

    def delete(self):
        cur = self.list.curselection()
        if not cur:
            return
        text = self.list.get(cur[0])
        aid = int(text.split()[0].split("=")[1])
        self.rms.delete_airline(aid)
        self.refresh()

    def search(self):
        k = self.ent_search.get()
        rows = self.rms.search_airlines(k)
        self.refresh(rows)


class FlightTab(ttk.Frame):
    def __init__(self, parent, rms: RMS):
        super().__init__(parent)
        self.rms = rms

        frm = ttk.Frame(self)
        frm.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frm, text="Client_ID").grid(row=0, column=0, sticky="w")
        ttk.Label(frm, text="Airline_ID").grid(row=1, column=0, sticky="w")
        ttk.Label(frm, text="Date (YYYY-MM-DD)").grid(row=2, column=0, sticky="w")
        ttk.Label(frm, text="Start City").grid(row=3, column=0, sticky="w")
        ttk.Label(frm, text="End City").grid(row=4, column=0, sticky="w")

        self.ent_cid = ttk.Entry(frm, width=20)
        self.ent_aid = ttk.Entry(frm, width=20)
        self.ent_date = ttk.Entry(frm, width=20)
        self.ent_s = ttk.Entry(frm, width=20)
        self.ent_e = ttk.Entry(frm, width=20)
        self.ent_cid.grid(row=0, column=1)
        self.ent_aid.grid(row=1, column=1)
        self.ent_date.grid(row=2, column=1)
        self.ent_s.grid(row=3, column=1)
        self.ent_e.grid(row=4, column=1)

        ttk.Button(frm, text="Create", command=self.create).grid(row=5, column=0)
        ttk.Button(frm, text="Delete Selected", command=self.delete).grid(row=5, column=1)

        self.list = tk.Listbox(self, width=80)
        self.list.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.refresh()

    def refresh(self):
        self.list.delete(0, tk.END)
        for i, f in enumerate(self.rms.flights):
            self.list.insert(
                tk.END,
                f'{i:03d}  Client={f["Client_ID"]}  Airline={f["Airline_ID"]}  '
                f'Date={f.get("Date","")}  {f.get("StartCity","")} -> {f.get("EndCity","")}'
            )

    def create(self):
        try:
            d = {
                "Client_ID": int(self.ent_cid.get()),
                "Airline_ID": int(self.ent_aid.get()),
                "Date": self.ent_date.get().strip(),
                "StartCity": self.ent_s.get().strip(),
                "EndCity": self.ent_e.get().strip(),
            }
            self.rms.create_flight(d)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Create Flight", str(e))

    def delete(self):
        cur = self.list.curselection()
        if not cur:
            return
        idx = int(self.list.get(cur[0]).split()[0])
        try:
            self.rms.delete_flight(idx)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Delete Flight", str(e))


if __name__ == "__main__":
    App().mainloop()
