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

READONLY_STYLE = "Gray.TEntry"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Record Management System")
        self.geometry("1100x700")
        self.resizable(True, True)

        self.rms = RMS()

        nb = ttk.Notebook(self)
        self.tab_clients = ttk.Frame(nb)
        self.tab_airlines = ttk.Frame(nb)
        self.tab_flights = ttk.Frame(nb)
        nb.add(self.tab_clients, text="Clients")
        nb.add(self.tab_airlines, text="Airlines")
        nb.add(self.tab_flights, text="Flights")
        nb.pack(fill="both", expand=True)

        # 样式：灰色只读
        self.style = ttk.Style(self)
        self.style.configure(READONLY_STYLE, foreground="#666")

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

        form = ttk.LabelFrame(f, text="Client Form")
        form.pack(side="top", fill="x", padx=8, pady=8)

        # 行0：ID / Type（只读置灰）
        ttk.Label(form, text="client_id").grid(row=0, column=0, sticky="e", padx=4, pady=4)
        self.ent_client_id = ttk.Entry(form, width=12, state="readonly", style=READONLY_STYLE)
        self.ent_client_id.grid(row=0, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="Type").grid(row=0, column=2, sticky="e", padx=4, pady=4)
        self.ent_client_type = ttk.Entry(form, width=12, state="readonly", style=READONLY_STYLE)
        self.ent_client_type.grid(row=0, column=3, sticky="w", padx=4, pady=4)
        self.ent_client_type_var = tk.StringVar(value="client")
        self.ent_client_type.configure(textvariable=self.ent_client_type_var)

        # ⚠️ 字段顺序：Name → Phone → Country → City → State → Zip → Address1/2/3
        # 行1：Name / Phone
        ttk.Label(form, text="Name*").grid(row=1, column=0, sticky="e", padx=4, pady=4)
        self.ent_name = ttk.Entry(form, width=40)
        self.ent_name.grid(row=1, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="Phone*").grid(row=1, column=2, sticky="e", padx=4, pady=4)
        self.ent_phone = ttk.Entry(form, width=20)
        self.ent_phone.grid(row=1, column=3, sticky="w", padx=4, pady=4)

        # 行2：Country / City（下拉）
        ttk.Label(form, text="Country*").grid(row=2, column=0, sticky="e", padx=4, pady=4)
        self.cmb_country = ttk.Combobox(form, width=24, values=self.rms.list_countries(), state="readonly")
        self.cmb_country.grid(row=2, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="City*").grid(row=2, column=2, sticky="e", padx=4, pady=4)
        self.cmb_city = ttk.Combobox(form, width=24, values=self.rms.list_cities(), state="readonly")
        self.cmb_city.grid(row=2, column=3, sticky="w", padx=4, pady=4)

        # 行3：State / Zip
        ttk.Label(form, text="State*").grid(row=3, column=0, sticky="e", padx=4, pady=4)
        self.ent_state = ttk.Entry(form, width=18)
        self.ent_state.grid(row=3, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="Zip*").grid(row=3, column=2, sticky="e", padx=4, pady=4)
        self.ent_zip = ttk.Entry(form, width=18)
        self.ent_zip.grid(row=3, column=3, sticky="w", padx=4, pady=4)

        # 行4：Address1/2/3
        ttk.Label(form, text="Address1*").grid(row=4, column=0, sticky="e", padx=4, pady=4)
        self.ent_addr1 = ttk.Entry(form, width=40)
        self.ent_addr1.grid(row=4, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="Address2").grid(row=4, column=2, sticky="e", padx=4, pady=4)
        self.ent_addr2 = ttk.Entry(form, width=40)
        self.ent_addr2.grid(row=4, column=3, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="Address3").grid(row=5, column=0, sticky="e", padx=4, pady=4)
        self.ent_addr3 = ttk.Entry(form, width=40)
        self.ent_addr3.grid(row=5, column=1, sticky="w", padx=4, pady=4)

        # 操作按钮
        btns = ttk.Frame(form)
        btns.grid(row=6, column=0, columnspan=4, sticky="w", padx=4, pady=8)
        ttk.Button(btns, text="Create", command=self.on_client_create).pack(side="left", padx=4)
        ttk.Button(btns, text="Update", command=self.on_client_update).pack(side="left", padx=4)
        ttk.Button(btns, text="Delete", command=self.on_client_delete).pack(side="left", padx=4)

        # 搜索栏 + 列表
        bar = ttk.Frame(f); bar.pack(side="top", fill="x", padx=8, pady=4)
        ttk.Label(bar, text="Search (by client_id / phone / name)").pack(side="left")
        self.ent_client_search = ttk.Entry(bar, width=32)
        self.ent_client_search.pack(side="left", padx=6)
        ttk.Button(bar, text="Find", command=self.on_client_search).pack(side="left", padx=4)
        ttk.Button(bar, text="Show All", command=self.refresh_clients).pack(side="left", padx=4)

        # ⚠️ 列表：显示所有主要字段
        client_cols = (
            "client_id", "Name", "Phone", "Country", "City", "State",
            "Zip", "Address1", "Address2", "Address3"
        )
        self.tree_clients = ttk.Treeview(f, columns=client_cols, show="headings", height=12)
        widths = (90, 180, 120, 140, 120, 100, 90, 200, 160, 160)
        for c, w in zip(client_cols, widths):
            self.tree_clients.heading(c, text=c)
            self.tree_clients.column(c, width=w, anchor="w")
        self.tree_clients.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree_clients.bind("<<TreeviewSelect>>", self.on_client_select)

        self._client_columns = client_cols  # 保存列顺序用于刷新

    def _collect_client_form(self) -> dict:
        return dict(
            Name=self.ent_name.get().strip(),
            Phone=self.ent_phone.get().strip(),
            Country=self.cmb_country.get().strip(),
            City=self.cmb_city.get().strip(),
            State=self.ent_state.get().strip(),
            Zip=self.ent_zip.get().strip(),
            Address1=self.ent_addr1.get().strip(),
            Address2=self.ent_addr2.get().strip(),
            Address3=self.ent_addr3.get().strip(),
            Type="client",
        )

    def refresh_clients(self, rows=None):
        if rows is None:
            rows = self.rms.clients
        self.tree_clients.delete(*self.tree_clients.get_children())
        for r in rows:
            vals = [r.get(k, "") for k in self._client_columns]
            self.tree_clients.insert("", "end", values=vals)

    def on_client_select(self, _evt):
        sel = self.tree_clients.selection()
        if not sel:
            return
        values = self.tree_clients.item(sel[0], "values")
        row = {self._client_columns[i]: values[i] for i in range(len(self._client_columns))}

        self.ent_client_id.configure(state="normal")
        self.ent_client_id.delete(0, "end")
        self.ent_client_id.insert(0, row.get("client_id"))
        self.ent_client_id.configure(state="readonly")

        self.ent_name.delete(0, "end"); self.ent_name.insert(0, row.get("Name", ""))
        self.ent_phone.delete(0, "end"); self.ent_phone.insert(0, row.get("Phone", ""))
        self.cmb_country.set(row.get("Country", ""))
        self.cmb_city.set(row.get("City", ""))
        self.ent_state.delete(0, "end"); self.ent_state.insert(0, row.get("State", ""))
        self.ent_zip.delete(0, "end"); self.ent_zip.insert(0, row.get("Zip", ""))
        self.ent_addr1.delete(0, "end"); self.ent_addr1.insert(0, row.get("Address1", ""))
        self.ent_addr2.delete(0, "end"); self.ent_addr2.insert(0, row.get("Address2", ""))
        self.ent_addr3.delete(0, "end"); self.ent_addr3.insert(0, row.get("Address3", ""))

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
            self.refresh_flights()
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
        form = ttk.LabelFrame(f, text="Airline Form")
        form.pack(side="top", fill="x", padx=8, pady=8)

        ttk.Label(form, text="airline_id").grid(row=0, column=0, sticky="e", padx=4, pady=4)
        self.ent_airline_id = ttk.Entry(form, width=12, state="readonly", style=READONLY_STYLE)
        self.ent_airline_id.grid(row=0, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(form, text="Type").grid(row=0, column=2, sticky="e", padx=4, pady=4)
        self.ent_airline_type = ttk.Entry(form, width=12, state="readonly", style=READONLY_STYLE)
        self.ent_airline_type.grid(row=0, column=3, sticky="w", padx=4, pady=4)
        var = tk.StringVar(value="airline")
        self.ent_airline_type.configure(textvariable=var)

        ttk.Label(form, text="CompanyName*").grid(row=1, column=0, sticky="e", padx=4, pady=4)
        self.ent_company = ttk.Entry(form, width=40)
        self.ent_company.grid(row=1, column=1, columnspan=3, sticky="w", padx=4, pady=4)

        bar = ttk.Frame(form); bar.grid(row=2, column=0, columnspan=4, sticky="w", padx=4, pady=8)
        ttk.Button(bar, text="Create", command=self.on_airline_create).pack(side="left", padx=4)
        ttk.Button(bar, text="Update", command=self.on_airline_update).pack(side="left", padx=4)
        ttk.Button(bar, text="Delete", command=self.on_airline_delete).pack(side="left", padx=4)

        # 🔎 搜索栏：支持 airline_id / CompanyName
        sbar = ttk.Frame(f); sbar.pack(side="top", fill="x", padx=8, pady=4)
        ttk.Label(sbar, text="Search (by airline_id / company)").pack(side="left")
        self.ent_airline_search = ttk.Entry(sbar, width=32)
        self.ent_airline_search.pack(side="left", padx=6)
        ttk.Button(sbar, text="Find", command=self.on_airline_search).pack(side="left", padx=4)
        ttk.Button(sbar, text="Show All", command=self.refresh_airlines).pack(side="left", padx=4)

        self.tree_airlines = ttk.Treeview(f, columns=("airline_id", "Type", "CompanyName"),
                                          show="headings", height=12)
        for c, w in (("airline_id", 100), ("Type", 100), ("CompanyName", 420)):
            self.tree_airlines.heading(c, text=c)
            self.tree_airlines.column(c, width=w, anchor="w")
        self.tree_airlines.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree_airlines.bind("<<TreeviewSelect>>", self.on_airline_select)

    def refresh_airlines(self, rows=None):
        if rows is None:
            rows = self.rms.airlines
        self.tree_airlines.delete(*self.tree_airlines.get_children())
        for r in rows:
            self.tree_airlines.insert("", "end", values=(r.get("airline_id"), r.get("Type", "airline"),
                                                         r.get("CompanyName", "")))

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
            self.refresh_flights()
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

    def on_airline_search(self):
        q = self.ent_airline_search.get().strip()
        rows = self.rms.search_airlines(q)
        self.refresh_airlines(rows)

    # ==============================================
    # Flights Tab
    # ==============================================
    def build_flights_tab(self):
        f = self.tab_flights
        form = ttk.LabelFrame(f, text="Flight Form")
        form.pack(side="top", fill="x", padx=8, pady=8)

        # 航班 ID（只读）
        ttk.Label(form, text="Flight ID").grid(row=0, column=0, sticky="e", padx=4, pady=4)
        self.ent_fid = ttk.Entry(form, width=12, state="readonly", style=READONLY_STYLE)
        self.ent_fid.grid(row=0, column=1, sticky="w", padx=4, pady=4)

        # Client 下拉
        ttk.Label(form, text="Client").grid(row=1, column=0, sticky="e", padx=4, pady=4)
        self.cmb_client = ttk.Combobox(form, width=44, values=self.rms.list_clients_combo(), state="readonly")
        self.cmb_client.grid(row=1, column=1, columnspan=3, sticky="w", padx=4, pady=4)

        # Airline 下拉
        ttk.Label(form, text="Airline").grid(row=2, column=0, sticky="e", padx=4, pady=4)
        self.cmb_airline = ttk.Combobox(form, width=44, values=self.rms.list_airlines_combo(), state="readonly")
        self.cmb_airline.grid(row=2, column=1, columnspan=3, sticky="w", padx=4, pady=4)

        # 日期下拉
        years = [str(y) for y in range(2024, 2031)]
        months = [f"{m:02d}" for m in range(1, 13)]
        days = [f"{d:02d}" for d in range(1, 32)]
        hours = [f"{h:02d}" for h in range(0, 24)]
        minutes = [f"{m:02d}" for m in range(0, 60, 5)]

        ttk.Label(form, text="Date (Y/M/D H:M)").grid(row=3, column=0, sticky="e", padx=4, pady=4)
        self.cbY = ttk.Combobox(form, width=6, values=years, state="readonly")
        self.cbM = ttk.Combobox(form, width=4, values=months, state="readonly")
        self.cbD = ttk.Combobox(form, width=4, values=days, state="readonly")
        self.cbH = ttk.Combobox(form, width=4, values=hours, state="readonly")
        self.cbMin = ttk.Combobox(form, width=4, values=minutes, state="readonly")
        for i, cb in enumerate([self.cbY, self.cbM, self.cbD, self.cbH, self.cbMin], start=1):
            cb.grid(row=3, column=i, sticky="w", padx=2, pady=4)

        # 起讫城市
        ttk.Label(form, text="StartCity").grid(row=4, column=0, sticky="e", padx=4, pady=4)
        self.cmb_start = ttk.Combobox(form, width=20, values=self.rms.list_cities(), state="readonly")
        self.cmb_start.grid(row=4, column=1, sticky="w", padx=4, pady=4)
        ttk.Label(form, text="EndCity").grid(row=4, column=2, sticky="e", padx=4, pady=4)
        self.cmb_end = ttk.Combobox(form, width=20, values=self.rms.list_cities(), state="readonly")
        self.cmb_end.grid(row=4, column=3, sticky="w", padx=4, pady=4)

        # 操作按钮
        bar = ttk.Frame(form); bar.grid(row=5, column=0, columnspan=4, sticky="w", padx=4, pady=8)
        ttk.Button(bar, text="Create", command=self.on_flight_create).pack(side="left", padx=4)
        ttk.Button(bar, text="Update", command=self.on_flight_update).pack(side="left", padx=4)
        ttk.Button(bar, text="Delete", command=self.on_flight_delete).pack(side="left", padx=4)

        # 搜索（⚠️ 按需求：隐藏 client+airline 联合搜索 UI）
        sbar = ttk.Frame(f); sbar.pack(side="top", fill="x", padx=8, pady=4)
        ttk.Label(sbar, text="Search by client_id / name / phone").pack(side="left")
        self.ent_fsearch = ttk.Entry(sbar, width=36); self.ent_fsearch.pack(side="left", padx=6)
        ttk.Button(sbar, text="Find", command=self.on_flight_search).pack(side="left", padx=4)
        ttk.Button(sbar, text="Show All", command=self.refresh_flights).pack(side="left", padx=4)

        # 列表
        cols = ("ID", "ClientName", "Phone", "Airline", "Date", "StartCity", "EndCity")
        self.tree_flights = ttk.Treeview(f, columns=cols, show="headings", height=12)
        widths = (70, 180, 120, 180, 150, 120, 120)
        for c, w in zip(cols, widths):
            self.tree_flights.heading(c, text=c)
            self.tree_flights.column(c, width=w, anchor="w")
        self.tree_flights.pack(fill="both", expand=True, padx=8, pady=8)
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
        # 校验合法性
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

        # 下拉刷新（防止新建/删除后列表不刷新）
        self.cmb_client.configure(values=self.rms.list_clients_combo())
        self.cmb_airline.configure(values=self.rms.list_airlines_combo())

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

        # 还原 form
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
        # 转展示结构
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
