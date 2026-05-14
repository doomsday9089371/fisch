import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
from collections import defaultdict, OrderedDict

DB_PATH = os.path.join(os.path.dirname(__file__), "fisch_data.db")

# Source data is loaded from `fisch_data.db`.

# -------------------------------------------------
# MUTATION DATA (CORE MUTATIONS)
# -------------------------------------------------
MUTATION_LIST = [
    ("None", 1.0),
    ("Ocean's Ruin", 10.2),
    ("Plagued", 10.0),
    ("Tryhard", 10.0),
    ("Ascended", 9.9),
    ("Requies", 9.8),
    ("Fabulous", 9.6),
    ("Withered", 9.5),
    ("Royal", 9.4),
    ("Verdant", 9.2),
    ("Mastered", 9.0),
    ("Mossy", 8.7),
    ("Igneous", 8.65),
    ("Breezed", 8.6),
    ("Blessed", 8.5),
    ("Noctic", 8.5),
    ("Distraught", 8.5),
    ("Serene", 8.5),
    ("Floral", 8.4),
    ("Obsidian", 8.3),
    ("Vitalic", 8.0),
    ("Gleebous", 8.0),
    ("Glowy", 8.0),
    ("Glacial", 8.0),
    ("Atomic", 8.0),
    ("Tentacle Surge", 7.8),
    ("Jackpot", 7.77),
    ("Mourned", 7.5),
    ("Magical", 7.2),
    ("Sacratus", 7.0),
    ("Shrouded", 7.0),
    ("Tidal", 7.0),
    ("Tainted", 6.5),
    ("Evil", 6.5),
    ("Aurora", 6.5),
    ("Luminescent", 6.5),
    ("Oscar", 6.4),
    ("Sunken", 6.3),
    ("Chaotic", 6.2),
    ("Fallen", 6.0),
    ("Nuclear", 6.0),
    ("Toxic", 6.0),
    ("Nova", 6.0),
    ("Heavenly", 6.0),
    ("Subspace", 6.0),
    ("Anomalous", 5.55),
    ("King's Blessing", 5.5),
    ("Prismize", 5.5),
    ("Mythical", 5.5),
    ("Abyssal", 5.5),
    ("Solar", 5.3),
    ("Spirit", 5.2),
    ("Carrot", 5.0),
    ("Sanguine", 5.0),
    ("Siren's Spite", 5.0),
    ("Rainbow Cluster", 5.0),
    ("Levitas", 5.0),
    ("Nico's Nyantics", 5.0),
    ("Ashen Fortune", 5.0),
    ("Colossal Ink", 5.0),
    ("Corvid", 5.0),
    ("Cursed Touch", 5.0),
    ("Emberflame", 5.0),
    ("Galactic", 5.0),
    ("Nullified", 5.0),
    ("Greedy", 5.0),
    ("Gemstone", 5.0),
    ("Blossomed", 4.6),
    ("Phantom", 4.5),
    ("Wrath", 4.5),
    ("Lost", 4.5),
    ("Spring", 4.5),
    ("Harmonized", 4.2),
    ("Bloom", 4.0),
    ("Crimson", 4.0),
    ("Fungal", 4.0),
    ("Revitalized", 4.0),
    ("Autumn", 4.0),
    ("Atlantean", 4.0),
    ("Boreal", 4.0),
    ("Celestial", 4.0),
    ("Cursed", 4.0),
    ("Moon-Kissed", 4.0),
    ("Lucid", 3.5),
    ("Aureolin", 3.5),
    ("Brined", 3.5),
    ("Electric Shock", 3.5),
    ("Vined", 3.5),
    ("Crystalized", 3.5),
    ("Fossilized", 3.3),
    ("Aurulent", 3.0),
    ("Brown Wood", 3.0),
    ("Cracked", 3.0),
    ("Green Leaf", 3.0),
    ("Mother Nature", 3.0),
    ("Blighted", 3.0),
    ("Ember", 3.0),
    ("Hexed", 3.0),
    ("Scorched", 3.0),
    ("Solarblaze", 3.0),
    ("Honey", 2.6),
    ("Winter", 2.5),
    ("Aureate", 2.5),
    ("Lunar", 2.5),
    ("Skrunkly", 2.5),
    ("Midas", 2.5),
    ("Purified", 2.5),
    ("Sleet", 2.4),
    ("Electric", 2.1),
    ("Aurelian", 2.0),
    ("Forgotten", 2.0),
    ("Lightning", 2.0),
    ("Coral", 1.8),
    ("Silver", 1.8),
    ("Studded", 1.8),
    ("Glossy", 1.6),
    ("Aurous", 1.5),
    ("Cement", 1.5),
    ("Darkened", 1.5),
    ("Frozen", 1.5),
    ("Mosaic", 1.5),
    ("Negative", 1.3),
    ("Translucent", 1.3),
    ("Albino", 1.2),
    ("Amber", 1.2),
    ("Sandy", 1.2),
    ("Neon", 1.0),
    ("Summer", 1.0),
    ("Poisoned", 0.9),
    ("Rusty", 0.7),
    ("Unlucky", 0.5),
    ("Charred", 0.5),
    ("Decayed", 0.45),
    ("Dirty", 0.3),
    ("Noxious", 0.3),
    ("Husk", 0.15),
    ("Exploded", 0.1),
    ("Putrid", -0.5),
]

# prefix mutations: 0–4
PREFIX_MUTATIONS = {
    "0": {"name": "None", "mult": 1.0},
    "1": {"name": "Big", "mult": 1.5},
    "2": {"name": "Shiny", "mult": 1.85},
    "3": {"name": "Sparkling", "mult": 1.85},
    "4": {"name": "Giant", "mult": 1.5},
}

ISLAND_LETTER_CODES = OrderedDict(
    [
        ("01", "A"),
        ("02", "B"),
        ("03", "C"),
        ("04", "D"),
        ("05", "E"),
        ("06", "F"),
        ("07", "G"),
        ("08", "K"),
        ("09", "L"),
        ("10", "M"),
        ("11", "N"),
        ("12", "O"),
        ("13", "R"),
        ("14", "S"),
        ("15", "T"),
        ("16", "V"),
    ]
)


def build_mutation_codex():
    codex = OrderedDict()
    for idx, (name, mult) in enumerate(MUTATION_LIST):
        code = f"{idx:03d}"  # 000–137
        codex[code] = {"name": name, "mult": mult}
    return codex


# -------------------------------------------------
# LOAD FISCH DATA AND BUILD CODEX
# -------------------------------------------------
def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def get_connection(db_path=DB_PATH):
    return sqlite3.connect(db_path)


def ensure_tracking_table(db_path=DB_PATH):
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tracked_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                island_code TEXT NOT NULL,
                island_name TEXT NOT NULL,
                fish_code TEXT NOT NULL,
                fish_name TEXT NOT NULL,
                weight REAL NOT NULL,
                base_price REAL NOT NULL,
                prefix_summary TEXT NOT NULL,
                core_name TEXT NOT NULL,
                prefix_mult REAL NOT NULL,
                core_mult REAL NOT NULL,
                final_price REAL NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def load_fisch_data_from_db(db_path=DB_PATH):
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT "Name", "Radar Location", COALESCE("C$/kg", 0)
            FROM fish_data
            ORDER BY "Radar Location" COLLATE NOCASE, "Name" COLLATE NOCASE
            """
        )
        return [
            (name, radar_location, safe_float(sell_value))
            for name, radar_location, sell_value in cursor.fetchall()
        ]
    except sqlite3.OperationalError as exc:
        raise RuntimeError(f"Missing required table `fish_data` in {db_path}") from exc
    finally:
        conn.close()


def load_tracked_items_from_db(db_path=DB_PATH):
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, island_code, island_name, fish_code, fish_name,
                   weight, base_price, prefix_summary, core_name,
                   prefix_mult, core_mult, final_price
            FROM tracked_items
            ORDER BY id
            """
        )
        return cursor.fetchall()
    finally:
        conn.close()


def insert_tracked_item(record, db_path=DB_PATH):
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO tracked_items (
                island_code, island_name, fish_code, fish_name,
                weight, base_price, prefix_summary, core_name,
                prefix_mult, core_mult, final_price
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record["island_code"],
                record["island_name"],
                record["fish_code"],
                record["fish_name"],
                record["weight"],
                record["base_price"],
                record["prefix_summary"],
                record["core_name"],
                record["prefix_mult"],
                record["core_mult"],
                record["final_price"],
            ),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def delete_tracked_items(item_ids, db_path=DB_PATH):
    if not item_ids:
        return

    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        placeholders = ",".join("?" for _ in item_ids)
        cursor.execute(f"DELETE FROM tracked_items WHERE id IN ({placeholders})", tuple(item_ids))
        conn.commit()
    finally:
        conn.close()


def clear_tracked_items(db_path=DB_PATH):
    conn = get_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tracked_items")
        conn.commit()
    finally:
        conn.close()


def build_codex(entries):
    island_to_fish = defaultdict(list)
    for name, island, sell_value in entries:
        island_to_fish[island].append((name, sell_value))

    islands_sorted = sorted(island_to_fish.keys(), key=lambda s: s.lower())
    codex = OrderedDict()

    for group_code, letter in ISLAND_LETTER_CODES.items():
        matching_islands = [name for name in islands_sorted if name.upper().startswith(letter)]
        islands = OrderedDict()

        for idx, island_name in enumerate(matching_islands, start=1):
            fish_list = island_to_fish[island_name]
            fish_dict = OrderedDict()
            for fish_idx, (fish_name, sell_value) in enumerate(fish_list, start=1):
                fish_code = f"{fish_idx:02d}"
                fish_dict[fish_code] = {"name": fish_name, "sell": sell_value}

            islands[f"{idx:02d}"] = {"name": island_name, "fish": fish_dict}

        codex[group_code] = {"letter": letter, "islands": islands}

    return codex


# -------------------------------------------------
# TRACKER APP
# -------------------------------------------------
class FischTracker:
    def __init__(self, root, codex, mutation_codex):
        self.root = root
        self.root.title("Fisch Tracker")
        self.root.geometry("1400x780")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        self.CODEX = codex
        self.MUTATION_CODEX = mutation_codex

        # input state
        self.stage = "letter_group"  # letter_group -> island -> fish -> prefix_count -> prefix_1..3 -> core -> weight
        self.buffer = ""

        self.letter_group_code = ""
        self.island_code = ""
        self.fish_code = ""

        self.prefix_count = 0
        self.prefix_codes = []  # list of "0"–"4"
        self.core_code = "000"

        self.weight = ""

        self.sell_total = 0.0

        self.create_total_label()
        self.create_table()
        self.create_controls()
        self.create_codex_panel()
        self.update_codex()
        self.load_saved_entries()

        self.root.bind("<Delete>", lambda _event: self.remove_selected())
        keyboard.on_press(self.handle_key)

    def get_selected_group(self):
        return self.CODEX.get(self.letter_group_code, {"letter": "", "islands": OrderedDict()})

    def get_selected_island_data(self):
        return self.get_selected_group().get("islands", {}).get(self.island_code, {})

    def get_display_island_code(self):
        if self.letter_group_code and self.island_code:
            return f"{self.letter_group_code}-{self.island_code}"
        return self.island_code

    # ---------------- UI ----------------
    def create_total_label(self):
        self.total_label = tk.Label(self.root, text="Total Sell: 0.00", font=("Arial", 14, "bold"))
        self.total_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)

    def update_total_label(self):
        self.total_label.config(text=f"Total Sell: {self.sell_total:.2f}")

    def create_table(self):
        columns = (
            "island_code",
            "island_name",
            "fish_code",
            "fish_name",
            "weight",
            "base_price",
            "prefix_summary",
            "core_name",
            "prefix_mult",
            "core_mult",
            "final_price",
        )
        self.table = ttk.Treeview(self.root, columns=columns, show="headings", selectmode="extended")
        for col, text in [
            ("island_code", "Island Code"),
            ("island_name", "Island"),
            ("fish_code", "Fish Code"),
            ("fish_name", "Fish"),
            ("weight", "Weight"),
            ("base_price", "Base Price"),
            ("prefix_summary", "Prefixes"),
            ("core_name", "Core Mutation"),
            ("prefix_mult", "Prefix x"),
            ("core_mult", "Core x"),
            ("final_price", "Final Sell"),
        ]:
            self.table.heading(col, text=text)

        column_widths = {
            "island_code": 80,
            "island_name": 140,
            "fish_code": 70,
            "fish_name": 140,
            "weight": 70,
            "base_price": 90,
            "prefix_summary": 140,
            "core_name": 120,
            "prefix_mult": 80,
            "core_mult": 80,
            "final_price": 90,
        }

        for col in columns:
            self.table.column(col, width=column_widths[col], minwidth=column_widths[col], stretch=False)

        self.table.grid(row=1, column=0, sticky="nsew")
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_controls(self):
        controls = tk.Frame(self.root)
        controls.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))

        ttk.Button(controls, text="Remove Selected", command=self.remove_selected).pack(side="left", padx=(0, 8))
        ttk.Button(controls, text="Clear All", command=self.full_reset).pack(side="left")

    def create_codex_panel(self):
        self.codex_frame = tk.Frame(self.root, padx=10)
        self.codex_frame.grid(row=1, column=1, rowspan=2, sticky="ns")

    def add_table_row(self, values, item_id):
        self.table.insert("", "end", iid=str(item_id), values=values)

    def load_saved_entries(self):
        for record in load_tracked_items_from_db():
            (
                item_id,
                island_code,
                island_name,
                fish_code,
                fish_name,
                weight,
                base_price,
                prefix_summary,
                core_name,
                prefix_mult,
                core_mult,
                final_price,
            ) = record

            self.add_table_row(
                (
                    island_code,
                    island_name,
                    fish_code,
                    fish_name,
                    f"{safe_float(weight):.2f}",
                    f"{safe_float(base_price):.2f}",
                    prefix_summary,
                    core_name,
                    f"{safe_float(prefix_mult):.2f}",
                    f"{safe_float(core_mult):.2f}",
                    f"{safe_float(final_price):.2f}",
                ),
                item_id,
            )

        self.refresh_total_label_from_table()

    def refresh_total_label_from_table(self):
        self.sell_total = 0.0
        for item in self.table.get_children():
            values = self.table.item(item, "values")
            if values:
                self.sell_total += safe_float(values[-1])
        self.update_total_label()

    def remove_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Remove Selected", "Select one or more line items to remove.")
            return

        if not messagebox.askyesno("Confirm Removal", "Remove the selected line items?"):
            return

        item_ids = [int(item) for item in selected]
        delete_tracked_items(item_ids)
        for item in selected:
            self.table.delete(item)
        self.refresh_total_label_from_table()

    def clear_all_entries(self, confirm=True):
        if confirm and not messagebox.askyesno("Clear All", "Clear all tracked line items?"):
            return

        clear_tracked_items()
        for item in self.table.get_children():
            self.table.delete(item)
        self.refresh_total_label_from_table()

    def update_codex(self):
        for w in self.codex_frame.winfo_children():
            w.destroy()

        tk.Label(self.codex_frame, text="CODEX", font=("Arial", 14, "bold")).pack(anchor="w")

        if self.stage == "letter_group":
            tk.Label(
                self.codex_frame,
                text="Island Letter Groups (enter 01–16):",
                font=("Arial", 12, "underline"),
            ).pack(anchor="w")
            for group_code, data in self.CODEX.items():
                count = len(data["islands"])
                suffix = "location" if count == 1 else "locations"
                tk.Label(self.codex_frame, text=f"{group_code} – {data['letter']} ({count} {suffix})").pack(anchor="w")

        elif self.stage == "island":
            group = self.get_selected_group()
            tk.Label(
                self.codex_frame,
                text=f"Locations starting with {group.get('letter', '?')}:",
                font=("Arial", 12, "underline"),
            ).pack(anchor="w")
            for island_code, data in group.get("islands", {}).items():
                tk.Label(self.codex_frame, text=f"{island_code} – {data['name']}").pack(anchor="w")

        elif self.stage == "fish":
            data = self.get_selected_island_data()
            if data:
                tk.Label(
                    self.codex_frame,
                    text=f"{self.get_display_island_code()} – {data['name']}",
                    font=("Arial", 12, "underline"),
                ).pack(anchor="w")
                for fish_code, fish_data in data["fish"].items():
                    tk.Label(self.codex_frame, text=f"  {fish_code} – {fish_data['name']}").pack(anchor="w")

        elif self.stage == "prefix_count":
            tk.Label(self.codex_frame, text="Prefix Count (1–3):", font=("Arial", 12, "underline")).pack(anchor="w")
            tk.Label(self.codex_frame, text="1 – One prefix").pack(anchor="w")
            tk.Label(self.codex_frame, text="2 – Two prefixes").pack(anchor="w")
            tk.Label(self.codex_frame, text="3 – Three prefixes").pack(anchor="w")

        elif self.stage in ("prefix_1", "prefix_2", "prefix_3"):
            tk.Label(self.codex_frame, text="Prefix Mutations:", font=("Arial", 12, "underline")).pack(anchor="w")
            for code, info in PREFIX_MUTATIONS.items():
                tk.Label(self.codex_frame, text=f"{code} – {info['name']} ({info['mult']}×)").pack(anchor="w")

        elif self.stage == "core":
            tk.Label(self.codex_frame, text="Core Mutations:", font=("Arial", 12, "underline")).pack(anchor="w")
            for code, info in self.MUTATION_CODEX.items():
                tk.Label(self.codex_frame, text=f"{code} – {info['name']} ({info['mult']}×)").pack(anchor="w")

        elif self.stage == "weight":
            tk.Label(self.codex_frame, text="Enter Weight (then Enter):", font=("Arial", 12, "underline")).pack(
                anchor="w"
            )

    # ------------- INPUT LOGIC -------------
    def handle_key(self, event):
        key = event.name

        if key.startswith("num "):
            key = key.replace("num ", "")

        if key in "0123456789":
            self.buffer += key
            self.process_buffer()
        elif key == "decimal":
            if self.stage == "weight" and "." not in self.buffer:
                self.buffer += "."
        elif key in ("plus", "+"):
            self.buffer += "+"
        elif key == "enter":
            if self.buffer == "+++":
                self.full_reset()
                return
            self.submit_entry()

    def process_buffer(self):
        if self.stage == "letter_group":
            if len(self.buffer) == 2:
                self.letter_group_code = self.buffer
                self.buffer = ""
                group = self.CODEX.get(self.letter_group_code)
                if not group:
                    messagebox.showerror("Error", f"Invalid letter group: {self.letter_group_code}")
                    self.reset()
                    return
                if not group.get("islands"):
                    messagebox.showinfo("No Locations", f"No locations found for letter {group['letter']}.")
                    self.reset()
                    return
                self.stage = "island"
                self.update_codex()

        elif self.stage == "island":
            if len(self.buffer) == 2:
                self.island_code = self.buffer
                self.buffer = ""
                islands = self.get_selected_group().get("islands", {})
                if self.island_code not in islands:
                    messagebox.showerror("Error", f"Invalid location code for group {self.letter_group_code}")
                    self.reset()
                    return
                self.stage = "fish"
                self.update_codex()

        elif self.stage == "fish":
            if len(self.buffer) == 2:
                self.fish_code = self.buffer
                self.buffer = ""
                island_data = self.get_selected_island_data()
                fish_dict = island_data.get("fish", {})
                if self.fish_code not in fish_dict:
                    messagebox.showerror("Error", f"Invalid fish code for location {self.get_display_island_code()}")
                    self.reset()
                    return
                self.stage = "prefix_count"
                self.update_codex()

        elif self.stage == "prefix_count":
            if len(self.buffer) == 1:
                c = self.buffer
                self.buffer = ""
                if c not in ("1", "2", "3"):
                    messagebox.showerror("Error", "Prefix count must be 1, 2, or 3.")
                    self.reset()
                    return
                self.prefix_count = int(c)
                self.prefix_codes = []
                self.stage = "prefix_1"
                self.update_codex()

        elif self.stage in ("prefix_1", "prefix_2", "prefix_3"):
            if len(self.buffer) == 1:
                code = self.buffer
                self.buffer = ""
                if code not in PREFIX_MUTATIONS:
                    messagebox.showerror("Error", "Invalid prefix code (0–4).")
                    self.reset()
                    return
                self.prefix_codes.append(code)
                if len(self.prefix_codes) < self.prefix_count:
                    # move to next prefix stage
                    if self.stage == "prefix_1":
                        self.stage = "prefix_2"
                    elif self.stage == "prefix_2":
                        self.stage = "prefix_3"
                    self.update_codex()
                else:
                    # done with prefixes, move to core
                    self.stage = "core"
                    self.update_codex()

        elif self.stage == "core":
            # core code is 3 digits: 000–137
            if len(self.buffer) == 3:
                self.core_code = self.buffer
                self.buffer = ""
                if self.core_code not in self.MUTATION_CODEX:
                    messagebox.showerror("Error", f"Invalid core mutation code: {self.core_code}")
                    self.reset()
                    return
                self.stage = "weight"
                self.update_codex()

        # weight: free-form until Enter

    def submit_entry(self):
        if self.stage != "weight":
            return

        self.weight = self.buffer
        self.buffer = ""

        try:
            weight_val = float(self.weight)
        except ValueError:
            messagebox.showerror("Error", f"Invalid weight: {self.weight}")
            self.reset()
            return

        island_data = self.get_selected_island_data()
        island_name = island_data.get("name", "Unknown")
        fish_data = island_data.get("fish", {}).get(self.fish_code, {})
        fish_name = fish_data.get("name", "Unknown")
        fish_price = float(fish_data.get("sell", 0.0))
        display_island_code = self.get_display_island_code()

        base_price = fish_price * weight_val

        # prefix multiplier
        prefix_mult = 1.0
        prefix_names = []
        for code in self.prefix_codes:
            info = PREFIX_MUTATIONS.get(code, {"name": "None", "mult": 1.0})
            prefix_mult *= info["mult"]
            if info["name"] != "None":
                prefix_names.append(info["name"])
        prefix_summary = ", ".join(prefix_names) if prefix_names else "None"

        # core multiplier
        core_info = self.MUTATION_CODEX.get(self.core_code, {"name": "None", "mult": 1.0})
        core_name = core_info["name"]
        core_mult = core_info["mult"]

        final_price = base_price * prefix_mult * core_mult

        item_id = insert_tracked_item(
            {
                "island_code": display_island_code,
                "island_name": island_name,
                "fish_code": self.fish_code,
                "fish_name": fish_name,
                "weight": weight_val,
                "base_price": base_price,
                "prefix_summary": prefix_summary,
                "core_name": core_name,
                "prefix_mult": prefix_mult,
                "core_mult": core_mult,
                "final_price": final_price,
            }
        )

        self.add_table_row(
            (
                display_island_code,
                island_name,
                self.fish_code,
                fish_name,
                f"{weight_val:.2f}",
                f"{base_price:.2f}",
                prefix_summary,
                core_name,
                f"{prefix_mult:.2f}",
                f"{core_mult:.2f}",
                f"{final_price:.2f}",
            ),
            item_id,
        )
        self.refresh_total_label_from_table()

        self.reset()

    def reset(self):
        self.stage = "letter_group"
        self.buffer = ""
        self.letter_group_code = ""
        self.island_code = ""
        self.fish_code = ""
        self.prefix_count = 0
        self.prefix_codes = []
        self.core_code = "000"
        self.weight = ""
        self.update_codex()

    def full_reset(self):
        self.clear_all_entries(confirm=True)
        self.reset()


# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    ensure_tracking_table()
    try:
        entries = load_fisch_data_from_db()
    except RuntimeError as exc:
        print(exc)
        return

    if not entries:
        print(f"No data loaded from database: {DB_PATH}")
        return

    codex = build_codex(entries)
    mutation_codex = build_mutation_codex()

    root = tk.Tk()
    app = FischTracker(root, codex, mutation_codex)
    root.mainloop()


if __name__ == "__main__":
    main()