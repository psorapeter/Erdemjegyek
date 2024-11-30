# pyinstaller --onefile --ico Érdemjegyek_uj\GUI\Érdemjegyek_GUI.ico Érdemjegyek_uj\GUI\Érdemjegyek_24_25_GUI.pyw

import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from datetime import date, datetime
import datetime
import pandas as pd


class Gyerek:
    def __init__(self, nev, kezdopenz):
        self.nev = nev
        self.kezdopenz = kezdopenz
        self.tantargyak = []
        self.erdemjegyek = []
        self.zsebpenz = 0
        self.df = pd.DataFrame
        self.stat = pd.DataFrame

    def penzek_frissitese(self, lista):
        erdemjegy_erteke = {5: 300, 4: 100, 3: -200, 2: -500, 1: -1000}  # jegyek pénzbeni értékei
        jegyek = [int(elem_p[2]) for elem_p in lista]

        self.zsebpenz = self.kezdopenz + sum(erdemjegy_erteke.get(jegy, 0) for jegy in jegyek)

    def lekerdezes(self):
        # lekérdezés főablak
        lekerdezes_ablak = tk.Toplevel(root)
        lekerdezes_ablak.title(f'Lekérdezés - {self.nev} - 2024/2025 tanév')
        lekerdezes_ablak.wm_attributes("-topmost", 1)
        lekerdezes_ablak.bind("<Escape>", on_escape)
        lekerdezes_ablak_foframe = tk.Frame(lekerdezes_ablak)
        lekerdezes_ablak_foframe.pack(expand=1)
        # lista
        lekerdezes_ablak_lista_frame = LabelFrame(lekerdezes_ablak_foframe, borderwidth=1, relief=RIDGE,
                                                  text=self.nev)
        lekerdezes_ablak_lista_frame.grid(row=0, column=0, rowspan=2, padx=(10, 5), pady=10)
        treeview_leker = ttk.Treeview(lekerdezes_ablak_lista_frame, show="headings", columns=cols_self, height=25)
        treeview_leker.heading("Jegy", text="Jegy",
                               command=lambda: foablak.sort_column(treeview_leker, 'Jegy', False))
        treeview_leker.heading("Tantárgy", text="Tantárgy",
                               command=lambda: foablak.sort_column(treeview_leker, 'Tantárgy', False))
        treeview_leker.heading("Dátum", text="Dátum",
                               command=lambda: foablak.sort_column(treeview_leker, 'Dátum', False))
        treeview_leker.column("Jegy", width=35, anchor="center")
        treeview_leker.column("Tantárgy", width=250, anchor="center")
        treeview_leker.column("Dátum", width=80, anchor="center")
        treeview_leker.grid(row=0, column=0, padx=(15, 0), pady=15)
        scrollbar_leker = tk.Scrollbar(lekerdezes_ablak_lista_frame, orient="vertical", command=treeview_leker.yview)
        treeview_leker.configure(yscrollcommand=scrollbar_leker.set)
        scrollbar_leker.grid(row=0, column=1, sticky="ns")
        # jegyek
        lekerdezes_ablak_jegyek_frame = LabelFrame(lekerdezes_ablak_foframe, borderwidth=1, relief=RIDGE,
                                                   text=f"Érdemjegyek - {len(self.erdemjegyek)} db")
        lekerdezes_ablak_jegyek_frame.grid(row=0, column=1, padx=5, pady=(10, 5), sticky="news")
        erdemjegyek_frame = LabelFrame(lekerdezes_ablak_jegyek_frame)
        erdemjegyek_frame.pack(padx=5, pady=5, expand=1)

        # tantárgyak
        lekerdezes_ablak_tantargyak_frame = LabelFrame(lekerdezes_ablak_foframe, borderwidth=1, relief=RIDGE,
                                                       text=f"Tantárgyak - {len(self.tantargyak)} db")
        lekerdezes_ablak_tantargyak_frame.grid(row=1, column=1, padx=5, pady=(5, 10), sticky="news")
        if self.nev == "Márk":
            results_text_leker = tk.Text(lekerdezes_ablak_tantargyak_frame, height=len(self.tantargyak),
                                         width=36, font=("Consolas", 10))
        elif self.nev == "Petra":
            results_text_leker = tk.Text(lekerdezes_ablak_tantargyak_frame, height=len(self.tantargyak),
                                         width=24, font=("Consolas", 10))
        else:
            results_text_leker = tk.Text(lekerdezes_ablak_tantargyak_frame, height=len(self.tantargyak),
                                         width=24, font=("Consolas", 10))
        results_text_leker.pack(padx=10, pady=10, expand=1)

        self.penzek_frissitese(self.erdemjegyek)
        rendezett_lista = sorted(self.erdemjegyek, key=lambda x_: datetime.datetime.strptime(x_[0], "%Y.%m.%d"),
                                 reverse=True)

        # lista kiir
        for i in rendezett_lista:
            treeview_leker.insert('', tk.END, values=i)
        # jegyek kiir

        jegyek = {}  # Dictionary to store grade counts
        osszeg = 0
        darab = 0
        for elem in self.erdemjegyek:
            osszeg += int(elem[2])
            darab += 1
            if elem[2] in jegyek:
                jegyek[elem[2]] += 1
            else:
                jegyek[elem[2]] = 1

        tatlag = osszeg / darab
        if tatlag >= 4:
            tatlag_szin = "red"
        elif tatlag >= 3:
            tatlag_szin = "green"
        elif tatlag >= 2:
            tatlag_szin = "blue"
        else:
            tatlag_szin = "black"

        for jegy in range(5, 0, -1):
            db = jegyek.get(jegy, 0)
            if db > 0:
                jegy_label = tk.Label(erdemjegyek_frame, text=f"{jegy}\t{db}  db")
                jegy_label.pack(padx=20)

        separator_jegyek = ttk.Separator(erdemjegyek_frame)
        separator_jegyek.pack(fill="x", padx=10, pady=5)
        atlag_label = tk.Label(erdemjegyek_frame, text=f"Tanulmányi átlag: {tatlag:.2f}", fg=tatlag_szin)
        atlag_label.pack(padx=20)

        # tantárgyak kiir
        results_text_leker.config(state="normal")
        results_text_leker.delete(1.0, "end")
        for i, tantargy in enumerate(self.tantargyak):
            results_text_leker.insert(tk.END, tantargy)
            if i < len(self.tantargyak) - 1:
                results_text_leker.insert(tk.END, "\n")
        results_text_leker.config(state="disabled")
        lekerdezes_ablak_stat_frame = LabelFrame(lekerdezes_ablak_foframe, borderwidth=1, relief=RIDGE,
                                                 text=f"Statisztikák")
        lekerdezes_ablak_stat_frame.grid(row=1, column=2, padx=(5, 10), pady=(5, 10), sticky="news")
        sor = (self.stat.shape[0])
        max_row_length = self.stat.apply(lambda row: len(' '.join(map(str, row))), axis=1).max()
        count_row_values = self.stat.apply(lambda row: len(row), axis=1).max()
        stat_text = tk.Text(lekerdezes_ablak_stat_frame, width=max_row_length + count_row_values + 5, height=sor + 1,
                            font=("Consolas", 10))

        stat_text.pack(padx=10, pady=10)
        text_kiir = self.stat.to_string(index=False)
        stat_text.insert("1.0", text_kiir)
        kituno, bukovari = 0, 0
        for i in range(self.stat.shape[0]):
            tag = get_tag_for_row(self.stat.iloc[i])
            stat_text.tag_add(tag, f"{i + 2}.0", f"{i + 2}.end")
            stat_text.tag_config(tag, foreground=tag)
            if tag == 'red':
                kituno += 1
            elif tag == 'blue':
                bukovari += 1
        stat_text.tag_add("start", "1.0", "2.0")
        stat_text.tag_config("start", background="#818589", foreground="white")
        stat_text.config(state="disabled")
        if kituno == len(self.stat):
            lekerdezes_ablak_lista_frame.config(text=f"{self.nev} - kitűnő tanuló")
            lekerdezes_ablak_stat_frame.config(text=f"Statisztikák - kitűnő tanuló")
        if bukovari:
            lekerdezes_ablak_lista_frame.config(text=f"{self.nev} - bukásveszély")
            lekerdezes_ablak_stat_frame.config(text=f"Statisztikák - bukásveszély {bukovari} tantárgyból")
        # zsebpénzek kiíratása
        lekerdezes_ablak_zsp_frame = LabelFrame(lekerdezes_ablak_foframe, borderwidth=1, relief=RIDGE,
                                                text=f"Havi zsebpénzek")
        lekerdezes_ablak_zsp_frame.grid(row=0, column=2, padx=(5, 10), pady=(10, 5), sticky="news")
        zsp_frame = LabelFrame(lekerdezes_ablak_zsp_frame)
        zsp_frame.pack(padx=5, pady=5, expand=1)

        kerdes_m = [szam_m[0][:7] for szam_m in self.erdemjegyek if szam_m[0][:7] not in self.erdemjegyek]
        honapok = sorted(set(kerdes_m))
        osszeszsp = 0
        for h, honap in enumerate(honapok):
            talal = [product for product in self.erdemjegyek if honap in product[0]]
            self.penzek_frissitese(talal)
            if self.zsebpenz > 0:
                osszeszsp += self.zsebpenz
            fsp = "{:,}".format(self.zsebpenz).replace(",", ".")
            zsph_label = tk.Label(zsp_frame, text=honap)
            zsph_label.grid(row=h, column=0, padx=10)
            zspp_label = tk.Label(zsp_frame, text=fsp)
            zspp_label.grid(row=h, column=1, padx=10)
        fsop = "{:,}".format(osszeszsp).replace(",", ".")
        separator_jegyek = ttk.Separator(zsp_frame)
        separator_jegyek.grid(row=h + 1, column=0, columnspan=2, sticky="ew", padx=10)
        zspossz_label = tk.Label(zsp_frame, text="Összesen:")
        zspossz_label.grid(row=h + 2, column=0, padx=10)
        zsposszp_label = tk.Label(zsp_frame, text=fsop)
        zsposszp_label.grid(row=h + 2, column=1, padx=10)

    def havi(self, aktho):
        # havi főablak
        havi_lekerdezes_ablak = tk.Toplevel(root)
        havi_lekerdezes_ablak.title(f' Havi lekérdezés - {self.nev} - {aktho}')
        havi_lekerdezes_ablak.wm_attributes("-topmost", 1)
        havi_lekerdezes_ablak.bind("<Escape>", on_escape)
        lekerdezes_ablak_frame = Frame(havi_lekerdezes_ablak)
        lekerdezes_ablak_frame.pack(expand=1)
        # lista
        lista_frame = LabelFrame(lekerdezes_ablak_frame, borderwidth=1, relief=RIDGE)
        lista_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 5))
        treeview_havi = ttk.Treeview(lista_frame, show="headings",
                                     columns=cols_havi, height=15)
        treeview_havi.heading("Jegy", text="Jegy", command=lambda: foablak.sort_column(treeview_havi, 'Jegy', False))
        treeview_havi.heading("Tantárgy", text="Tantárgy",
                              command=lambda: foablak.sort_column(treeview_havi, 'Tantárgy', False))
        treeview_havi.heading("Dátum", text="Nap",
                              command=lambda: foablak.sort_column(treeview_havi, 'Dátum', False))
        treeview_havi.heading("Pénz", text="Pénz",
                              command=lambda: foablak.sort_column(treeview_havi, 'Pénz', False))
        treeview_havi.heading("Zsebpénz", text="Zsebpénz",
                              command=lambda: foablak.sort_column(treeview_havi, 'Zsebpénz', False))
        treeview_havi.column("Jegy", width=35, anchor="center")
        treeview_havi.column("Tantárgy", width=250, anchor="center")
        treeview_havi.column("Dátum", width=40, anchor="center")
        treeview_havi.column("Pénz", width=40, anchor="center")
        treeview_havi.column("Zsebpénz", width=43, anchor="center")
        treeview_havi.grid(row=0, column=0, padx=(15, 0), pady=15)
        scrollbar_havi = tk.Scrollbar(lista_frame, orient="vertical", command=treeview_havi.yview)
        treeview_havi.configure(yscrollcommand=scrollbar_havi.set)
        scrollbar_havi.grid(row=0, column=1, sticky="ns")

        # havi pénz
        honap_penz_jegyek_frame = LabelFrame(lekerdezes_ablak_frame, borderwidth=1, relief=RIDGE)
        honap_penz_jegyek_frame.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="news")

        honap_penz_frame = LabelFrame(honap_penz_jegyek_frame)
        honap_penz_frame.pack(padx=10, pady=(10, 5), expand=True)
        alapzsebpenz_label = tk.Label(honap_penz_frame)
        alapzsebpenz_label.grid(row=1, column=0)
        havizsebpenz_label = tk.Label(honap_penz_frame)
        havizsebpenz_label.grid(row=2, column=0)
        separator_zsebpenz = ttk.Separator(honap_penz_frame)
        separator_zsebpenz.grid(row=3, column=0, sticky="ew")
        kulonbozetzsebpenz_label = tk.Label(honap_penz_frame)
        kulonbozetzsebpenz_label.grid(row=4, column=0)
        for widget_jegyek in honap_penz_frame.winfo_children():
            if widget_jegyek == separator_zsebpenz:
                widget_jegyek.grid_configure(padx=10, pady=5)
            else:
                widget_jegyek.grid_configure(padx=10, pady=1)
        # havi jegyek
        honap_jegyek_frame = LabelFrame(honap_penz_jegyek_frame)
        honap_jegyek_frame.pack(padx=10, pady=(5, 10), expand=True, fill="x")

        valasztotthonap = aktho
        lista_frame.config(text=f"Havi érdemjegyek - {valasztotthonap}")
        honap_penz_jegyek_frame.config(text=f"Havi zsebpénz - {valasztotthonap}")
        talalatok = [product for product in self.erdemjegyek if valasztotthonap in product[0]]

        if talalatok:
            fap = "{:,}".format(self.kezdopenz).replace(",", ".")
            alapzsebpenz_label.config(text=f"Alap zsebpénz: {fap} Ft")
            rendezett_lista = sorted(talalatok, key=lambda x_: datetime.datetime.strptime(x_[0], "%Y.%m.%d"))
            # lista kiir
            ertekek_ = {5: 300, 4: 100, 3: -200, 2: -500, 1: -1000}
            zsebpenz_kezdo = self.kezdopenz
            for jegy in rendezett_lista:
                datum, tantargy, jegy_szoveg = jegy
                jegy_szam = int(jegy_szoveg)
                penz = ertekek_.get(jegy_szam, 0)
                zsebpenz_kezdo += penz
                treeview_havi.insert("", "end", values=(datum[-2:], tantargy, jegy_szoveg, penz, zsebpenz_kezdo))

            self.penzek_frissitese(talalatok)
            fsp = "{:,}".format(self.zsebpenz).replace(",", ".")
            kulonbozet = self.zsebpenz - self.kezdopenz
            fkp = "{:,}".format(kulonbozet).replace(",", ".")
            # pénz kiir
            if self.zsebpenz > self.kezdopenz:
                havizsebpenz_szin = "blue"
            elif self.zsebpenz < self.kezdopenz:
                havizsebpenz_szin = "red"
            else:
                havizsebpenz_szin = "black"
            havizsebpenz_label.config(text=f'Hóvégi zsebpénz: {fsp} Ft', fg=havizsebpenz_szin)
            kulonbozetzsebpenz_label.config(text=f'Különbözet: {fkp} Ft')
            # jegyek kiir
            jegyek = {}  # Dictionary to store grade counts
            osszeg = 0
            darab = 0
            for elem in talalatok:
                osszeg += int(elem[2])
                darab += 1
                if elem[2] in jegyek:
                    jegyek[elem[2]] += 1
                else:
                    jegyek[elem[2]] = 1
            tatlag = osszeg / darab
            if tatlag >= 4:
                tatlag_szin = "red"
            elif tatlag >= 3:
                tatlag_szin = "green"
            elif tatlag >= 2:
                tatlag_szin = "blue"
            else:
                tatlag_szin = "black"
            for jegy in range(5, 0, -1):
                db = jegyek.get(jegy, 0)
                if db > 0:
                    jegy_label = tk.Label(honap_jegyek_frame, text=f"{jegy}\t{db}  db")
                    jegy_label.pack(padx=20)
            separator_jegyek = ttk.Separator(honap_jegyek_frame)
            separator_jegyek.pack(fill="x", padx=10, pady=5)
            jegyek_szama_label = tk.Label(honap_jegyek_frame, text=f"Érdemjegyek száma: {len(talalatok)}")
            jegyek_szama_label.pack()
            atlag_label = tk.Label(honap_jegyek_frame, text=f"Havi átlag: {tatlag:.2f}", fg=tatlag_szin)
            atlag_label.pack()
        else:
            uzenet("Keresés hiba", "Nincs találat a keresésre!")
            # tkinter.messagebox.showwarning(title="Keresés hiba", message="Nincs találat a keresésre!")
        havi_df = self.df[self.df['Dátum'].str.contains(aktho)]
        havi_ = havi_df.groupby(['Tantárgy', 'Jegy']).size().unstack(fill_value=0).reset_index()
        havi__ = havi_df.groupby(['Tantárgy'])['Jegy'].count().reset_index()
        havi__.columns = ['Tantárgy', 'Szum']
        havi___ = havi_df.groupby(['Tantárgy'])['Jegy'].mean().reset_index()
        havi___.columns = ['Tantárgy', 'Átlag']
        havi___["Átlag"] = havi___["Átlag"].apply(lambda x: round(x, 2))
        havi_merged = pd.merge(havi_, havi__, on='Tantárgy')
        havi_stat = pd.merge(havi_merged, havi___, on='Tantárgy').sort_values(by='Átlag', ascending=False)
        honap_stat_frame = LabelFrame(lekerdezes_ablak_frame, borderwidth=1, relief=RIDGE)
        honap_stat_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="news")
        max_row_length = havi_stat.apply(lambda row: len(' '.join(map(str, row))), axis=1).max()
        count_row_values = havi_stat.apply(lambda row: len(row), axis=1).max()
        havi_stat_text = tk.Text(honap_stat_frame, width=max_row_length + count_row_values + 4,
                                 height=havi_stat.shape[0] + 1,
                                 font=("Consolas", 10))
        havi_stat_text.pack(padx=10, pady=10)
        havi_stat_text.insert("1.0", havi_stat.to_string(index=False))
        havi_stat_text.tag_add("start", "1.0", "2.0")
        havi_stat_text.tag_config("start", background="#818589", foreground="white")
        honap_stat_frame.config(text=f"Havi statisztika - {valasztotthonap}")
        havi_stat_text.config(state="disabled")
        kivalogatott_tantargyak = havi___[havi___['Átlag'] == 1.0]['Tantárgy'].to_list()
        if kivalogatott_tantargyak:
            messagebox.showwarning(title=f"{valasztotthonap}., átlag 1,00 alatt",
                                   message="  -  ".join(kivalogatott_tantargyak))


class Window:
    def __init__(self, master):
        self.master = master
        self.k_es = True
        self.df = pd.DataFrame
        self.kereses_tipus_var = None
        self.kereses_betuerzekeny_var = None
        self.kereses_datumban_var = None
        self.honap = date.today().strftime("%Y.%m")

        self.foframe = Frame(root, borderwidth=1, relief=RIDGE)
        self.foframe.pack(padx=10, pady=10, expand=1)
        self.fowidgets_frame = tk.LabelFrame(self.foframe, text="Rögzítés, módosítás, törlés", borderwidth=1,
                                             relief=RIDGE)
        self.fowidgets_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky="ns")
        self.name_combobox = ttk.Combobox(self.fowidgets_frame, values=gyerekek_list, justify="center")
        self.name_combobox.current(0)
        self.name_combobox.grid(row=0, column=0, padx=5, sticky="ew")
        self.jegy_combobox = ttk.Combobox(self.fowidgets_frame, values=jegyek_lista, justify="center")
        self.jegy_combobox.current(0)
        self.jegy_combobox.grid(row=1, column=0, padx=5, sticky="ew")
        self.tantargy_combobox = ttk.Combobox(self.fowidgets_frame, values=tantargyak_list, justify="center")
        self.tantargy_combobox.current(0)
        self.tantargy_combobox.grid(row=2, column=0, sticky="ew")
        self.datum_entry = tk.Entry(self.fowidgets_frame, justify="center")
        self.datum_entry.grid(row=3, column=0, sticky="ew")
        self.datum_entry.insert(0, date.today().strftime("%Y.%m.%d"))
        self.temazaro = tk.BooleanVar()
        self.checkbutton = tk.Checkbutton(self.fowidgets_frame, text="Témazáró", variable=self.temazaro)
        self.checkbutton.grid(row=4, column=0, sticky="nsew")

        self.rogzit_button = tk.Button(self.fowidgets_frame, text="Rögzít", command=self.insert_row, height=1)
        self.rogzit_button.grid(row=5, column=0, sticky="nsew")
        self.edit_button = tk.Button(self.fowidgets_frame, text="Módosít", command=self.edit_row, state="disabled",
                                     height=1)
        self.edit_button.grid(row=6, column=0, sticky="nsew")
        self.delete_button = tk.Button(self.fowidgets_frame, text="Töröl", command=self.delete_selected_row,
                                       state="disabled",
                                       height=1)
        self.delete_button.grid(row=7, column=0, sticky="nsew")
        self.treeview_alap = ttk.Treeview(self.fowidgets_frame, show="headings", columns=cols, height=10)
        self.treeview_alap.heading("Név", text="Név",
                                   command=lambda: self.sort_column(self.treeview_alap, 'Név', False))
        self.treeview_alap.heading("Jegy", text="Jegy",
                                   command=lambda: self.sort_column(self.treeview_alap, 'Jegy', False))
        self.treeview_alap.heading("Tantárgy", text="Tantárgy",
                                   command=lambda: self.sort_column(self.treeview_alap, 'Tantárgy', False))
        self.treeview_alap.heading("Dátum", text="Dátum",
                                   command=lambda: self.sort_column(self.treeview_alap, 'Dátum', False))
        self.treeview_alap.column("Név", width=50, anchor="center")
        self.treeview_alap.column("Jegy", width=35, anchor="center")
        self.treeview_alap.column("Tantárgy", width=250, anchor="center")
        self.treeview_alap.column("Dátum", width=80, anchor="center")
        self.treeview_alap.grid(row=0, column=1, rowspan=8, columnspan=3)
        self.treeview_alap.tag_configure('visible', background='white', foreground='black')
        self.treeview_alap.tag_configure('hidden', background='white', foreground='#EAEAEA')
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#818589", foreground="white", relief="raised")
        style.map("Treeview.Heading", background=[('active', 'black')])
        self.treeview_alap["style"] = "Treeview"
        scrollbar = tk.Scrollbar(self.fowidgets_frame, orient="vertical", command=self.treeview_alap.yview)
        self.treeview_alap.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=8, rowspan=8, sticky="ns")
        self.lista_db_label = tk.Label(self.fowidgets_frame, text=0)
        self.lista_db_label.grid(row=8, column=2)
        self.keres_entry = tk.Entry(self.fowidgets_frame)
        self.keres_entry.grid(row=8, column=1)
        for widget in self.fowidgets_frame.winfo_children():
            widget.grid_configure(padx=3, pady=3)

        # Create main frame for searching
        self.kereses_frame = tk.LabelFrame(self.foframe)
        self.kereses_frame.grid(row=1, column=0, columnspan=2, padx=(10, 10), pady=(5, 10), sticky="ew")
        self.keres_frame = tk.LabelFrame(self.kereses_frame, text="Keresett érték(ek)")
        self.keres_frame.grid(row=0, column=5, padx=(5, 10), pady=10, sticky="ew")

        # Create a keresés Treeview widget
        self.kereses_tablazat = ttk.Treeview(self.kereses_frame, columns=cols, show="headings")
        self.kereses_tablazat.heading("Név", text="Név",
                                      command=lambda: self.sort_column(self.kereses_tablazat, 'Név', False))
        self.kereses_tablazat.heading("Jegy", text="Jegy",
                                      command=lambda: self.sort_column(self.kereses_tablazat, 'Jegy', False))
        self.kereses_tablazat.heading("Tantárgy", text="Tantárgy",
                                      command=lambda: self.sort_column(self.kereses_tablazat, 'Tantárgy', False))
        self.kereses_tablazat.heading("Dátum", text="Dátum",
                                      command=lambda: self.sort_column(self.kereses_tablazat, 'Dátum', False))
        self.kereses_tablazat.column("Név", width=50, anchor="center")
        self.kereses_tablazat.column("Jegy", width=35, anchor="center")
        self.kereses_tablazat.column("Tantárgy", width=250, anchor="center")
        self.kereses_tablazat.column("Dátum", width=80, anchor="center")
        self.kereses_tablazat.grid(row=0, column=0, padx=(10, 0), pady=10)
        self.scrollbar_kereses = tk.Scrollbar(self.kereses_frame, orient="vertical",
                                              command=self.kereses_tablazat.yview)
        self.kereses_tablazat.configure(yscrollcommand=self.scrollbar_kereses.set)
        self.scrollbar_kereses.grid(row=0, column=4, padx=(0, 5), pady=10, sticky="ns")
        self.kereses_frame.config(text=f"Keresés - Találat(ok): {len(self.kereses_tablazat.get_children())}")

        # Create a search entry
        self.kereses_mezo = tk.Entry(self.keres_frame, width=35)
        self.kereses_mezo.grid(row=0, column=0, padx=(5, 2.5), pady=(5, 2.5))
        # Create a search button
        self.kereses_gomb = tk.Button(self.keres_frame, text="Keresés", command=self.search, width=10)
        self.kereses_gomb.grid(row=0, column=1, padx=(1, 5), pady=(5, 1))
        # Create a checkbox for case sensitivity
        self.kereses_betuerzekeny_var = tk.BooleanVar()
        self.kereses_betu_erzekeny_checkbox = tk.Checkbutton(self.keres_frame, text="Kis/nagybetű érzékeny",
                                                             variable=self.kereses_betuerzekeny_var)
        self.kereses_betu_erzekeny_checkbox.grid(row=1, column=0, padx=(5, 1), pady=(1, 1))
        # Create a checkbox for indate searching
        self.kereses_datumban_var = tk.BooleanVar(value=False)
        self.kereses_datumban_checkbox = tk.Checkbutton(self.keres_frame, text="Keresés a Dátum oszlopban is",
                                                        variable=self.kereses_datumban_var)
        self.kereses_datumban_checkbox.grid(row=2, column=0, padx=(5, 1), pady=(1, 5))
        # Create a radio button for search type (AND / OR)
        self.kereses_tipus_var = tk.StringVar(value="AND")
        self.kereses_tipus_radio_and = tk.Radiobutton(self.keres_frame, text="ÉS", variable=self.kereses_tipus_var,
                                                      value="AND")
        self.kereses_tipus_radio_or = tk.Radiobutton(self.keres_frame, text="VAGY", variable=self.kereses_tipus_var,
                                                     value="OR",
                                                     state="disabled")
        self.kereses_tipus_radio_and.grid(row=1, column=1, padx=(1, 5), pady=(1, 2.5))
        self.kereses_tipus_radio_or.grid(row=2, column=1, padx=(1, 5), pady=(1, 5))
        # események
        self.kereses_mezo.bind("<KeyRelease>", lambda event: self.search())
        self.kereses_tipus_var.trace_add("write", self.ker_tipus_valtozott)
        self.kereses_datumban_var.trace_add("write", self.ker_tipus_valtozott)
        self.kereses_betuerzekeny_var.trace_add("write", self.ker_tipus_valtozott)
        # zsebpénz rész
        self.fozsebpenz_jegyek = tk.LabelFrame(self.foframe, text=f"Zsebpénzek {self.honap}", borderwidth=1,
                                               relief=RIDGE)
        self.fozsebpenz_jegyek.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="ns")
        self.zsebpenzek_frame = tk.LabelFrame(self.fozsebpenz_jegyek)
        self.zsebpenzek_frame.pack(expand=1, padx=10, pady=1, fill="x")
        self.jegyek_frame = tk.LabelFrame(self.fozsebpenz_jegyek)
        self.jegyek_frame.pack(expand=1, padx=10, pady=1)

    def frissit(self):
        global elso
        for widget_ in self.zsebpenzek_frame.winfo_children():
            widget_.destroy()
        if elso:
            df = pd.read_excel(path)
            elso = False
        else:
            df = pd.DataFrame([self.treeview_alap.item(item, 'values') for item in self.treeview_alap.get_children()],
                              columns=cols)
            df['Jegy'] = df['Jegy'].astype(int)
            df.to_excel(path, index=False)
            df.to_excel('jegyek.xlsx', index=False, sheet_name='technikai', startrow=0, startcol=0)
        self.df = df
        Mark.df = df[df['Név'] == 'Márk'].drop('Név', axis=1)
        Petra.df = df[df['Név'] == 'Petra'].drop('Név', axis=1)
        Dora.df = df[df['Név'] == 'Dóra'].drop('Név', axis=1)
        Mark.erdemjegyek.clear()
        Petra.erdemjegyek.clear()
        Dora.erdemjegyek.clear()
        Mark.erdemjegyek = Mark.df.values.tolist()
        Petra.erdemjegyek = Petra.df.values.tolist()
        Dora.erdemjegyek = Dora.df.values.tolist()
        for widget_ in self.jegyek_frame.winfo_children():
            widget_.destroy()
        talalatok = [product for product in Mark.erdemjegyek if self.honap.lower() in product[0].lower()]
        Mark.penzek_frissitese(talalatok)
        talalatok = [product for product in Petra.erdemjegyek if self.honap.lower() in product[0].lower()]
        Petra.penzek_frissitese(talalatok)
        talalatok = [product for product in Dora.erdemjegyek if self.honap.lower() in product[0].lower()]
        Dora.penzek_frissitese(talalatok)
        sorban = [[Mark.nev, Mark.zsebpenz], [Petra.nev, Petra.zsebpenz], [Dora.nev, Dora.zsebpenz]]
        sorban.sort(key=lambda x_: x_[1], reverse=True)
        for ssz, i in enumerate(sorban):
            fp = "{:,}".format(i[1]).replace(",", ".")
            nev_zsebpenz_label = tk.Label(self.zsebpenzek_frame, text=f'{i[0]}   {fp} Ft')
            nev_zsebpenz_label.pack(expand=1)
        ossz = sum(x for x in (Petra.zsebpenz, Dora.zsebpenz) if x > 0)
        fop = "{:,}".format(ossz).replace(",", ".")
        separator = ttk.Separator(self.zsebpenzek_frame, orient="horizontal")
        separator.pack(fill="x", padx=10)
        osszesen_label = tk.Label(self.zsebpenzek_frame,
                                  text=f'Összesen: {fop} Ft', fg='red')
        osszesen_label.pack(expand=1)
        """
                M_jegyek_szama = Mark.erdemjegyek[Mark.erdemjegyek["Dátum"].str.startswith(self.honap)][
            "Jegy"].value_counts().reindex(range(5, 0, -1), fill_value=0)

        P_jegyek_szama = Petra.erdemjegyek[Petra.erdemjegyek["Dátum"].str.startswith(self.honap)][
            "Jegy"].value_counts().reindex(range(5, 0, -1), fill_value=0)

        D_jegyek_szama = Dora.erdemjegyek[Dora.erdemjegyek["Dátum"].str.startswith(self.honap)][
            "Jegy"].value_counts().reindex(range(5, 0, -1), fill_value=0)

        df_jegyek = pd.DataFrame({
            "Márk": M_jegyek_szama,
            "Petra": P_jegyek_szama,
            "Dóra": D_jegyek_szama
        })

        label = tk.Label(self.jegyek_frame, text=df_jegyek)
        label.pack()
        """
        ot_m = [jegy[2] for jegy in Mark.erdemjegyek if jegy[2] == 5 and self.honap.lower() in jegy[0].lower()]
        negy_m = [jegy[2] for jegy in Mark.erdemjegyek if jegy[2] == 4 and self.honap.lower() in jegy[0].lower()]
        harom_m = [jegy[2] for jegy in Mark.erdemjegyek if jegy[2] == 3 and self.honap.lower() in jegy[0].lower()]
        ketto_m = [jegy[2] for jegy in Mark.erdemjegyek if jegy[2] == 2 and self.honap.lower() in jegy[0].lower()]
        egy_m = [jegy[2] for jegy in Mark.erdemjegyek if jegy[2] == 1 and self.honap.lower() in jegy[0].lower()]
        ot_p = [jegy[2] for jegy in Petra.erdemjegyek if jegy[2] == 5 and self.honap.lower() in jegy[0].lower()]
        negy_p = [jegy[2] for jegy in Petra.erdemjegyek if jegy[2] == 4 and self.honap.lower() in jegy[0].lower()]
        harom_p = [jegy[2] for jegy in Petra.erdemjegyek if jegy[2] == 3 and self.honap.lower() in jegy[0].lower()]
        ketto_p = [jegy[2] for jegy in Petra.erdemjegyek if jegy[2] == 2 and self.honap.lower() in jegy[0].lower()]
        egy_p = [jegy[2] for jegy in Petra.erdemjegyek if jegy[2] == 1 and self.honap.lower() in jegy[0].lower()]
        ot_d = [jegy[2] for jegy in Dora.erdemjegyek if jegy[2] == 5 and self.honap.lower() in jegy[0].lower()]
        negy_d = [jegy[2] for jegy in Dora.erdemjegyek if jegy[2] == 4 and self.honap.lower() in jegy[0].lower()]
        harom_d = [jegy[2] for jegy in Dora.erdemjegyek if jegy[2] == 3 and self.honap.lower() in jegy[0].lower()]
        ketto_d = [jegy[2] for jegy in Dora.erdemjegyek if jegy[2] == 2 and self.honap.lower() in jegy[0].lower()]
        egy_d = [jegy[2] for jegy in Dora.erdemjegyek if jegy[2] == 1 and self.honap.lower() in jegy[0].lower()]
        nevek = [Mark.nev, Petra.nev, Dora.nev]
        akthavijegyek = [["5-ös", len(ot_m), len(ot_p), len(ot_d)], ["4-es", len(negy_m), len(negy_p), len(negy_d)],
                         ["3-as", len(harom_m), len(harom_p), len(harom_d)],
                         ["2-es", len(ketto_m), len(ketto_p), len(ketto_d)],
                         ["1-es", len(egy_m), len(egy_p), len(egy_d)]]
        r, c = 0, 1
        for nev in nevek:
            label = tk.Label(self.jegyek_frame, text=f"{nev}")
            if c < len(nevek):
                label.grid(row=r, column=c)
            label.grid(row=r, column=c, padx=(0, 10))
            c += 1
        r += 1
        c = 0
        separator_jegyek = ttk.Separator(self.jegyek_frame, orient="horizontal")
        separator_jegyek.grid(row=r, column=c, columnspan=4, padx=10, sticky="ew")
        r += 1
        for jegyek in akthavijegyek:
            c = 0
            for jegy in jegyek:
                if jegy == jegyek[0]:
                    label = tk.Label(self.jegyek_frame, text=f"{jegy}")
                    label.grid(row=r, column=c, padx=(15, 0))
                else:
                    label = tk.Label(self.jegyek_frame, text=f"{jegy}")
                    label.grid(row=r, column=c)
                c += 1
            r += 1
        self.treeview_alap.delete(*self.treeview_alap.get_children())
        for index, row in df.sort_values(by='Dátum').iterrows():
            row.fillna("", inplace=True)
            self.treeview_alap.insert("", "end", values=row.tolist())

        self.kereses_tablazat.delete(*self.kereses_tablazat.get_children())
        for index, row in df.sort_values(by='Dátum', ascending=False).iterrows():
            self.kereses_tablazat.insert("", "end", values=row.tolist())
        self.kereses_frame.config(text=f"Keresés - Találat(ok): {len(self.kereses_tablazat.get_children())}")
        bejegyzesek = self.treeview_alap.get_children()
        db = f"Bejegyzések száma: {len(bejegyzesek)} db"
        self.lista_db_label.config(text=db)

        mark_df_friss = df[df['Név'] == 'Márk']
        petra_df_friss = df[df['Név'] == 'Petra']
        dora_df_friss = df[df['Név'] == 'Dóra']

        mark_friss = mark_df_friss.groupby(['Tantárgy', 'Jegy']).size().unstack(fill_value=0).reset_index()
        mark__friss = mark_df_friss.groupby(['Tantárgy'])['Jegy'].count().reset_index()
        mark__friss.columns = ['Tantárgy', 'Darab']
        mark___friss = mark_df_friss.groupby(['Tantárgy'])['Jegy'].mean().reset_index()
        mark___friss.columns = ['Tantárgy', 'Átlag']
        mark___friss["Átlag"] = mark___friss["Átlag"].apply(lambda x: round(x, 2))
        mark_mergedfriss = pd.merge(mark_friss, mark__friss, on='Tantárgy')
        Mark.stat = pd.merge(mark_mergedfriss, mark___friss, on='Tantárgy').sort_values(by='Átlag', ascending=False)

        petra_friss = petra_df_friss.groupby(['Tantárgy', 'Jegy']).size().unstack(fill_value=0).reset_index()
        petra__friss = petra_df_friss.groupby(['Tantárgy'])['Jegy'].count().reset_index()
        petra__friss.columns = ['Tantárgy', 'Darab']
        petra___friss = petra_df_friss.groupby(['Tantárgy'])['Jegy'].mean().reset_index()
        petra___friss.columns = ['Tantárgy', 'Átlag']
        petra___friss["Átlag"] = petra___friss["Átlag"].apply(lambda x: round(x, 2))
        petra_merged_friss = pd.merge(petra_friss, petra__friss, on='Tantárgy')
        Petra.stat = pd.merge(petra_merged_friss, petra___friss, on='Tantárgy').sort_values(by='Átlag', ascending=False)

        dora_friss = dora_df_friss.groupby(['Tantárgy', 'Jegy']).size().unstack(fill_value=0).reset_index()
        dora__friss = dora_df_friss.groupby(['Tantárgy'])['Jegy'].count().reset_index()
        dora__friss.columns = ['Tantárgy', 'Darab']
        dora___friss = dora_df_friss.groupby(['Tantárgy'])['Jegy'].mean().reset_index()
        dora___friss.columns = ['Tantárgy', 'Átlag']
        dora___friss["Átlag"] = dora___friss["Átlag"].apply(lambda x: round(x, 2))
        dora_merged_friss = pd.merge(dora_friss, dora__friss, on='Tantárgy')
        Dora.stat = pd.merge(dora_merged_friss, dora___friss, on='Tantárgy').sort_values(by='Átlag', ascending=False)

    def search(self):
        # Ha a kereses_mezo nem tartalmaz szóközt, inaktív állapotba helyezzük a vagy_button-t
        if " " not in self.kereses_mezo.get():
            self.kereses_tipus_radio_or.config(state="disabled")
            self.kereses_tipus_var.set("AND")
        else:
            self.kereses_tipus_radio_or.config(state="normal")
        query = self.kereses_mezo.get()
        case_sensitive = self.kereses_betuerzekeny_var.get()
        date_search = self.kereses_datumban_var.get()

        # Convert query to lowercase if case_sensitive is False
        if not case_sensitive:
            query = query.lower()

        self.kereses_tablazat.delete(*self.kereses_tablazat.get_children())
        for index, row in self.df.iterrows():
            row["Jegy"] = str(row["Jegy"])
            if date_search:
                if self.kereses_tipus_var.get() == "AND":
                    # Search using AND logic
                    if all((query_word in row["Dátum"].lower() or query_word in row["Tantárgy"].lower() or query_word in
                            row["Jegy"].lower() or query_word in row["Név"].lower()) if not case_sensitive else
                           (query_word in row["Dátum"] or query_word in row["Tantárgy"] or query_word in row["Jegy"] or
                            query_word in row["Név"]) for query_word in query.split()):
                        self.kereses_tablazat.insert("", "end",
                                                     values=(row["Dátum"], row["Tantárgy"], row["Jegy"], row["Név"]))
                else:
                    # Search using OR logic
                    if any((query_word in row["Dátum"].lower() or query_word in row["Tantárgy"].lower() or query_word in
                            row["Jegy"].lower() or query_word in row["Név"].lower()) if not case_sensitive else
                           (query_word in row["Dátum"] or query_word in row["Tantárgy"] or query_word in row["Jegy"] or
                            query_word in row["Név"]) for query_word in query.split()):
                        self.kereses_tablazat.insert("", "end",
                                                     values=(row["Dátum"], row["Tantárgy"], row["Jegy"], row["Név"]))
            else:
                if self.kereses_tipus_var.get() == "AND":
                    # Search using AND logic
                    if all((query_word in row["Tantárgy"].lower() or query_word in
                            row["Jegy"].lower() or query_word in row["Név"].lower()) if not case_sensitive else
                           (query_word in row["Tantárgy"] or query_word in row["Jegy"] or
                            query_word in row["Név"]) for query_word in query.split()):
                        self.kereses_tablazat.insert("", "end",
                                                     values=(row["Dátum"], row["Tantárgy"], row["Jegy"], row["Név"]))
                else:
                    # Search using OR logic
                    if any((query_word in row["Tantárgy"].lower() or query_word in
                            row["Jegy"].lower() or query_word in row["Név"].lower()) if not case_sensitive else
                           (query_word in row["Tantárgy"] or query_word in row["Jegy"] or
                            query_word in row["Név"]) for query_word in query.split()):
                        self.kereses_tablazat.insert("", "end",
                                                     values=(row["Dátum"], row["Tantárgy"], row["Jegy"], row["Név"]))
        self.kereses_frame.config(text=f"Keresés - Találat(ok): {len(self.kereses_tablazat.get_children())}")

    def ker_tipus_valtozott(self, var, index, mode):
        self.search()

    def insert_row(self):
        nev_helyes, datum_helyes, tantargy_helyes, jegy_helyes = False, False, False, False
        nev = self.name_combobox.get()
        if nev == Mark.nev or nev == Petra.nev or nev == Dora.nev:
            nev_helyes = True
        else:
            uzenet("Név hiba", "Nincs ilyen nevű tanuló!")
        jegy = self.jegy_combobox.get()
        try:
            jegy = int(jegy)
            if 1 <= jegy <= 5:
                jegy = str(jegy)
                jegy_helyes = True
            else:
                uzenet("Érdemjegy hiba", "Megengedett érdemjegy tartomány: 1 - 5 !")

        except ValueError:
            uzenet("Érdemjegy hiba", "Érvénytelen érdemjegy!")
            # tkinter.messagebox.showwarning(title="Érdemjegy hiba", message="Érvénytelen érdemjegy!")
        tantargy = self.tantargy_combobox.get()
        if tantargy in tantargyak_list:
            tantargy_helyes = True
        else:
            uzenet("Tantárgy hiba", "Nincs ilyen tantárgy!")
        datum = self.datum_entry.get()
        try:
            datum = ''.join(filter(str.isdigit, datum))
            date_obj = datetime.datetime.strptime(datum, "%Y%m%d")
            if "20240901" <= datum <= "20250630":
                datum = date_obj.strftime('%Y.%m.%d')
                datum_helyes = True
            else:
                uzenet("Dátum hiba", "Megengedett tartomány: 2024.09.01 - 2025.06.30!")
        except ValueError:
            uzenet("Dátumm hiba", "Érvénytelen dátumformátum!")
        if nev_helyes and datum_helyes and tantargy_helyes and jegy_helyes:
            uj_ertek = [datum, tantargy, jegy, nev]
            self.treeview_alap.insert('', tk.END, values=uj_ertek)
            if self.temazaro.get():
                self.treeview_alap.insert('', tk.END, values=uj_ertek)
            uzenet("Rögzítés", f"{nev}\n{datum} {tantargy} {jegy}\nrögzítve")
            # Clear the values
            self.datum_entry.delete(0, "end")
            self.datum_entry.insert(0, date.today().strftime("%Y.%m.%d"))
            self.treeview_alap.focus(self.treeview_alap.get_children()[-1])
            self.treeview_alap.selection_set(self.treeview_alap.get_children()[-1])
            self.checkbutton.deselect()
            self.frissit()

    def edit_row(self):
        nev_helyes, datum_helyes, tantargy_helyes, jegy_helyes = False, False, False, False
        selected_item = self.treeview_alap.selection()[0]
        if selected_item:
            nev = self.name_combobox.get()
            if nev == Mark.nev or nev == Petra.nev or nev == Dora.nev:
                nev_helyes = True
            else:
                uzenet("Név hiba", "Nincs ilyen nevű tanuló!")
                # tkinter.messagebox.showwarning(title="Név hiba", message="Nincs ilyen nevű tanuló!")
            datum = self.datum_entry.get()
            try:
                datum = ''.join(filter(str.isdigit, datum))
                date_obj = datetime.datetime.strptime(datum, "%Y%m%d")
                if "20240901" <= datum <= "20250630":
                    datum = date_obj.strftime('%Y.%m.%d')
                    datum_helyes = True
                else:
                    uzenet("Dátum hiba", "Megengedett tartomány: 2024.09.01 - 2025.06.30!")
                    # tkinter.messagebox.showwarning(title="Dátum hiba",
                    # message="Megengedett tartomány: 2024.09.01 - 2025.06.30!")
            except ValueError:
                uzenet("Dátumm hiba", "Érvénytelen dátumformátum!")
                # tkinter.messagebox.showwarning(title="Dátumm hiba", message="Érvénytelen dátumformátum!")
            tantargy = self.tantargy_combobox.get()
            if tantargy in tantargyak_list:
                tantargy_helyes = True
            else:
                uzenet("Tantárgy hiba", "Nincs ilyen tantárgy!")
                # tkinter.messagebox.showwarning(title="Tantárgy hiba", message="Nincs ilyen tantárgy!")
            jegy = self.jegy_combobox.get()
            try:
                jegy = int(jegy)
                if 1 <= jegy <= 5:
                    jegy = str(jegy)
                    jegy_helyes = True
                else:
                    uzenet("Érdemjegy hiba", "Megengedett érdemjegy tartomány: 1 - 5!")

            except ValueError:
                uzenet("Érdemjegy hiba", "Érvénytelen érdemjegy!")
                # tkinter.messagebox.showwarning(title="Érdemjegy hiba", message="Érvénytelen érdemjegy!")
            if nev_helyes and datum_helyes and tantargy_helyes and jegy_helyes:
                new_values = [datum, tantargy, jegy, nev]
                self.treeview_alap.item(selected_item, values=new_values)
                uzenet("Módosítás", f"{nev}\n{datum} {tantargy} {jegy}\nmódosítva")
        else:
            uzenet("Módosítási hiba", "Nincs sor kijelölve!")
        self.frissit()
        item_unselected()

    def delete_selected_row(self):
        selected_item = self.treeview_alap.selection()[0]
        if selected_item:
            current_values = self.treeview_alap.item(selected_item)["values"]
            self.treeview_alap.delete(selected_item)
            uzenet("Törlés",
                   f"{current_values[3]}\n{current_values[0]} {current_values[1]} {current_values[2]}\ntörölve")
        else:
            uzenet("Törlési hiba", "Nincs sor kijelölve!")
        self.frissit()

    def sort_column(self, tv, col, reverse):  # sorbarendezés
        data = [(tv.set(k, col), k) for k in tv.get_children('')]
        data.sort(reverse=reverse)
        for index, (val, k) in enumerate(data):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.sort_column(tv, col, not reverse))


def get_tag_for_row(row):
    if row["Átlag"] > 4.50:
        return "red"
    elif row["Átlag"] < 2:
        return "blue"
    else:
        return "black"


def get_tag_for_row2(row):
    if row["Név"] == 'Márk':
        return "blue"
    elif row["Név"] == 'Petra':
        return "#e7547f"
    else:
        return "purple"


def lekerdezes(tanulo):
    if tanulo == Mark.nev:
        Mark.lekerdezes()
    elif tanulo == Petra.nev:
        Petra.lekerdezes()
    elif tanulo == Dora.nev:
        Dora.lekerdezes()


def havi(tanulo, ho):
    if tanulo == Mark.nev:
        Mark.havi(ho)
    elif tanulo == Petra.nev:
        Petra.havi(ho)
    elif tanulo == Dora.nev:
        Dora.havi(ho)


# menúválasztásnál hónapok ellenőrzése
def updatemenu():
    for nevecske in gyerekek_list:
        student_menus[nevecske].delete(0, "end")
        student_menus[nevecske].add_command(label="Tanév", command=lambda student_=nevecske: lekerdezes(student_))
        havi_lekerdezes_menu = tk.Menu(student_menus[nevecske], tearoff=0)
        student_menus[nevecske].add_cascade(label="Havi lekérdezés", menu=havi_lekerdezes_menu)
        if nevecske == "Márk":
            kerdes_m = [szam_m[0][:7] for szam_m in Mark.erdemjegyek if szam_m[0][:7] not in Mark.erdemjegyek]
            akthonap_m = sorted(set(kerdes_m))
            for elem in akthonap_m:
                havi_lekerdezes_menu.add_command(label=elem, command=lambda e=elem: havi(Mark.nev, e))
        elif nevecske == "Petra":
            kerdes_p = [szam_p[0][:7] for szam_p in Petra.erdemjegyek if szam_p[0][:7] not in Petra.erdemjegyek]
            akthonap_p = sorted(set(kerdes_p))
            for elem in akthonap_p:
                havi_lekerdezes_menu.add_command(label=elem, command=lambda e=elem: havi(Petra.nev, e))
        elif nevecske == "Dóra":
            kerdes_d = [szam_d[0][:7] for szam_d in Dora.erdemjegyek if szam_d[0][:7] not in Dora.erdemjegyek]
            akthonap_d = sorted(set(kerdes_d))
            for elem in akthonap_d:
                havi_lekerdezes_menu.add_command(label=elem, command=lambda e=elem: havi(Dora.nev, e))


def uzenet(t, m):
    top_message = Toplevel()
    top_message.wm_attributes("-topmost", 1)
    top_message.title(t)
    messagelabel = tk.Label(top_message, text=m, font=("Times New Roman", 10))
    messagelabel.pack(padx=60, pady=40)
    top_message.after(2000, top_message.destroy)


def tan_stat():
    top_tan_stat = Toplevel()
    top_tan_stat.wm_attributes("-topmost", 1)
    top_tan_stat.title("Tantárgyak - statisztika")
    stat_foframe = tk.Frame(top_tan_stat)
    stat_foframe.pack(expand=1)
    df = pd.read_excel(path)
    df_mark = df.loc[df['Név'] == 'Márk']
    df_mark = df_mark.groupby('Tantárgy').mean('Jegy').round(2)
    df_petra = df.loc[df['Név'] == 'Petra']
    df_petra = df_petra.groupby('Tantárgy').mean('Jegy').round(2)
    df_dora = df.loc[df['Név'] == 'Dóra']
    df_dora = df_dora.groupby('Tantárgy').mean('Jegy').round(2)
    result_ = pd.merge(df_mark, df_petra, on='Tantárgy', how='outer')
    result = pd.merge(result_, df_dora, on='Tantárgy', how='outer')
    result.fillna("-", inplace=True)
    result = result.sort_values('Tantárgy').rename(columns={'Jegy_x': 'Márk', 'Jegy_y': 'Petra', 'Jegy': 'Dóra'})
    result.reset_index(inplace=True)
    max_row_length = result.apply(lambda row: len(' '.join(map(str, row))), axis=1).max()
    count_row_values = result.apply(lambda row: len(row), axis=1).max()
    df_2 = df.groupby(['Név', 'Tantárgy']).mean('Jegy').round(2)
    df_3_atlagok = df.groupby(['Név']).mean('Jegy').round(2)
    df_2.sort_values(['Jegy', 'Név'], ascending=[False, True], inplace=True)
    df_2.rename(columns={'Jegy': 'Átlag'}, inplace=True)
    df_3_atlagok.reset_index(inplace=True)
    df_3_atlagok.rename(columns={'Jegy': 'Átlag'}, inplace=True)
    df_3_atlagok.sort_values('Átlag', ascending=False, inplace=True)
    ossz_tantargy_egyben_frame = tk.LabelFrame(stat_foframe, text="Tantárgy átlag egyben")
    ossz_tantargy_egyben_frame.grid(row=0, column=1, padx=5, pady=5, sticky="news")
    atlagok_egyben = tk.Text(ossz_tantargy_egyben_frame, width=12,
                             height=len(df_3_atlagok) + 1, font=("Consolas", 10))
    atlagok_egyben.pack(padx=10, pady=(5, 10))
    ossz_tantargy_egyben = tk.Text(ossz_tantargy_egyben_frame, width=max_row_length + count_row_values + 6,
                                   height=len(result) + 1, font=("Consolas", 10))
    ossz_tantargy_egyben.pack(padx=10, pady=(10, 5))
    max_value = []
    for i, row in result.iterrows():
        ertek = []
        if row['Márk'] != '-':
            ertek.append(row['Márk'])
        if row['Petra'] != '-':
            ertek.append(row['Petra'])
        if row['Dóra'] != '-':
            ertek.append(row['Dóra'])
        max_value.append(max(ertek))

    ossz_tantargy_egyben.insert("1.0", result.to_string(index=False))

    for i in range(result.shape[0]):
        line_length = len(ossz_tantargy_egyben.get(f"{i + 2}.0", f"{i + 2}.end"))
        if (result.iloc[i]['Márk'] == max_value[i]):
            ossz_tantargy_egyben.tag_add('red', f"{i + 2}.{line_length - 15}", f"{i + 2}.{line_length - 12}")
        if (result.iloc[i]['Petra'] == max_value[i]):
            ossz_tantargy_egyben.tag_add('red', f"{i + 2}.{line_length - 10}", f"{i + 2}.{line_length - 6}")
        if (result.iloc[i]['Dóra'] == max_value[i]):
            ossz_tantargy_egyben.tag_add('red', f"{i + 2}.{line_length - 4}", f"{i + 2}.end")
        ossz_tantargy_egyben.tag_config('red', foreground='red')

    ossz_tantargy_egyben.tag_add("start", "1.0", "2.0")

    ossz_tantargy_egyben.tag_config("start", background="#818589", foreground="white")
    ossz_tantargy_egyben.config(state="disabled")
    atlagok_egyben.insert("1.0", df_3_atlagok.to_string(index=False))
    atlagok_egyben.tag_add("start", "1.0", "2.0")
    atlagok_egyben.tag_config("start", background="#818589", foreground="white")
    atlagok_egyben.config(state="disabled")
    ossz_tantargy_atlagok_frame = tk.LabelFrame(stat_foframe, text="Átlag sorrendben")
    ossz_tantargy_atlagok_frame.grid(row=0, column=0, padx=5, pady=5, sticky="news")
    ossz_tantargy_atlagok = tk.Text(ossz_tantargy_atlagok_frame, width=50,
                                    height=len(df_2) + 1, font=("Consolas", 10))
    ossz_tantargy_atlagok.pack(padx=10, pady=10)
    pd.set_option('display.max_rows', None)  # összes sor mutat
    df_2.reset_index(inplace=True)
    df_2 = df_2.loc[:, ['Átlag', 'Tantárgy', 'Név']]

    above_4_50 = df_2[df_2['Átlag'] > 4.50]
    total_count = len(df_2)
    above_4_50_count = len(above_4_50)
    percentage_above_4_50 = (above_4_50_count / total_count) * 100

    grouped = df_2.groupby('Név')
    above_4_50_counts = grouped.apply(lambda x: (x['Átlag'] > 4.50).sum(), include_groups=False)
    above_4_50_counts.sort_values(ascending=False, inplace=True)
    textcsi = tk.Text(ossz_tantargy_egyben_frame, width=30, height=6, padx=3)
    textcsi.insert(tk.END,
                   f"A {len(df_2)} db tantárgyból {len(above_4_50)} db 5-ös\n- {percentage_above_4_50:.2f}% -\n")
    for nev, darab in above_4_50_counts.items():
        otos_atlag = darab / len(above_4_50) * 100
        if nev == Mark.nev:
            teljes_atlag = darab / len(Mark.tantargyak) * 100
        elif nev == Petra.nev:
            teljes_atlag = darab / len(Petra.tantargyak) * 100
        else:
            teljes_atlag = darab / len(Dora.tantargyak) * 100
        textcsi.insert(tk.END,
                       f"\n{nev}: {darab} db - {otos_atlag:.2f}% ({teljes_atlag:.2f}%)")
    textcsi.pack(pady=10)
    textcsi.config(state='disabled')

    ossz_tantargy_atlagok_frame.config(text=f"A tantárgyak {percentage_above_4_50:.2f}%-a 5-ös")

    ossz_tantargy_atlagok.insert("1.0", df_2.to_string(index=False))

    for i in range(df_2.shape[0]):
        tag = get_tag_for_row2(df_2.iloc[i])
        ossz_tantargy_atlagok.tag_add(tag, f"{i + 2}.0", f"{i + 2}.end")
        ossz_tantargy_atlagok.tag_config(tag, foreground=tag)
    ossz_tantargy_atlagok.tag_add("start", "1.0", "2.0")
    ossz_tantargy_atlagok.tag_config("start", background="#818589", foreground="white")
    ossz_tantargy_atlagok.config(state="disabled")


def set_current_date(_event):
    foablak.datum_entry.delete(0, tk.END)
    foablak.datum_entry.insert(0, date.today().strftime("%Y.%m.%d"))


def close_windows():
    # Minden nyitott ablak bezárása
    for window in root.winfo_children():
        if isinstance(window, tk.Toplevel):
            window.destroy()


def on_escape(_event):
    # Ellenőrizze, hogy van-e nyitott ablak
    open_windows = [window for window in root.winfo_children() if isinstance(window, tk.Toplevel)]
    if open_windows:
        close_windows()
    else:
        root.destroy()


def searching(_event):
    search_by = foablak.keres_entry.get()
    for item in foablak.treeview_alap.get_children():
        values = foablak.treeview_alap.item(item, 'values')
        if search_by.lower() in ' '.join(values).lower():
            foablak.treeview_alap.item(item, tags=('visible',))
        else:
            foablak.treeview_alap.item(item, tags=('hidden',))


def item_unselected():
    selected_item = foablak.treeview_alap.selection()
    if selected_item:
        for selected_item in foablak.treeview_alap.selection():
            foablak.treeview_alap.index(selected_item)
        foablak.name_combobox.delete(0, "end")
        foablak.name_combobox.current(0)
        foablak.jegy_combobox.delete(0, "end")
        foablak.jegy_combobox.current(0)
        foablak.tantargy_combobox.delete(0, "end")
        foablak.tantargy_combobox.config(values=Mark.tantargyak)
        foablak.tantargy_combobox.current(0)
        foablak.datum_entry.delete(0, "end")
        foablak.datum_entry.insert(0, date.today().strftime("%Y.%m.%d"))
        foablak.edit_button.config(state="disabled")
        foablak.delete_button.config(state="disabled")


def item_selected(_event):
    selected_item = foablak.treeview_alap.selection()
    if selected_item:
        for selected_item in foablak.treeview_alap.selection():
            foablak.treeview_alap.index(selected_item)
        current_values = foablak.treeview_alap.item(selected_item)["values"]
        foablak.name_combobox.delete(0, "end")
        foablak.name_combobox.insert(0, current_values[3])
        foablak.jegy_combobox.delete(0, "end")
        foablak.jegy_combobox.insert(0, current_values[2])
        check_name_combobox()
        foablak.tantargy_combobox.set(current_values[1])
        foablak.datum_entry.delete(0, "end")
        foablak.datum_entry.insert(0, current_values[0])
        foablak.edit_button.config(state="normal")
        foablak.delete_button.config(state="normal")


def check_name_combobox():
    global tantargyak_list
    if Mark.nev in foablak.name_combobox.get():
        tantargyak_list = Mark.tantargyak
    elif Petra.nev in foablak.name_combobox.get():
        tantargyak_list = Petra.tantargyak
    elif Dora.nev in foablak.name_combobox.get():
        tantargyak_list = Dora.tantargyak
    foablak.tantargy_combobox.config(values=tantargyak_list)
    foablak.tantargy_combobox.current(0)


# Fájl beolvasása
path = "jegyek_24_45.xlsx"

# Objektumok létrehozása
Mark = Gyerek('Márk', 10000)
Mark.tantargyak = ["Angol nyelv", "Digitális kultúra", "Honvédelem", "IKT projektmunka I.",
                   "Informatikai és távközlési alapok I.", "Irodalom", "Komplex természettudományos tantárgy",
                   "Magatartás", "Magyar nyelv", "Matematika", "Munkavállalói ismeretek", "Művészetek", "Osztályfőnöki",
                   "Programozási alapok", "Szorgalom", "Testnevelés", "Történelem"]
Petra = Gyerek('Petra', 6000)
Petra.tantargyak = ["Angol nyelv", "Digitális kultúra", "Etika/Hit- és erkölcstan", "Ének-zene", "Hon- és népismeret",
                    "Irodalom",
                    "Közösségi nevelés", "Magatartás", "Magyar nyelv", "Matematika", "Szorgalom", "Természettudomány",
                    "Technika és tervezés", "Testnevelés", "Történelem", "Vízuális kultúra"]
Dora = Gyerek('Dóra', 3000)
Dora.tantargyak = ["Digitális kultúra", "Etika/Hit- és erkölcstan", "Ének-zene", "Irodalom", "Környezetismeret",
                   "Magatartás", "Magyar nyelv",
                   "Matematika", "Szorgalom", "Technika és tervezés", "Testnevelés", "Vízuális kultúra"]

gyerekek_list = [Mark.nev, Petra.nev, Dora.nev]
jegyek_lista = ["5", "4", "3", "2", "1"]

cols = ("Dátum", "Tantárgy", "Jegy", "Név")
cols_self = ("Dátum", "Tantárgy", "Jegy")
cols_havi = ("Dátum", "Tantárgy", "Jegy", "Pénz", "Zsebpénz")

tantargyak_list = Mark.tantargyak
studentke = Mark.nev

# Ablak létrehozása
root = tk.Tk()
root.title("Érdemjegyek, havi zsebpénzek - 2024/2025 tanév")
root.wm_attributes("-topmost", 1)
foablak = Window(root)

# Menü létrehozása
# Create student menus
menubar = tk.Menu(root)
root.config(menu=menubar)
student_menus = {}
for student in gyerekek_list:
    student_menus[student] = tk.Menu(menubar, tearoff=0, postcommand=updatemenu)
    menubar.add_cascade(label=student, menu=student_menus[student])
menubar.add_command(label="Tantárgy statisztika", command=tan_stat)
menubar.add_separator()
menubar.add_separator()
menubar.add_command(label="Kilépés", command=root.destroy)

foablak.name_combobox.bind("<<ComboboxSelected>>", lambda event: check_name_combobox())
foablak.treeview_alap.bind('<<TreeviewSelect>>', lambda event: item_unselected())
foablak.treeview_alap.bind("<Double-1>", item_selected)
foablak.treeview_alap.bind("<Delete>", lambda event: foablak.delete_selected_row())
root.bind("<Insert>", lambda event: foablak.edit_row())
foablak.keres_entry.bind("<KeyRelease>", searching)
foablak.datum_entry.bind("<Button-3>", set_current_date)
root.bind("<Escape>", on_escape)
print("Psóra Péter - 2024.")
elso = True
foablak.frissit()
root.mainloop()
