# app.py
import logging
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from services import RMS

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Record Management System")
        self.geometry("1400x750")
        self.resizable(True, True)
        
        self.rms = RMS()

        nb = ttk.Notebook(self)
        self.tab_clients = ttk.Frame(nb)
        self.tab_airlines = ttk.Frame(nb)
        self.tab_flights = ttk.Frame(nb)
        nb.add(self.tab_clients, text="Clients Record")
        nb.add(self.tab_airlines, text="Airlines Record")
        nb.add(self.tab_flights, text="Flights Record")
        nb.pack(fill="both", expand=True)

        # Style: grey read-only
        self.style = ttk.Style(self)
        self.style.configure("Gray.TEntry", foreground="#666")

        self.build_clients_tab()
        self.build_airlines_tab()
        self.build_flights_tab()

        self.refresh_clients()
        self.refresh_airlines()
        self.refresh_flights()

    # ==============================================
    # Clients Tab
    # ==============================================
    def build_clients_tab(self):
        f = self.tab_clients

        # Left and Right Panels, Left if fixed, Right expands
        left = ttk.Frame(f, width=420)
        left.pack(side="left", fill="y", padx=(8,4), pady=8)
        left.pack_propagate(False)

        right = ttk.Frame(f)
        right.pack(side="left", fill="both", expand=True, padx=(4,8), pady=8)

        # Left Panel:

        form = ttk.Frame(left)
        form.pack(fill="y", expand=False)
        
        # Row 0: Client ID
        ttk.Label(form, text="Client ID").grid(row=0, column=0, sticky="w", padx=1, pady=4)
        self.ent_client_id = ttk.Entry(form, width=22, state="readonly", style="Gray.TEntry")
        self.ent_client_id.grid(row=0, column=1, sticky="w", padx=1, pady=4)

        #Row 1: Record Type
        ttk.Label(form, text="Record Type").grid(row=1, column=0, sticky="w", padx=1, pady=4)
        self.ent_client_type = ttk.Entry(form, width=22, state="readonly", style="Gray.TEntry")
        self.ent_client_type.grid(row=1, column=1, sticky="w", padx=1, pady=4)
        self.ent_client_type_var = tk.StringVar(value="client")
        self.ent_client_type.configure(textvariable=self.ent_client_type_var)

        # Row 2: Name
        ttk.Label(form, text="Name*").grid(row=2, column=0, sticky="w", padx=1, pady=4)
        self.ent_name = ttk.Entry(form, width=22)
        self.ent_name.grid(row=2, column=1, sticky="w", padx=1, pady=4)

        # Row 3: Country
        ttk.Label(form, text="Country*").grid(row=3, column=0, sticky="w", padx=1, pady=4)
        self.cmb_country = ttk.Combobox(form, width=21, values=self.rms.list_countries(), state="readonly")
        self.cmb_country.grid(row=3, column=1, sticky="w", padx=1, pady=4)

        # Row 4: Address Line 1
        ttk.Label(form, text="Address Line 1*").grid(row=4, column=0, sticky="w", padx=1, pady=4)
        self.ent_addr1 = ttk.Entry(form, width=22)
        self.ent_addr1.grid(row=4, column=1, padx=1, sticky="w", pady=4)

        # Row 5: Address Line 2
        ttk.Label(form, text="Address Line 2").grid(row=5, column=0, sticky="w", padx=1, pady=4)
        self.ent_addr2 = ttk.Entry(form, width=22)
        self.ent_addr2.grid(row=5, column=1, sticky="w", padx=1, pady=4)

        # Row 6: Address Line 3
        ttk.Label(form, text="Address Line 3").grid(row=6, column=0, sticky="w", padx=1, pady=4)
        self.ent_addr3 = ttk.Entry(form, width=22)
        self.ent_addr3.grid(row=6, column=1, sticky="w", padx=1, pady=4)

        # Row 7: City
        ttk.Label(form, text="City*").grid(row=7, column=0, sticky="w", padx=1, pady=4)
        self.cmb_city = ttk.Combobox(form, width=21, values=self.rms.list_cities(), state="readonly")
        self.cmb_city.grid(row=7, column=1, sticky="w", padx=1, pady=4)

        # Row 8: State/County
        ttk.Label(form, text="State/County*").grid(row=8, column=0, sticky="w", padx=1, pady=4)
        self.ent_state = ttk.Entry(form, width=22)
        self.ent_state.grid(row=8, column=1, sticky="w", padx=1, pady=4)

        # Row 9: ZIP Code/Postcode
        ttk.Label(form, text="ZIP Code/Postcode*").grid(row=9, column=0, sticky="w", padx=1, pady=4)
        self.ent_zip = ttk.Entry(form, width=22)
        self.ent_zip.grid(row=9, column=1, sticky="w", padx=1, pady=4)

        # Row 10: Phone Number
        ttk.Label(form, text="Phone Number*").grid(row=10, column=0, sticky="w", padx=1, pady=4)
        self.ent_phone = ttk.Entry(form, width=22)
        self.ent_phone.grid(row=10, column=1, sticky="w", padx=1, pady=4)

        # Rows 11-12: Action buttons
        #btns = ttk.Frame(form)
        #btns.grid(row=8, column=0, columnspan=4, sticky="w", padx=4, pady=8)
        ttk.Button(form, text="Create New Record", command=self.on_client_create).grid(row=11, column=0, sticky="sw", padx=4, pady=4)
        ttk.Button(form, text="Update Record", command=self.on_client_update).grid(row=11, column=1, sticky="se", padx=4, pady=4)
        ttk.Button(form, text="Delete Record", command=self.on_client_delete).grid(row=12, column=0, sticky="sw", padx=4, pady=4)
        ttk.Button(form, text="Save Changes").grid(row=12, column=1, sticky="se", padx=4, pady=4) # Does nothing yet

        # Right Panel:
        # Search bar + list
        bar = ttk.Frame(right); bar.pack(side="top", fill="x")
        ttk.Label(bar, text="Search (by Client ID/Phone Number/Name)").pack(side="left")
        self.ent_client_search = ttk.Entry(bar, width=32)
        self.ent_client_search.pack(side="left", padx=6)
        ttk.Button(bar, text="Find", command=self.on_client_search).pack(side="left", padx=4)
        ttk.Button(bar, text="Show All", command=self.refresh_clients).pack(side="left", padx=4)

        self.tree_clients = ttk.Treeview(right, columns=("Client ID", "Name", "Phone Number"), show="headings", height=10)
        for c, w in (("Client ID", 100), ("Name", 260), ("Phone Number", 160)):
            self.tree_clients.heading(c, text=c)
            self.tree_clients.column(c, width=w, anchor="w")
        self.tree_clients.pack(fill="both", expand=True, padx=0, pady=8)
        self.tree_clients.bind("<<TreeviewSelect>>", self.on_client_select)

    def _collect_client_form(self) -> dict:
        return dict(
            Name=self.ent_name.get().strip(),
            Address1=self.ent_addr1.get().strip(),
            Address2=self.ent_addr2.get().strip(),
            Address3=self.ent_addr3.get().strip(),
            City=self.cmb_city.get().strip(),
            State=self.ent_state.get().strip(),
            Zip=self.ent_zip.get().strip(),
            Country=self.cmb_country.get().strip(),
            Phone=self.ent_phone.get().strip(),
            Type="client",
        )

    def refresh_clients(self, rows=None):
        if rows is None:
            rows = self.rms.clients
        self.tree_clients.delete(*self.tree_clients.get_children())
        for r in rows:
            self.tree_clients.insert("", "end", values=(r.get("client_id"), r.get("Name", ""), r.get("Phone", "")))

    def on_client_select(self, _evt):
        sel = self.tree_clients.selection()
        if not sel:
            return
        vals = self.tree_clients.item(sel[0], "values")
        cid = int(vals[0])
        r = self.rms._find(self.rms.clients, "client_id", cid) or {}
        # Fill form
        self.ent_client_id.configure(state="normal")
        self.ent_client_id.delete(0, "end")
        self.ent_client_id.insert(0, r.get("client_id"))
        self.ent_client_id.configure(state="readonly")

        self.ent_name.delete(0, "end"); self.ent_name.insert(0, r.get("Name", ""))
        self.ent_addr1.delete(0, "end"); self.ent_addr1.insert(0, r.get("Address1", ""))
        self.ent_addr2.delete(0, "end"); self.ent_addr2.insert(0, r.get("Address2", ""))
        self.ent_addr3.delete(0, "end"); self.ent_addr3.insert(0, r.get("Address3", ""))
        self.cmb_city.set(r.get("City", ""))
        self.ent_state.delete(0, "end"); self.ent_state.insert(0, r.get("State", ""))
        self.ent_zip.delete(0, "end"); self.ent_zip.insert(0, r.get("Zip", ""))
        self.cmb_country.set(r.get("Country", ""))
        self.ent_phone.delete(0, "end"); self.ent_phone.insert(0, r.get("Phone", ""))

    def on_client_create(self):
        if not messagebox.askyesno("Confirm", "Create this client?"):
            return
        try:
            data = self._collect_client_form()
            r = self.rms.create_client(data)
            messagebox.showinfo("OK", f"Created client {r['client_id']}")
            self.refresh_clients()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_client_update(self):
        cid = self.ent_client_id.get().strip()
        if not cid:
            messagebox.showerror("Error", "No client selected")
            return
        if not messagebox.askyesno("Confirm", f"Update client {cid}?"):
            return
        try:
            data = self._collect_client_form()
            r = self.rms.update_client(int(cid), data)
            messagebox.showinfo("OK", f"Updated client {r['client_id']}")
            self.refresh_clients()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_client_delete(self):
        cid = self.ent_client_id.get().strip()
        if not cid:
            messagebox.showerror("Error", "No client selected")
            return
        if not messagebox.askyesno("Confirm", f"Delete client {cid} and its flights?"):
            return
        try:
            self.rms.delete_client(int(cid))
            messagebox.showinfo("OK", "Deleted.")
            self.refresh_clients()
            self.refresh_flights()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_client_search(self):
        q = self.ent_client_search.get().strip()
        rows = self.rms.search_clients(q)
        self.refresh_clients(rows)

    # ==============================================
    # Airlines Tab
    # ==============================================
    def build_airlines_tab(self):
        f = self.tab_airlines

        # Left and Right Panels, Left if fixed, Right expands
        left = ttk.Frame(f, width=420)
        left.pack(side="left", fill="y", padx=(8,4), pady=8)
        left.pack_propagate(False)

        right = ttk.Frame(f)
        right.pack(side="left", fill="both", expand=True, padx=(4,8), pady=8)

        # Left Panel:

        form = ttk.Frame(left)
        form.pack(fill="y", expand=False)

        # Row 0: Airline ID
        ttk.Label(form, text="Airline ID").grid(row=0, column=0, sticky="w", padx=1, pady=4)
        self.ent_airline_id = ttk.Entry(form, width=22, state="readonly", style="Gray.TEntry")
        self.ent_airline_id.grid(row=0, column=1, sticky="w", padx=1, pady=4)

        # Row 1: Record Type
        ttk.Label(form, text="Record Type").grid(row=1, column=0, sticky="w", padx=1, pady=4)
        self.ent_airline_type = ttk.Entry(form, width=22, state="readonly", style="Gray.TEntry")
        self.ent_airline_type.grid(row=1, column=1, sticky="w", padx=1, pady=4)
        var = tk.StringVar(value="airline")
        self.ent_airline_type.configure(textvariable=var)

        # Row 2: Company Name
        ttk.Label(form, text="Company Name").grid(row=2, column=0, sticky="w", padx=1, pady=4)
        self.ent_company = ttk.Entry(form, width=22)
        self.ent_company.grid(row=2, column=1, sticky="w", padx=1, pady=4)

        # Rows 3-4: Action buttons
        #bar = ttk.Frame(form); bar.grid(row=2, column=0, columnspan=4, sticky="w", padx=4, pady=8)
        ttk.Button(form, text="Create New Record", command=self.on_airline_create).grid(row=11, column=0, sticky="sw", padx=4, pady=4)
        ttk.Button(form, text="Update Record", command=self.on_airline_update).grid(row=11, column=1, sticky="se", padx=4, pady=4)
        ttk.Button(form, text="Delete Record", command=self.on_airline_delete).grid(row=12, column=0, sticky="sw", padx=4, pady=4)
        ttk.Button(form, text="Save Changes").grid(row=12, column=1, sticky="se", padx=4, pady=4) # Does nothing yet

        # Right Panel:
        # Search bar + list
        bar = ttk.Frame(right); bar.pack(side="top", fill="x")
        # bar = ttk.Frame(f); bar.pack(side="top", fill="x", padx=8, pady=4)
        # ttk.Label(bar, text="Search (by Airline ID/Company Name)").pack(side="left")
        # self.ent_client_search = ttk.Entry(bar, width=32)
        # self.ent_client_search.pack(side="left", padx=6)
        # ttk.Button(bar, text="Find", command=self.on_airline_search).pack(side="left", padx=4)
        # ttk.Button(bar, text="Show All", command=self.refresh_airlines).pack(side="left", padx=4)

        self.tree_airlines = ttk.Treeview(right, columns=("Airline ID", "Company Name"), show="headings", height=10)
        for c, w in (("Airline ID", 180), ("Company Name", 360)):
            self.tree_airlines.heading(c, text=c)
            self.tree_airlines.column(c, width=w, anchor="w")
        self.tree_airlines.pack(fill="both", expand=True, padx=0, pady=8)
        self.tree_airlines.bind("<<TreeviewSelect>>", self.on_airline_select)

    def refresh_airlines(self):
        self.tree_airlines.delete(*self.tree_airlines.get_children())
        for r in self.rms.airlines:
            self.tree_airlines.insert("", "end", values=(r.get("airline_id"), r.get("CompanyName", "")))

    def on_airline_select(self, _evt):
        sel = self.tree_airlines.selection()
        if not sel:
            return
        vals = self.tree_airlines.item(sel[0], "values")
        aid = int(vals[0])
        r = self.rms._find(self.rms.airlines, "airline_id", aid) or {}

        self.ent_airline_id.configure(state="normal")
        self.ent_airline_id.delete(0, "end")
        self.ent_airline_id.insert(0, r.get("airline_id"))
        self.ent_airline_id.configure(state="readonly")

        self.ent_company.delete(0, "end")
        self.ent_company.insert(0, r.get("CompanyName", ""))

    def on_airline_create(self):
        if not messagebox.askyesno("Confirm", "Create this airline?"):
            return
        try:
            r = self.rms.create_airline({"CompanyName": self.ent_company.get().strip()})
            messagebox.showinfo("OK", f"Created airline {r['airline_id']}")
            self.refresh_airlines()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_airline_update(self):
        aid = self.ent_airline_id.get().strip()
        if not aid:
            messagebox.showerror("Error", "No airline selected")
            return
        if not messagebox.askyesno("Confirm", f"Update airline {aid}?"):
            return
        try:
            r = self.rms.update_airline(int(aid), {"CompanyName": self.ent_company.get().strip()})
            messagebox.showinfo("OK", f"Updated airline {r['airline_id']}")
            self.refresh_airlines()
            self.refresh_flights()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_airline_delete(self):
        aid = self.ent_airline_id.get().strip()
        if not aid:
            messagebox.showerror("Error", "No airline selected")
            return
        if not messagebox.askyesno("Confirm", f"Delete airline {aid} and its flights?"):
            return
        try:
            self.rms.delete_airline(int(aid))
            messagebox.showinfo("OK", "Deleted.")
            self.refresh_airlines()
            self.refresh_flights()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # def on_airline_search(self):
        # q = self.ent_airline_search.get().strip()
        # rows = self.rms.search_airlines(q)
        # self.refresh_airlines(rows)

    # ==============================================
    # Flights Tab
    # ==============================================
    def build_flights_tab(self):
        f = self.tab_flights

        # Left and Right Panels, Left if fixed, Right expands
        left = ttk.Frame(f, width=420)
        left.pack(side="left", fill="y", padx=(8,4), pady=8)
        left.pack_propagate(False)

        right = ttk.Frame(f)
        right.pack(side="left", fill="both", expand=True, padx=(4,8), pady=8)

        # Left Panel:
        form = ttk.Frame(left)
        form.pack(fill="y", expand=False)

        # Row 0: Flight ID (read-only)
        ttk.Label(form, text="Flight ID").grid(row=0, column=0, sticky="w", padx=1, pady=4)
        self.ent_fid = ttk.Entry(form, width=22, state="readonly", style="Gray.TEntry")
        self.ent_fid.grid(row=0, column=1, sticky="w", padx=1, pady=4)

        # Row 1: Client dropdown
        ttk.Label(form, text="Client").grid(row=1, column=0, sticky="w", padx=1, pady=4)
        self.cmb_client = ttk.Combobox(form, width=21, values=self.rms.list_clients_combo(), state="readonly")
        self.cmb_client.grid(row=1, column=1, sticky="w", padx=1, pady=4)

        # Row 2: Airline dropdown
        ttk.Label(form, text="Airline").grid(row=2, column=0, sticky="w", padx=1, pady=4)
        self.cmb_airline = ttk.Combobox(form, width=21, values=self.rms.list_airlines_combo(), state="readonly")
        self.cmb_airline.grid(row=2, column=1, sticky="w", padx=1, pady=4)

        # Row 3: Date dropdown
        years = [str(y) for y in range(2024, 2031)]
        months = [f"{m:02d}" for m in range(1, 13)]
        days = [f"{d:02d}" for d in range(1, 32)]
        hours = [f"{h:02d}" for h in range(0, 24)]
        minutes = [f"{m:02d}" for m in range(0, 60, 5)]

        bar = ttk.Frame(form); bar.grid(row=3, column=0, columnspan=3, sticky="w", pady=4)
        ttk.Label(bar, text="Date (Y/M/D H:M)").grid(row=3,column=0, sticky="w", pady=4)
        self.cbY = ttk.Combobox(bar, width=4, values=years, state="readonly")
        self.cbM = ttk.Combobox(bar, width=1, values=months, state="readonly")
        self.cbD = ttk.Combobox(bar, width=1, values=days, state="readonly")
        self.cbH = ttk.Combobox(bar, width=2, values=hours, state="readonly")
        self.cbMin = ttk.Combobox(bar, width=2, values=minutes, state="readonly")
        for i, cb in enumerate([self.cbY, self.cbM, self.cbD, self.cbH, self.cbMin], start=1):
            cb.grid(row=3, column=i, sticky="w", pady=4)

        # Rows 4-5: Start and End Cities
        ttk.Label(form, text="Start City").grid(row=4, column=0, sticky="w", padx=1, pady=4)
        self.cmb_start = ttk.Combobox(form, width=21, values=self.rms.list_cities(), state="readonly")
        self.cmb_start.grid(row=4, column=1, sticky="w", padx=1, pady=4)
        ttk.Label(form, text="End City").grid(row=5, column=0, sticky="w", padx=1, pady=4)
        self.cmb_end = ttk.Combobox(form, width=21, values=self.rms.list_cities(), state="readonly")
        self.cmb_end.grid(row=5, column=1, sticky="w", padx=1, pady=4)

        # Action buttons
        # bar = ttk.Frame(form); bar.grid(row=5, column=0, columnspan=4, sticky="w", padx=4, pady=8)
        ttk.Button(form, text="Create", command=self.on_flight_create).grid(row=6, column=0, sticky="sw", padx=4, pady=4)
        ttk.Button(form, text="Update", command=self.on_flight_update).grid(row=6, column=1, sticky="se", padx=4, pady=4)
        ttk.Button(form, text="Delete", command=self.on_flight_delete).grid(row=7, column=0, sticky="sw", padx=4, pady=4)
        ttk.Button(form, text="Save Changes", command=self).grid(row=7, column=1, sticky="se", padx=4, pady=4) # Does nothing yet

        # Right Panel:
        # Search + foreign key combo search
        sbar = ttk.Frame(right); sbar.pack(side="top", fill="x")
        ttk.Label(sbar, text="Search by Client ID/Client Name/Phone Number").grid(row=0, column=0, sticky="w")
        self.ent_fsearch = ttk.Entry(sbar, width=32); self.ent_fsearch.grid(row=0, column=1, sticky="w")
        ttk.Button(sbar, text="Find", command=self.on_flight_search).grid(row=0, column=2, padx=4)
        ttk.Button(sbar, text="Filter", command=self.on_flight_search_fk).grid(row=1, column=2, padx=4)
        ttk.Button(sbar, text="Show All", command=self.refresh_flights).grid(row=0, column=3, padx=4)
        

        ttk.Label(sbar, text="Filter by Client & Airline").grid(row=1, column=0, sticky="w")
        self.cmb_fk_client = ttk.Combobox(sbar, width=31, values=self.rms.list_clients_combo(), state="readonly")
        self.cmb_fk_client.grid(row=1, column=1, sticky="w")
        self.cmb_fk_airline = ttk.Combobox(sbar, width=31, values=self.rms.list_airlines_combo(), state="readonly")
        self.cmb_fk_airline.grid(row=2, column=1, sticky="w")


        # List
        cols = ("ID", "Client Name", "Phone Number", "Airline Name", "Date", "Start City", "End City")
        self.tree_flights = ttk.Treeview(right, columns=cols, show="headings", height=12)
        widths = (70, 180, 120, 160, 140, 120, 120)
        for c, w in zip(cols, widths):
            self.tree_flights.heading(c, text=c)
            self.tree_flights.column(c, width=w, anchor="w")
        self.tree_flights.pack(fill="both", expand=True, pady=8)
        self.tree_flights.bind("<<TreeviewSelect>>", self.on_flight_select)

    # ---- flights helpers ----
    @staticmethod
    def _pick_id_from_combo(txt: str) -> int:
        # "123 - Alice (138...)" -> 123
        try:
            if txt and "-" in txt:
                return int(txt.split("-", 1)[0].strip())
        except Exception:
            pass
        return 0

    def _collect_flight_form(self) -> dict:
        y, m, d, h, mi = self.cbY.get(), self.cbM.get(), self.cbD.get(), self.cbH.get(), self.cbMin.get()
        if not all([y, m, d, h, mi]):
            raise ValueError("Please select complete date time (Y/M/D H:M)")
        dt = f"{y}-{m}-{d} {h}:{mi}"
        # Validate correctness
        datetime.strptime(dt, "%Y-%m-%d %H:%M")
        return dict(
            client_id=self._pick_id_from_combo(self.cmb_client.get()),
            airline_id=self._pick_id_from_combo(self.cmb_airline.get()),
            Date=dt,
            StartCity=self.cmb_start.get(),
            EndCity=self.cmb_end.get(),
            Type="flight",
        )

    def refresh_flights(self, rows=None):
        if rows is None:
            # enrich for display
            rows = []
            for f in self.rms.flights:
                c = self.rms._find(self.rms.clients, "client_id", int(f.get("client_id", 0))) or {}
                a = self.rms._find(self.rms.airlines, "airline_id", int(f.get("airline_id", 0))) or {}
                rows.append({
                    "ID": f.get("ID"),
                    "ClientName": c.get("Name", ""),
                    "Phone": c.get("Phone", ""),
                    "Airline": a.get("CompanyName", ""),
                    "Date": f.get("Date", ""),
                    "StartCity": f.get("StartCity", ""),
                    "EndCity": f.get("EndCity", ""),
                })
        self.tree_flights.delete(*self.tree_flights.get_children())
        for r in rows:
            self.tree_flights.insert("", "end", values=(r["ID"], r["ClientName"], r["Phone"],
                                                       r["Airline"], r["Date"], r["StartCity"], r["EndCity"]))

        # Update dropdowns (to avoid lists not refreshing after create/delete)
        self.cmb_client.configure(values=self.rms.list_clients_combo())
        self.cmb_fk_client.configure(values=self.rms.list_clients_combo())
        self.cmb_airline.configure(values=self.rms.list_airlines_combo())
        self.cmb_fk_airline.configure(values=self.rms.list_airlines_combo())

    def on_flight_select(self, _evt):
        sel = self.tree_flights.selection()
        if not sel:
            return
        fid = int(self.tree_flights.item(sel[0], "values")[0])
        row = self.rms._find(self.rms.flights, "ID", fid) or {}

        self.ent_fid.configure(state="normal")
        self.ent_fid.delete(0, "end")
        self.ent_fid.insert(0, row.get("ID"))
        self.ent_fid.configure(state="readonly")

        # Restore form
        c = self.rms._find(self.rms.clients, "client_id", int(row.get("client_id", 0))) or {}
        a = self.rms._find(self.rms.airlines, "airline_id", int(row.get("airline_id", 0))) or {}
        if c:
            self.cmb_client.set(f'{c["client_id"]} - {c.get("Name","")} ({c.get("Phone","")})')
        if a:
            self.cmb_airline.set(f'{a["airline_id"]} - {a.get("CompanyName","")}')

        dt = row.get("Date", "2025-01-01 00:00")
        try:
            ymd, hm = dt.split(" ")
            y, m, d = ymd.split("-")
            h, mi = hm.split(":")
            self.cbY.set(y); self.cbM.set(m); self.cbD.set(d); self.cbH.set(h); self.cbMin.set(mi)
        except Exception:
            pass
        self.cmb_start.set(row.get("StartCity", ""))
        self.cmb_end.set(row.get("EndCity", ""))

    def on_flight_create(self):
        if not messagebox.askyesno("Confirm", "Create this flight?"):
            return
        try:
            data = self._collect_flight_form()
            f = self.rms.create_flight(data)
            messagebox.showinfo("OK", f"Created flight {f['ID']}")
            self.refresh_flights()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_flight_update(self):
        fid = self.ent_fid.get().strip()
        if not fid:
            messagebox.showerror("Error", "No flight selected")
            return
        if not messagebox.askyesno("Confirm", f"Update flight {fid}?"):
            return
        try:
            data = self._collect_flight_form()
            f = self.rms.update_flight(int(fid), data)
            messagebox.showinfo("OK", f"Updated flight {f['ID']}")
            self.refresh_flights()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_flight_delete(self):
        fid = self.ent_fid.get().strip()
        if not fid:
            messagebox.showerror("Error", "No flight selected")
            return
        if not messagebox.askyesno("Confirm", f"Delete flight {fid}?"):
            return
        try:
            self.rms.delete_flight(int(fid))
            messagebox.showinfo("OK", "Deleted.")
            self.refresh_flights()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_flight_search(self):
        q = self.ent_fsearch.get().strip()
        rows = self.rms.search_flights(q)
        self.refresh_flights(rows)

    def on_flight_search_fk(self):
        cid = self._pick_id_from_combo(self.cmb_fk_client.get())
        aid = self._pick_id_from_combo(self.cmb_fk_airline.get())
        if cid <= 0 or aid <= 0:
            messagebox.showerror("Error", "Please pick both Client and Airline")
            return
        rows = self.rms.search_flights_by_fk(cid, aid)
        # rows are original flights with enhancements; convert directly to display structure
        disp = [{
            "ID": r["ID"],
            "ClientName": r.get("ClientName", ""),
            "Phone": r.get("Phone", ""),
            "Airline": r.get("Airline", ""),
            "Date": r.get("Date", ""),
            "StartCity": r.get("StartCity", ""),
            "EndCity": r.get("EndCity", "")
        } for r in rows]
        self.refresh_flights(disp)



if __name__ == "__main__":
    App().mainloop()
