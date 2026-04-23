import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as mfig
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import sys

BG      = "#0f0f0f"
SURFACE = "#1a1a1a"
BORDER  = "#2a2a2a"
TEXT    = "#e0e0e0"
MUTED   = "#666666"
ACCENT  = "#ffffff"
RED     = "#e05c5c"

FONT_MONO = ("Courier New", 10)
FONT_UI   = ("Helvetica", 10)

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_PATH  = os.path.join(BASE_DIR, "ciudades.csv")
CRED_PATH = os.path.join(BASE_DIR, "credenciales.txt")

def style_entry(e, width=28):
    e.configure(
        bg=SURFACE, fg=TEXT, insertbackground=TEXT,
        relief="flat", bd=0, highlightthickness=1,
        highlightbackground=BORDER, highlightcolor=ACCENT,
        font=FONT_UI, width=width
    )

def flat_button(parent, text, cmd, fg=BG, bg=ACCENT, width=None):
    kw = dict(text=text, command=cmd, bg=bg, fg=fg,
              activebackground=MUTED, activeforeground=ACCENT,
              relief="flat", bd=0, cursor="hand2",
              font=("Helvetica", 10, "bold"),
              padx=16, pady=8)
    if width:
        kw["width"] = width
    return tk.Button(parent, **kw)

def label(parent, text, size=10, bold=False, color=TEXT, anchor="w"):
    return tk.Label(parent, text=text, bg=parent["bg"], fg=color,
                    font=("Helvetica", size, "bold" if bold else "normal"),
                    anchor=anchor)

def sep(parent):
    f = tk.Frame(parent, bg=BORDER, height=1)
    f.pack(fill="x")
    return f

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("login")
        self.configure(bg=BG)
        self.resizable(False, False)
        self._build()
        self._center(380, 420)

    def _center(self, w, h):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build(self):
        pad = dict(padx=40)

        tk.Frame(self, bg=BG, height=48).pack()
        label(self, "análisis de ciudades", 18, bold=True, color=ACCENT, anchor="center"
              ).pack(**pad, fill="x")
        label(self, "ingresa tus credenciales", 10, color=MUTED, anchor="center"
              ).pack(**pad, pady=(4, 32), fill="x")

        label(self, "usuario").pack(**pad, fill="x")
        self.e_user = tk.Entry(self)
        style_entry(self.e_user)
        self.e_user.pack(**pad, pady=(4, 16), fill="x", ipady=6)

        label(self, "contraseña").pack(**pad, fill="x")
        self.e_pass = tk.Entry(self, show="•")
        style_entry(self.e_pass)
        self.e_pass.pack(**pad, pady=(4, 4), fill="x", ipady=6)

        self.show_var = tk.BooleanVar()
        ck = tk.Checkbutton(self, text="mostrar contraseña",
                            variable=self.show_var, command=self._toggle,
                            bg=BG, fg=MUTED, selectcolor=BG,
                            activebackground=BG, activeforeground=ACCENT,
                            relief="flat", bd=0, font=FONT_UI,
                            cursor="hand2")
        ck.pack(**pad, anchor="w", pady=(0, 20))

        self.lbl_err = label(self, "", color=RED, anchor="center")
        self.lbl_err.pack(**pad, fill="x")

        btn = flat_button(self, "iniciar sesión →", self._login)
        btn.pack(**pad, pady=(8, 0), fill="x")

        label(self, "admin/admin123  ·  usuario1/pass2024  ·  analista/datos456",
              size=8, color=MUTED, anchor="center").pack(pady=(20, 0))

        self.e_user.bind("<Return>", lambda e: self.e_pass.focus())
        self.e_pass.bind("<Return>", lambda e: self._login())

    def _toggle(self):
        self.e_pass.configure(show="" if self.show_var.get() else "•")

    def _load_creds(self):
        creds = {}
        try:
            with open(CRED_PATH) as f:
                for line in f:
                    if "," in line:
                        u, p = line.strip().split(",", 1)
                        creds[u.strip()] = p.strip()
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró: {CRED_PATH}")
        return creds

    def _login(self):
        u = self.e_user.get().strip()
        p = self.e_pass.get().strip()
        if not u:
            self._err("el usuario no puede estar vacío")
            return
        if not p:
            self._err("la contraseña no puede estar vacía")
            return
        if len(p) < 4:
            self._err("contraseña demasiado corta (mín. 4 caracteres)")
            return
        creds = self._load_creds()
        if creds.get(u) == p:
            self.destroy()
            MainApp(u).mainloop()
        else:
            self._err("usuario o contraseña incorrectos")
            self.e_pass.delete(0, "end")

    def _err(self, msg):
        self.lbl_err.configure(text=f"⚠  {msg}")
        self.after(3000, lambda: self.lbl_err.configure(text=""))

class MainApp(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.df = self._load_data()
        self.title(f"ciudades — {username}")
        self.configure(bg=BG)
        self.state("zoomed")
        self._build_layout()
        self._select(0)

    def _load_data(self):
        try:
            df = pd.read_csv(CSV_PATH, encoding="latin-1")
            df.columns = df.columns.str.strip()
            return df
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró: {CSV_PATH}")
            sys.exit(1)

    def _build_layout(self):
        # Sidebar
        self.sidebar = tk.Frame(self, bg=SURFACE, width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        top = tk.Frame(self.sidebar, bg=SURFACE)
        top.pack(fill="x", padx=20, pady=(24, 16))
        label(top, "CityAnalytics", 13, bold=True, color=ACCENT).pack(anchor="w")
        label(top, f"↳ {self.username}", 9, color=MUTED).pack(anchor="w", pady=(2, 0))

        sep(self.sidebar)

        # Numeración y etiquetas ajustadas a los 10 elementos restantes
        self.queries = [
            ("01", "top 10 población"),
            ("02", "temp vs precipitación"),
            ("03", "pib vs esperanza vida"),
            ("04", "densidad poblacional"),
            ("05", "correlación"),
            ("06", "altitud vs temperatura"),
            ("07", "infraestructura urbana"),
            ("08", "estadísticas"),
            ("09", "comparativa por país"),
            ("10", "mapa de calor"),
        ]

        self.nav_btns = []
        nav = tk.Frame(self.sidebar, bg=SURFACE)
        nav.pack(fill="both", expand=True, pady=8)

        for i, (num, name) in enumerate(self.queries):
            row = tk.Frame(nav, bg=SURFACE, cursor="hand2")
            row.pack(fill="x")
            row.bind("<Button-1>", lambda e, idx=i: self._select(idx))

            n_lbl = tk.Label(row, text=num, bg=SURFACE, fg=MUTED,
                             font=("Courier New", 9), width=4, anchor="e", pady=8)
            n_lbl.pack(side="left", padx=(12, 6))
            n_lbl.bind("<Button-1>", lambda e, idx=i: self._select(idx))

            t_lbl = tk.Label(row, text=name, bg=SURFACE, fg=MUTED,
                             font=FONT_UI, anchor="w")
            t_lbl.pack(side="left")
            t_lbl.bind("<Button-1>", lambda e, idx=i: self._select(idx))

            self.nav_btns.append((row, n_lbl, t_lbl))

        sep(self.sidebar)
        lo = flat_button(self.sidebar, "cerrar sesión", self._logout,
                         fg=RED, bg=SURFACE)
        lo.configure(anchor="w", padx=20)
        lo.pack(fill="x", pady=12)

        right = tk.Frame(self, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        self.titlebar = tk.Frame(right, bg=SURFACE, height=48)
        self.titlebar.pack(fill="x")
        self.titlebar.pack_propagate(False)
        self.lbl_title = tk.Label(self.titlebar, text="", bg=SURFACE, fg=TEXT,
                                  font=("Helvetica", 12, "bold"), anchor="w")
        self.lbl_title.pack(side="left", padx=24, pady=12)
        sep(right)

        content = tk.Frame(right, bg=BG)
        content.pack(fill="both", expand=True)

        self.left_pane = tk.Frame(content, bg=SURFACE, width=400)
        self.left_pane.pack(side="left", fill="y", padx=(16, 8), pady=16)
        self.left_pane.pack_propagate(False)

        self.right_pane = tk.Frame(content, bg=SURFACE)
        self.right_pane.pack(side="left", fill="both", expand=True,
                             padx=(0, 16), pady=16)

    def _select(self, idx):
        for i, (row, n_lbl, t_lbl) in enumerate(self.nav_btns):
            active = (i == idx)
            bg = BG if active else SURFACE
            fg_n = ACCENT if active else MUTED
            fg_t = ACCENT if active else MUTED
            row.configure(bg=bg)
            n_lbl.configure(bg=bg, fg=fg_n)
            t_lbl.configure(bg=bg, fg=fg_t,
                            font=("Helvetica", 10, "bold") if active else FONT_UI)

        num, name = self.queries[idx]
        self.lbl_title.configure(text=f"{num}  {name}")

        for w in self.left_pane.winfo_children():  w.destroy()
        for w in self.right_pane.winfo_children(): w.destroy()

        # Lista actualizada para sincronizar los 10 botones con sus funciones exactas
        [
            self._q1_top_poblacion,
            self._q2_temp_precip,
            self._q3_pib_vida,
            self._q4_densidad,
            self._q6_correlacion,     # Antes era la 06
            self._q7_altitud_temp,    # Antes era la 07
            self._q8_infraestructura, # Antes era la 08
            self._q10_estadisticas,   # Antes era la 10
            self._q11_por_pais,       # Antes era la 11
            self._q12_heatmap,        # Antes era la 12
        ][idx]()

    def _make_fig(self):
        plt.style.use("dark_background")
        fig = mfig.Figure(figsize=(7, 5), facecolor=SURFACE)
        return fig

    def _embed_fig(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self.right_pane)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    def _make_table(self, df_view, title=""):
        if title:
            tk.Label(self.left_pane, text=title, bg=SURFACE, fg=ACCENT,
                     font=("Helvetica", 10, "bold"), anchor="w"
                     ).pack(padx=16, pady=(14, 6), anchor="w")

        frame = tk.Frame(self.left_pane, bg=BORDER)
        frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("M.Treeview",
                        background=SURFACE, foreground=TEXT,
                        fieldbackground=SURFACE, rowheight=24,
                        borderwidth=0, font=("Courier New", 9))
        style.configure("M.Treeview.Heading",
                        background=BG, foreground=MUTED,
                        borderwidth=0, font=("Courier New", 9, "bold"))
        style.map("M.Treeview", background=[("selected", BORDER)])

        cols = list(df_view.columns)
        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            style="M.Treeview", selectmode="browse")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=max(70, min(140, len(col)*11)), anchor="center")
        for _, row in df_view.iterrows():
            vals = [f"{v:,.1f}" if isinstance(v, float) else str(v) for v in row]
            tree.insert("", "end", values=vals)

        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

    def _stat_card(self, parent, label_text, value, color=ACCENT):
        f = tk.Frame(parent, bg=BG, pady=8)
        f.pack(fill="x", padx=12, pady=2)
        tk.Label(f, text=label_text, bg=BG, fg=MUTED,
                 font=("Helvetica", 9), anchor="w").pack(anchor="w", padx=10)
        tk.Label(f, text=value, bg=BG, fg=color,
                 font=("Courier New", 11, "bold"), anchor="w").pack(anchor="w", padx=10)

    def _q1_top_poblacion(self):
        top = self.df.nlargest(10, "poblacion")[["ciudad", "pais", "poblacion"]].copy()
        top["pob_M"] = (top["poblacion"] / 1e6).round(2)
        self._make_table(top[["ciudad", "pais", "pob_M"]].rename(columns={"pob_M": "pob (M)"}),
                         "top 10 ciudades más pobladas")
        self._stat_card(self.left_pane, "mayor población", top.iloc[0]["ciudad"])
        self._stat_card(self.left_pane, "promedio top 10", f"{top['pob_M'].mean():.1f} M", MUTED)

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=SURFACE)
        colors = plt.cm.Greys(np.linspace(0.4, 0.9, len(top)))
        bars = ax.barh(top["ciudad"], top["pob_M"], color=colors, edgecolor="none")
        ax.set_xlabel("Población (millones)", color=MUTED, fontsize=9)
        ax.set_title("Top 10 por Población", color=TEXT, fontsize=11, pad=10)
        ax.tick_params(colors=MUTED, labelsize=8)
        for s in ax.spines.values(): s.set_visible(False)
        ax.xaxis.grid(True, color=BORDER, linewidth=0.5)
        ax.set_axisbelow(True)
        for bar, val in zip(bars, top["pob_M"]):
            ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
                    f"{val:.1f}M", va="center", color=TEXT, fontsize=7)
        fig.tight_layout()
        self._embed_fig(fig)

    def _q2_temp_precip(self):
        df = self.df[["ciudad", "temperatura_media", "precipitacion_mm"]].copy()
        self._make_table(df.rename(columns={"temperatura_media": "temp (°C)",
                                            "precipitacion_mm": "precip (mm)"}),
                         "temperatura y precipitación")
        self._stat_card(self.left_pane, "más cálida",
                        self.df.loc[self.df["temperatura_media"].idxmax(), "ciudad"], RED)
        self._stat_card(self.left_pane, "más húmeda",
                        self.df.loc[self.df["precipitacion_mm"].idxmax(), "ciudad"])
        corr = self.df["temperatura_media"].corr(self.df["precipitacion_mm"])
        self._stat_card(self.left_pane, "correlación", f"{corr:.3f}", MUTED)

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=SURFACE)
        ax.scatter(self.df["temperatura_media"], self.df["precipitacion_mm"],
                   c=self.df["poblacion"], cmap="Greys", s=60, alpha=0.8, edgecolors="none")
        z = np.polyfit(self.df["temperatura_media"], self.df["precipitacion_mm"], 1)
        xs = np.linspace(self.df["temperatura_media"].min(), self.df["temperatura_media"].max(), 100)
        ax.plot(xs, np.poly1d(z)(xs), "--", color=ACCENT, linewidth=1.2, alpha=0.7)
        ax.set_xlabel("Temperatura Media (°C)", color=MUTED, fontsize=9)
        ax.set_ylabel("Precipitación (mm/año)", color=MUTED, fontsize=9)
        ax.set_title("Temperatura vs Precipitación", color=TEXT, fontsize=11, pad=10)
        ax.tick_params(colors=MUTED, labelsize=8)
        for s in ax.spines.values(): s.set_color(BORDER)
        fig.tight_layout()
        self._embed_fig(fig)

    def _q3_pib_vida(self):
        df = self.df[["ciudad", "pais", "pib_per_capita", "esperanza_vida"]].copy()
        self._make_table(df.rename(columns={"pib_per_capita": "pib/cáp (USD)",
                                            "esperanza_vida": "esp. vida (años)"}),
                         "pib vs esperanza de vida")
        self._stat_card(self.left_pane, "mayor pib/cáp.",
                        self.df.loc[self.df["pib_per_capita"].idxmax(), "ciudad"])
        self._stat_card(self.left_pane, "mayor esperanza de vida",
                        self.df.loc[self.df["esperanza_vida"].idxmax(), "ciudad"], MUTED)

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=SURFACE)
        ax.scatter(self.df["pib_per_capita"], self.df["esperanza_vida"],
                   c="#cccccc", s=70, alpha=0.75, edgecolors="none")
        for _, row in self.df.nlargest(5, "pib_per_capita").iterrows():
            ax.annotate(row["ciudad"], (row["pib_per_capita"], row["esperanza_vida"]),
                        fontsize=7, color=MUTED, xytext=(4, 4), textcoords="offset points")
        ax.set_xlabel("PIB per cápita (USD)", color=MUTED, fontsize=9)
        ax.set_ylabel("Esperanza de Vida (años)", color=MUTED, fontsize=9)
        ax.set_title("PIB vs Esperanza de Vida", color=TEXT, fontsize=11, pad=10)
        ax.tick_params(colors=MUTED, labelsize=8)
        for s in ax.spines.values(): s.set_color(BORDER)
        fig.tight_layout()
        self._embed_fig(fig)

    def _q4_densidad(self):
        top = self.df.nlargest(15, "densidad")[["ciudad", "pais", "densidad"]].copy()
        self._make_table(top.rename(columns={"densidad": "densidad (hab/km²)"}),
                         "densidad poblacional (top 15)")
        self._stat_card(self.left_pane, "mayor densidad",
                        self.df.loc[self.df["densidad"].idxmax(), "ciudad"], RED)
        self._stat_card(self.left_pane, "promedio global",
                        f"{self.df['densidad'].mean():,.0f} hab/km²", MUTED)

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=SURFACE)
        vals = top["densidad"].values
        norm = (vals - vals.min()) / (vals.max() - vals.min())
        colors = plt.cm.Greys(0.3 + norm * 0.6)
        ax.bar(range(len(top)), vals, color=colors, edgecolor="none", width=0.7)
        ax.set_xticks(range(len(top)))
        ax.set_xticklabels(top["ciudad"], rotation=45, ha="right", fontsize=7, color=MUTED)
        ax.set_ylabel("Densidad (hab/km²)", color=MUTED, fontsize=9)
        ax.set_title("Top 15 por Densidad", color=TEXT, fontsize=11, pad=10)
        ax.tick_params(colors=MUTED, labelsize=8)
        for s in ax.spines.values(): s.set_visible(False)
        ax.yaxis.grid(True, color=BORDER, linewidth=0.5)
        ax.set_axisbelow(True)
        fig.tight_layout()
        self._embed_fig(fig)

    def _q6_correlacion(self):
        num_cols = ["poblacion", "densidad", "temperatura_media", "precipitacion_mm",
                    "pib_per_capita", "esperanza_vida", "altitud_m", "turistas_anuales"]
        corr_df = self.df[num_cols].corr().round(2)
        self._make_table(corr_df.reset_index().rename(columns={"index": ""}),
                         "matriz de correlación")

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=SURFACE)
        im = ax.imshow(corr_df.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        short = ["Pob.", "Dens.", "Temp.", "Prec.", "PIB", "Vida", "Alt.", "Tur."]
        ax.set_xticks(range(len(short))); ax.set_xticklabels(short, color=MUTED, fontsize=8, rotation=45)
        ax.set_yticks(range(len(short))); ax.set_yticklabels(short, color=MUTED, fontsize=8)
        for i in range(len(short)):
            for j in range(len(short)):
                ax.text(j, i, f"{corr_df.values[i,j]:.2f}",
                        ha="center", va="center",
                        color="white" if abs(corr_df.values[i,j]) > 0.4 else MUTED,
                        fontsize=7)
        ax.set_title("Correlación entre Variables", color=TEXT, fontsize=11, pad=10)
        fig.tight_layout()
        self._embed_fig(fig)

    def _q7_altitud_temp(self):
        df = self.df[["ciudad", "altitud_m", "temperatura_media"]].sort_values("altitud_m", ascending=False)
        self._make_table(df.rename(columns={"altitud_m": "altitud (m)",
                                            "temperatura_media": "temp (°C)"}),
                         "altitud vs temperatura")
        corr = df["altitud_m"].corr(df["temperatura_media"])
        self._stat_card(self.left_pane, "correlación altitud-temp.", f"{corr:.3f}")
        self._stat_card(self.left_pane, "ciudad más alta",
                        self.df.loc[self.df["altitud_m"].idxmax(), "ciudad"], MUTED)

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=SURFACE)
        ax.scatter(self.df["altitud_m"], self.df["temperatura_media"],
                   c="#aaaaaa", s=60, alpha=0.8, edgecolors="none")
        z = np.polyfit(self.df["altitud_m"], self.df["temperatura_media"], 1)
        xs = np.linspace(self.df["altitud_m"].min(), self.df["altitud_m"].max(), 100)
        ax.plot(xs, np.poly1d(z)(xs), "--", color=ACCENT, linewidth=1.2, alpha=0.7)
        for _, row in self.df.nlargest(3, "altitud_m").iterrows():
            ax.annotate(row["ciudad"], (row["altitud_m"], row["temperatura_media"]),
                        fontsize=7, color=MUTED, xytext=(4, 4), textcoords="offset points")
        ax.set_xlabel("Altitud (m)", color=MUTED, fontsize=9)
        ax.set_ylabel("Temperatura Media (°C)", color=MUTED, fontsize=9)
        ax.set_title("Altitud vs Temperatura", color=TEXT, fontsize=11, pad=10)
        ax.tick_params(colors=MUTED, labelsize=8)
        for s in ax.spines.values(): s.set_color(BORDER)
        fig.tight_layout()
        self._embed_fig(fig)

    def _q8_infraestructura(self):
        df = self.df[["ciudad", "universidades", "hospitales", "parques"]].copy()
        df["índice"] = (df["universidades"]*0.4 + df["hospitales"]*0.35 + df["parques"]*0.25).round(1)
        df = df.sort_values("índice", ascending=False).head(15)
        self._make_table(df, "índice de infraestructura (top 15)")

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=SURFACE)
        x = np.arange(len(df)); w = 0.25
        ax.bar(x - w,  df["universidades"], w, label="Universidades", color="#cccccc", alpha=0.9)
        ax.bar(x,      df["hospitales"],    w, label="Hospitales",    color="#888888", alpha=0.9)
        ax.bar(x + w,  df["parques"],       w, label="Parques",       color="#555555", alpha=0.9)
        ax.set_xticks(x)
        ax.set_xticklabels(df["ciudad"], rotation=45, ha="right", fontsize=7, color=MUTED)
        ax.set_title("Infraestructura Urbana (Top 15)", color=TEXT, fontsize=11, pad=10)
        ax.tick_params(colors=MUTED, labelsize=8)
        ax.legend(facecolor=BG, edgecolor=BORDER, labelcolor=TEXT, fontsize=9)
        for s in ax.spines.values(): s.set_visible(False)
        ax.yaxis.grid(True, color=BORDER, linewidth=0.5); ax.set_axisbelow(True)
        fig.tight_layout()
        self._embed_fig(fig)

    def _q10_estadisticas(self):
        num_cols = ["poblacion", "densidad", "temperatura_media", "precipitacion_mm",
                    "pib_per_capita", "esperanza_vida"]
        stats = self.df[num_cols].describe().T[["mean", "std", "min", "max"]].round(1)
        stats.columns = ["media", "desv.std", "mín.", "máx."]
        self._make_table(stats.reset_index().rename(columns={"index": "variable"}),
                         "estadísticas descriptivas")
        self._stat_card(self.left_pane, "total ciudades", str(len(self.df)))
        self._stat_card(self.left_pane, "países representados",
                        str(self.df["pais"].nunique()), MUTED)

        fig = self._make_fig()
        variables = ["poblacion", "pib_per_capita", "esperanza_vida",
                     "densidad", "temperatura_media", "precipitacion_mm"]
        titles    = ["Población", "PIB/cáp.", "Esp. Vida",
                     "Densidad", "Temp.", "Precip."]
        axes_list = fig.subplots(2, 3)
        for ax, col, title in zip(axes_list.flat, variables, titles):
            ax.set_facecolor(SURFACE)
            ax.hist(self.df[col], bins=10, color="#888888", alpha=0.85, edgecolor="none")
            ax.set_title(title, color=TEXT, fontsize=9)
            ax.tick_params(colors=MUTED, labelsize=7)
            for s in ax.spines.values(): s.set_visible(False)
        fig.suptitle("Distribuciones", color=TEXT, fontsize=11, y=1.01)
        fig.tight_layout()
        self._embed_fig(fig)

    def _q11_por_pais(self):
        grupo = self.df.groupby("pais").agg(
            Ciudades=("ciudad", "count"),
            Pob_Total=("poblacion", "sum"),
            PIB_Prom=("pib_per_capita", "mean"),
            Turistas=("turistas_anuales", "sum")
        ).reset_index().sort_values("Pob_Total", ascending=False)
        grupo["Pob_Total"] = (grupo["Pob_Total"] / 1e6).round(1)
        grupo["PIB_Prom"]  = grupo["PIB_Prom"].round(0)
        grupo["Turistas"]  = (grupo["Turistas"] / 1e6).round(1)
        self._make_table(grupo, "comparativa por país")

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=SURFACE)
        norm = (grupo["Pob_Total"] - grupo["Pob_Total"].min()) / (grupo["Pob_Total"].max() - grupo["Pob_Total"].min())
        colors = plt.cm.Greys(0.3 + norm * 0.6)
        ax.barh(grupo["pais"], grupo["Pob_Total"], color=colors, edgecolor="none")
        ax.set_xlabel("Población Total (millones)", color=MUTED, fontsize=9)
        ax.set_title("Población Total por País", color=TEXT, fontsize=11, pad=10)
        ax.tick_params(colors=MUTED, labelsize=8)
        for s in ax.spines.values(): s.set_visible(False)
        ax.xaxis.grid(True, color=BORDER, linewidth=0.5); ax.set_axisbelow(True)
        fig.tight_layout()
        self._embed_fig(fig)

    def _q12_heatmap(self):
        num_cols = ["poblacion", "densidad", "temperatura_media", "precipitacion_mm",
                    "pib_per_capita", "esperanza_vida", "altitud_m", "turistas_anuales",
                    "universidades", "hospitales"]
        df_norm = self.df[num_cols].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
        self._make_table(
            self.df[["ciudad", "pais"]].join(
                df_norm[["pib_per_capita", "esperanza_vida", "turistas_anuales"]].round(2)),
            "variables normalizadas (muestra)")

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=SURFACE)
        im = ax.imshow(df_norm.values.T, cmap="Greys", aspect="auto")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        short_cols = ["Pob.", "Dens.", "Temp.", "Prec.", "PIB", "Vida", "Alt.", "Tur.", "Univ.", "Hosp."]
        ax.set_yticks(range(len(short_cols)))
        ax.set_yticklabels(short_cols, color=MUTED, fontsize=8)
        step = max(1, len(self.df) // 10)
        ax.set_xticks(range(0, len(self.df), step))
        ax.set_xticklabels(self.df["ciudad"].iloc[::step],
                           rotation=45, ha="right", color=MUTED, fontsize=7)
        ax.set_title("Heatmap — Variables Normalizadas", color=TEXT, fontsize=11, pad=10)
        fig.tight_layout()
        self._embed_fig(fig)

    def _logout(self):
        if messagebox.askyesno("Cerrar sesión", "¿Deseas cerrar sesión?"):
            self.destroy()
            LoginWindow().mainloop()

if __name__ == "__main__":
    LoginWindow().mainloop()