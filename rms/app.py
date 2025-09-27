# app.py
import logging
import tkinter as tk
from tkinter import ttk, messagebox
from services import RMS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
log = logging.getLogger("RMS.GUI")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Record Management System (Write-through)")
        self.geometry("1000x620")
        self.rms = RMS(autosave=True)

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


# ----------------- Client Tab -----------------
class ClientTab(ttk.Frame):
    FIELDS = [
        ("Name", 25), ("Address1", 25), ("Address2", 25), ("Address3", 25),
        ("City", 20), ("State", 10), ("Zip", 10), ("Country", 15), ("Phone", 18),
    ]

    def __init__(self, parent, rms: RMS):
        super().__init__(parent)
        self.rms = rms

        frm = ttk.Frame(self)
        frm.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frm, text="ID").grid(row=0, column=0, sticky="w")
        self.ent_id = ttk.Entry(frm, width=10)
        self.ent_id.grid(row=0, column=1, sticky="w")
        self.ent_id.configure(state="readonly")

        ttk.Label(frm, text="Type").grid(row=1, column=0, sticky="w")
        self.ent_type = ttk.Entry(frm, width=10)
        self.ent_type.grid(row=1, column=1, sticky="w")
        self.ent_type.insert(0, "client")
        self.ent_type.configure(state="readonly")

        self.inputs = {}
        base_row = 2
        for i, (label, w) in enumerate(self.FIELDS):
            ttk.Label(frm, text=label).grid(row=base_row + i, column=0, sticky="w")
            e = ttk.Entry(frm, width=w)
            e.grid(row=base_row + i, column=1, sticky="w", pady=2)
            self.inputs[label] = e

        r = base_row + len(self.FIELDS)
        ttk.Button(frm, text="Create", command=self.create).grid(row=r, column=0, pady=8, sticky="w")
        ttk.Button(frm, text="Update", command=self.update).grid(row=r, column=1, pady=8, sticky="w")
        ttk.Button(frm, text="Delete", command=self.delete).grid(row=r, column=2, pady=8, sticky="w")

        ttk.Label(frm, text="Search").grid(row=r + 1, column=0, sticky="w", pady=(10, 0))
        self.ent_search = ttk.Entry(frm, width=25)
        self.ent_search.grid(row=r + 1, column=1, sticky="w", pady=(10, 0))
        ttk.Button(frm, text="Go", command=self.search).grid(row=r + 1, column=2, sticky="w", pady=(10, 0))

        self.list = tk.Listbox(self, width=90)
        self.list.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.list.bind("<<ListboxSelect>>", self.on_select)

        self.refresh()

    def refresh(self, rows=None):
        rows = rows if rows is not None else self.rms.clients
        self.list.delete(0, tk.END)
        for c in rows:
            self.list.insert(
                tk.END,
                f'ID={c["ID"]}  Name={c.get("Name","")}  City={c.get("City","")}  Phone={c.get("Phone","")}'
            )

    def _collect_form(self) -> dict:
        data = {"Type": "client"}
        for k, e in self.inputs.items():
            data[k] = e.get().strip()
        return data

    def _clear_form(self):
        self.ent_id.configure(state="normal")
        self.ent_id.delete(0, tk.END)
        self.ent_id.configure(state="readonly")
        for e in self.inputs.values():
            e.delete(0, tk.END)

    def on_select(self, _evt):
        cur = self.list.curselection()
        if not cur:
            return
        text = self.list.get(cur[0])
        cid = int(text.split()[0].split("=")[1])
        c = self.rms.get_client(cid)
        if not c:
            return
        self.ent_id.configure(state="normal")
        self.ent_id.delete(0, tk.END)
        self.ent_id.insert(0, str(c["ID"]))
        self.ent_id.configure(state="readonly")
        for k, e in self.inputs.items():
            e.delete(0, tk.END)
            e.insert(0, c.get(k, ""))

    def create(self):
        d = self._collect_form()
        if not d["Name"]:
            messagebox.showwarning("Input", "Name is required")
            return
        if not messagebox.askyesno("Confirm", "Create this client?"):
            return
        try:
            row = self.rms.create_client(d)
            log.info("GUI create client ok: %s", row)
            self._clear_form()
            self.refresh()
        except Exception as e:
            log.exception("GUI create client failed")
            messagebox.showerror("Create Client", str(e))

    def update(self):
        cid = self.ent_id.get().strip()
        if not cid:
            messagebox.showwarning("Update", "Please select a row from list")
            return
        try:
            d = self._collect_form()
            row = self.rms.update_client(int(cid), d)
            log.info("GUI update client ok: %s", row)
            self.refresh()
        except Exception as e:
            log.exception("GUI update client failed")
            messagebox.showerror("Update Client", str(e))

    def delete(self):
        cur = self.list.curselection()
        if not cur:
            return
        text = self.list.get(cur[0])
        cid = int(text.split()[0].split("=")[1])
        if not messagebox.askyesno("Confirm", f"Delete client ID={cid}? (linked flights will be removed)"):
            return
        try:
            self.rms.delete_client(cid)
            log.info("GUI delete client ok: id=%s", cid)
            self._clear_form()
            self.refresh()
        except Exception as e:
            log.exception("GUI delete client failed")
            messagebox.showerror("Delete Client", str(e))

    def search(self):
        k = self.ent_search.get()
        rows = self.rms.search_clients(k)
        self.refresh(rows)


# ----------------- Airline Tab（含 Update 与确认） -----------------
class AirlineTab(ttk.Frame):
    def __init__(self, parent, rms: RMS):
        super().__init__(parent)
        self.rms = rms

        frm = ttk.Frame(self)
        frm.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frm, text="ID").grid(row=0, column=0, sticky="w")
        self.ent_id = ttk.Entry(frm, width=10)
        self.ent_id.grid(row=0, column=1, sticky="w")
        self.ent_id.configure(state="readonly")

        ttk.Label(frm, text="CompanyName").grid(row=1, column=0, sticky="w")
        self.ent_name = ttk.Entry(frm, width=30)
        self.ent_name.grid(row=1, column=1, sticky="w")

        ttk.Button(frm, text="Create", command=self.create).grid(row=2, column=0, pady=6)
        ttk.Button(frm, text="Update", command=self.update).grid(row=2, column=1, pady=6)
        ttk.Button(frm, text="Delete", command=self.delete).grid(row=2, column=2, pady=6)

        ttk.Label(frm, text="Search").grid(row=3, column=0, sticky="w")
        self.ent_search = ttk.Entry(frm, width=30)
        self.ent_search.grid(row=3, column=1, sticky="w")
        ttk.Button(frm, text="Go", command=self.search).grid(row=3, column=2, sticky="w")

        self.list = tk.Listbox(self, width=90)
        self.list.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.list.bind("<<ListboxSelect>>", self.on_select)
        self.refresh()

    def refresh(self, rows=None):
        rows = rows if rows is not None else self.rms.airlines
        self.list.delete(0, tk.END)
        for a in rows:
            self.list.insert(tk.END, f'ID={a["ID"]}  CompanyName={a.get("CompanyName","")}')

    def on_select(self, _evt):
        cur = self.list.curselection()
        if not cur:
            return
        text = self.list.get(cur[0])
        aid = int(text.split()[0].split("=")[1])
        a = self.rms.get_airline(aid)
        if not a:
            return
        self.ent_id.configure(state="normal")
        self.ent_id.delete(0, tk.END)
        self.ent_id.insert(0, str(a["ID"]))
        self.ent_id.configure(state="readonly")
        self.ent_name.delete(0, tk.END)
        self.ent_name.insert(0, a.get("CompanyName", ""))

    def create(self):
        name = self.ent_name.get().strip()
        if not name:
            messagebox.showwarning("Input", "CompanyName required")
            return
        if not messagebox.askyesno("Confirm", "Create this airline?"):
            return
        try:
            row = self.rms.create_airline({"Type": "airline", "CompanyName": name})
            log.info("GUI create airline ok: %s", row)
            self.ent_name.delete(0, tk.END)
            self.refresh()
        except Exception as e:
            log.exception("GUI create airline failed")
            messagebox.showerror("Create Airline", str(e))

    def update(self):
        aid = self.ent_id.get().strip()
        if not aid:
            messagebox.showwarning("Update", "Please select a row from list")
            return
        try:
            row = self.rms.update_airline(int(aid), {"CompanyName": self.ent_name.get().strip(), "Type": "airline"})
            log.info("GUI update airline ok: %s", row)
            self.refresh()
        except Exception as e:
            log.exception("GUI update airline failed")
            messagebox.showerror("Update Airline", str(e))

    def delete(self):
        cur = self.list.curselection()
        if not cur:
            return
        text = self.list.get(cur[0])
        aid = int(text.split()[0].split("=")[1])
        if not messagebox.askyesno("Confirm", f"Delete airline ID={aid}? (linked flights will be removed)"):
            return
        try:
            self.rms.delete_airline(aid)
            log.info("GUI delete airline ok: id=%s", aid)
            self.ent_id.configure(state="normal")
            self.ent_id.delete(0, tk.END)
            self.ent_id.configure(state="readonly")
            self.ent_name.delete(0, tk.END)
            self.refresh()
        except Exception as e:
            log.exception("GUI delete airline failed")
            messagebox.showerror("Delete Airline", str(e))

    def search(self):
        k = self.ent_search.get()
        rows = self.rms.search_airlines(k)
        self.refresh(rows)


# ----------------- Flight Tab（含 ID、Update、确认） -----------------
class FlightTab(ttk.Frame):
    def __init__(self, parent, rms: RMS):
        super().__init__(parent)
        self.rms = rms

        frm = ttk.Frame(self)
        frm.pack(side="left", fill="y", padx=10, pady=10)

        ttk.Label(frm, text="ID").grid(row=0, column=0, sticky="w")
        self.ent_id = ttk.Entry(frm, width=10)
        self.ent_id.grid(row=0, column=1, sticky="w")
        self.ent_id.configure(state="readonly")

        ttk.Label(frm, text="Client_ID").grid(row=1, column=0, sticky="w")
        self.ent_cid = ttk.Entry(frm, width=10)
        self.ent_cid.grid(row=1, column=1, sticky="w")

        ttk.Label(frm, text="Airline_ID").grid(row=2, column=0, sticky="w")
        self.ent_aid = ttk.Entry(frm, width=10)
        self.ent_aid.grid(row=2, column=1, sticky="w")

        ttk.Label(frm, text="Date(YYYY-MM-DD or ISO)").grid(row=3, column=0, sticky="w")
        self.ent_date = ttk.Entry(frm, width=20)
        self.ent_date.grid(row=3, column=1, sticky="w")

        ttk.Label(frm, text="StartCity").grid(row=4, column=0, sticky="w")
        self.ent_sc = ttk.Entry(frm, width=18)
        self.ent_sc.grid(row=4, column=1, sticky="w")

        ttk.Label(frm, text="EndCity").grid(row=5, column=0, sticky="w")
        self.ent_ec = ttk.Entry(frm, width=18)
        self.ent_ec.grid(row=5, column=1, sticky="w")

        ttk.Button(frm, text="Create", command=self.create).grid(row=6, column=0, pady=8)
        ttk.Button(frm, text="Update", command=self.update).grid(row=6, column=1, pady=8)
        ttk.Button(frm, text="Delete", command=self.delete).grid(row=6, column=2, pady=8)

        self.list = tk.Listbox(self, width=100)
        self.list.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.list.bind("<<ListboxSelect>>", self.on_select)

        self.refresh()

    def refresh(self):
        self.list.delete(0, tk.END)
        for f in self.rms.flights:
            self.list.insert(
                tk.END,
                f'ID={f["ID"]}  Client_ID={f["Client_ID"]} Airline_ID={f["Airline_ID"]} '
                f'Date={f.get("Date","")} {f.get("StartCity","")}->{f.get("EndCity","")}'
            )

    def on_select(self, _evt):
        cur = self.list.curselection()
        if not cur:
            return
        text = self.list.get(cur[0])
        fid = int(text.split()[0].split("=")[1])
        f = self.rms.get_flight(fid)
        if not f:
            return
        self.ent_id.configure(state="normal")
        self.ent_id.delete(0, tk.END)
        self.ent_id.insert(0, str(f["ID"]))
        self.ent_id.configure(state="readonly")
        self.ent_cid.delete(0, tk.END)
        self.ent_cid.insert(0, str(f["Client_ID"]))
        self.ent_aid.delete(0, tk.END)
        self.ent_aid.insert(0, str(f["Airline_ID"]))
        self.ent_date.delete(0, tk.END)
        self.ent_date.insert(0, f.get("Date", ""))
        self.ent_sc.delete(0, tk.END)
        self.ent_sc.insert(0, f.get("StartCity", ""))
        self.ent_ec.delete(0, tk.END)
        self.ent_ec.insert(0, f.get("EndCity", ""))

    def _collect(self) -> dict:
        return {
            "Client_ID": int(self.ent_cid.get().strip()),
            "Airline_ID": int(self.ent_aid.get().strip()),
            "Date": self.ent_date.get().strip(),
            "StartCity": self.ent_sc.get().strip(),
            "EndCity": self.ent_ec.get().strip(),
        }

    def _clear(self):
        self.ent_id.configure(state="normal")
        self.ent_id.delete(0, tk.END)
        self.ent_id.configure(state="readonly")
        for e in (self.ent_cid, self.ent_aid, self.ent_date, self.ent_sc, self.ent_ec):
            e.delete(0, tk.END)

    def create(self):
        if not messagebox.askyesno("Confirm", "Create this flight?"):
            return
        try:
            row = self.rms.create_flight(self._collect())
            log.info("GUI create flight ok: %s", row)
            self._clear()
            self.refresh()
        except Exception as e:
            log.exception("GUI create flight failed")
            messagebox.showerror("Create Flight", str(e))

    def update(self):
        fid = self.ent_id.get().strip()
        if not fid:
            messagebox.showwarning("Update", "Please select a row from list")
            return
        try:
            row = self.rms.update_flight(int(fid), self._collect())
            log.info("GUI update flight ok: %s", row)
            self.refresh()
        except Exception as e:
            log.exception("GUI update flight failed")
            messagebox.showerror("Update Flight", str(e))

    def delete(self):
        cur = self.list.curselection()
        if not cur:
            return
        text = self.list.get(cur[0])
        fid = int(text.split()[0].split("=")[1])
        if not messagebox.askyesno("Confirm", f"Delete flight ID={fid}?"):
            return
        try:
            self.rms.delete_flight(fid)
            log.info("GUI delete flight ok: id=%s", fid)
            self._clear()
            self.refresh()
        except Exception as e:
            log.exception("GUI delete flight failed")
            messagebox.showerror("Delete Flight", str(e))


if __name__ == "__main__":
    App().mainloop()
