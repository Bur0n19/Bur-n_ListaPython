import customtkinter as ctk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as mfig
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import cm
import tkinter as tk
from tkinter import messagebox, ttk
import os
import sys

#Configuración visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ACCENT   = "#00C9FF"
BG_DARK  = "#0D1117"
BG_CARD  = "#161B22"
BG_PANEL = "#1C2128"
TEXT_PRI = "#E6EDF3"
TEXT_SEC = "#8B949E"
SUCCESS  = "#3FB950"
WARNING  = "#D29922"
DANGER   = "#F85149"

#Rutas
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
CSV_PATH   = os.path.join(BASE_DIR, "ciudades.csv")
CRED_PATH  = os.path.join(BASE_DIR, "credenciales.txt")


#PANTALLA DE LOGIN
class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Análisis de Ciudades — Acceso")
        self.geometry("480x560")
        self.resizable(False, False)
        self.configure(fg_color=BG_DARK)
        self._build_ui()
        self.center()

    def center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - 480) // 2
        y = (self.winfo_screenheight() - 560) // 2
        self.geometry(f"480x560+{x}+{y}")

    def _build_ui(self):
        # Título
        ctk.CTkLabel(self, text="🌍", font=("Segoe UI Emoji", 48)).pack(pady=(50, 4))
        ctk.CTkLabel(self, text="Análisis Global de Ciudades",font=ctk.CTkFont("Segoe UI", 22, "bold"),text_color=ACCENT).pack()
        ctk.CTkLabel(self, text="Ingresa tus credenciales para continuar",font=ctk.CTkFont("Segoe UI", 13),text_color=TEXT_SEC).pack(pady=(4, 30))

        frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=16)
        frame.pack(padx=40, fill="x")

        ctk.CTkLabel(frame, text="Usuario", anchor="w",
                     font=ctk.CTkFont("Segoe UI", 13, "bold"),
                     text_color=TEXT_SEC).pack(padx=24, pady=(24, 0), fill="x")
        self.entry_user = ctk.CTkEntry(frame, placeholder_text="Ingresa tu usuario",
                                       height=42, corner_radius=8,
                                       fg_color=BG_PANEL, border_color="#30363D",
                                       text_color=TEXT_PRI, font=ctk.CTkFont("Segoe UI", 14))
        self.entry_user.pack(padx=24, pady=(4, 16), fill="x")

        ctk.CTkLabel(frame, text="Contraseña", anchor="w",
                     font=ctk.CTkFont("Segoe UI", 13, "bold"),
                     text_color=TEXT_SEC).pack(padx=24, fill="x")
        self.entry_pass = ctk.CTkEntry(frame, placeholder_text="Ingresa tu contraseña",
                                       show="●", height=42, corner_radius=8,
                                       fg_color=BG_PANEL, border_color="#30363D",
                                       text_color=TEXT_PRI, font=ctk.CTkFont("Segoe UI", 14))
        self.entry_pass.pack(padx=24, pady=(4, 8), fill="x")

        self.show_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(frame, text="Mostrar contraseña", variable=self.show_var,
                        command=self._toggle_pass,
                        text_color=TEXT_SEC, font=ctk.CTkFont("Segoe UI", 12),
                        checkmark_color=ACCENT, fg_color=ACCENT).pack(padx=24, pady=(0, 20), anchor="w")

        self.lbl_error = ctk.CTkLabel(frame, text="", text_color=DANGER,
                                      font=ctk.CTkFont("Segoe UI", 12))
        self.lbl_error.pack()

        ctk.CTkButton(frame, text="Iniciar sesión →", height=44, corner_radius=10,
                      fg_color=ACCENT, hover_color="#009FCC", text_color=BG_DARK,
                      font=ctk.CTkFont("Segoe UI", 15, "bold"),
                      command=self._login).pack(padx=24, pady=(8, 24), fill="x")

        ctk.CTkLabel(self, text="admin / admin123  •  usuario1 / pass2024  •  analista / datos456",
                     text_color=TEXT_SEC, font=ctk.CTkFont("Segoe UI", 10)).pack(pady=(16, 0))

        self.entry_user.bind("<Return>", lambda e: self.entry_pass.focus())
        self.entry_pass.bind("<Return>", lambda e: self._login())

    def _toggle_pass(self):
        self.entry_pass.configure(show="" if self.show_var.get() else "●")

    def _load_credentials(self):
        creds = {}
        try:
            with open(CRED_PATH, "r") as f:
                for line in f:
                    line = line.strip()
                    if "," in line:
                        user, pwd = line.split(",", 1)
                        creds[user.strip()] = pwd.strip()
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró: {CRED_PATH}")
        return creds

    def _login(self):
        user = self.entry_user.get().strip()
        pwd  = self.entry_pass.get().strip()

        # Validaciones
        if not user:
            self._show_error("El usuario no puede estar vacío.")
            return
        if not pwd:
            self._show_error("La contraseña no puede estar vacía.")
            return
        if len(pwd) < 4:
            self._show_error("La contraseña debe tener al menos 4 caracteres.")
            return

        creds = self._load_credentials()
        if user in creds and creds[user] == pwd:
            self.destroy()
            app = MainApp(user)
            app.mainloop()
        else:
            self._show_error("Usuario o contraseña incorrectos.")
            self.entry_pass.delete(0, "end")

    def _show_error(self, msg):
        self.lbl_error.configure(text=f"⚠ {msg}")
        self.after(3000, lambda: self.lbl_error.configure(text=""))


#Main
class MainApp(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.df = self._load_data()
        self.title(f"Análisis Global de Ciudades — {username}")
        self.geometry("1400x850")
        self.configure(fg_color=BG_DARK)
        self.current_frame = None
        self._build_layout()
        self._show_query(0)
        self.state("zoomed")

    #Datos
    def _load_data(self):
        try:
            df = pd.read_csv(CSV_PATH)
            df.columns = df.columns.str.strip()
            return df
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró: {CSV_PATH}")
            sys.exit(1)

    #Layout
    def _build_layout(self):
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=260, fg_color=BG_CARD, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        header = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(20, 10))
        ctk.CTkLabel(header, text="🌍 CityAnalytics",
                     font=ctk.CTkFont("Segoe UI", 17, "bold"),
                     text_color=ACCENT).pack(anchor="w")
        ctk.CTkLabel(header, text=f"👤 {self.username}",
                     font=ctk.CTkFont("Segoe UI", 12),
                     text_color=TEXT_SEC).pack(anchor="w", pady=(2, 0))

        ctk.CTkFrame(self.sidebar, height=1, fg_color="#30363D").pack(fill="x", padx=16, pady=10)

        ctk.CTkLabel(self.sidebar, text="CONSULTAS",
                     font=ctk.CTkFont("Segoe UI", 10, "bold"),
                     text_color=TEXT_SEC).pack(anchor="w", padx=20, pady=(0, 6))

        self.queries = [
            ("📊", "Top 10 por Población"),
            ("🌡️", "Temperatura vs Precipitación"),
            ("💰", "PIB vs Esperanza de Vida"),
            ("🏙️", "Densidad Poblacional"),
            ("🌊", "Ciudades Costeras vs Interior"),
            ("📈", "Correlación de Variables"),
            ("🏔️", "Altitud vs Temperatura"),
            ("🎓", "Infraestructura Urbana"),
            ("✈️", "Top Destinos Turísticos"),
            ("📉", "Análisis Estadístico"),
            ("🗺️", "Comparativa por País"),
            ("🔥", "Mapa de Calor"),
        ]

        self.btn_vars = []
        for i, (icon, name) in enumerate(self.queries):
            btn = ctk.CTkButton(
                self.sidebar,
                text=f"  {icon}  {name}",
                anchor="w",
                height=38,
                corner_radius=8,
                fg_color="transparent",
                hover_color="#21262D",
                text_color=TEXT_PRI,
                font=ctk.CTkFont("Segoe UI", 13),
                command=lambda idx=i: self._show_query(idx)
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.btn_vars.append(btn)

        # Salir
        ctk.CTkFrame(self.sidebar, height=1, fg_color="#30363D").pack(fill="x", padx=16, pady=10, side="bottom")
        ctk.CTkButton(self.sidebar, text="⏻  Cerrar sesión", anchor="w", height=38,
                      corner_radius=8, fg_color="transparent", hover_color="#3D1515",
                      text_color=DANGER, font=ctk.CTkFont("Segoe UI", 13),
                      command=self._logout).pack(fill="x", padx=12, pady=(0,16), side="bottom")

        # Panel derecho: título + contenido
        right = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=0)
        right.pack(side="left", fill="both", expand=True)

        self.title_bar = ctk.CTkFrame(right, height=64, fg_color=BG_CARD, corner_radius=0)
        self.title_bar.pack(fill="x")
        self.title_bar.pack_propagate(False)

        self.lbl_title = ctk.CTkLabel(self.title_bar, text="",
                                      font=ctk.CTkFont("Segoe UI", 18, "bold"),
                                      text_color=TEXT_PRI)
        self.lbl_title.pack(side="left", padx=24, pady=16)

        content = ctk.CTkFrame(right, fg_color=BG_DARK)
        content.pack(fill="both", expand=True, padx=0)

        self.left_pane = ctk.CTkFrame(content, width=460, fg_color=BG_CARD, corner_radius=12)
        self.left_pane.pack(side="left", fill="y", padx=(16, 8), pady=16)
        self.left_pane.pack_propagate(False)

        self.right_pane = ctk.CTkFrame(content, fg_color=BG_CARD, corner_radius=12)
        self.right_pane.pack(side="left", fill="both", expand=True, padx=(0, 16), pady=16)

    def _show_query(self, idx):
        for i, btn in enumerate(self.btn_vars):
            btn.configure(fg_color=ACCENT if i == idx else "transparent",
                          text_color=BG_DARK if i == idx else TEXT_PRI,
                          font=ctk.CTkFont("Segoe UI", 13, "bold" if i == idx else "normal"))

        icon, name = self.queries[idx]
        self.lbl_title.configure(text=f"{icon}  {name}")

        for w in self.left_pane.winfo_children():  w.destroy()
        for w in self.right_pane.winfo_children(): w.destroy()

        funcs = [
            self._q1_top_poblacion,
            self._q2_temp_precip,
            self._q3_pib_vida,
            self._q4_densidad,
            self._q5_costeras,
            self._q6_correlacion,
            self._q7_altitud_temp,
            self._q8_infraestructura,
            self._q9_turismo,
            self._q10_estadisticas,
            self._q11_por_pais,
            self._q12_heatmap,
        ]
        funcs[idx]()

    #Helpers
    def _make_fig(self):
        plt.style.use("dark_background")
        fig = mfig.Figure(figsize=(7, 5), facecolor=BG_CARD)
        return fig

    def _embed_fig(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self.right_pane)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)

    def _make_table(self, df_view, title="Datos"):
        ctk.CTkLabel(self.left_pane, text=title,
                     font=ctk.CTkFont("Segoe UI", 14, "bold"),
                     text_color=ACCENT).pack(padx=16, pady=(14, 6), anchor="w")

        frame = ctk.CTkFrame(self.left_pane, fg_color=BG_PANEL, corner_radius=8)
        frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("City.Treeview",
                        background=BG_PANEL, foreground=TEXT_PRI,
                        fieldbackground=BG_PANEL, rowheight=26,
                        borderwidth=0, font=("Segoe UI", 11))
        style.configure("City.Treeview.Heading",
                        background=BG_DARK, foreground=ACCENT,
                        borderwidth=0, font=("Segoe UI", 11, "bold"))
        style.map("City.Treeview", background=[("selected", "#21262D")])

        cols = list(df_view.columns)
        tree = ttk.Treeview(frame, columns=cols, show="headings",
                            style="City.Treeview", selectmode="browse")

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=max(80, min(160, len(col)*12)), anchor="center")

        for _, row in df_view.iterrows():
            vals = [str(v) if not isinstance(v, float) else f"{v:,.1f}" for v in row]
            tree.insert("", "end", values=vals)

        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

    def _stat_card(self, parent, label, value, color=ACCENT):
        card = ctk.CTkFrame(parent, fg_color=BG_PANEL, corner_radius=10)
        card.pack(fill="x", padx=12, pady=4)
        ctk.CTkLabel(card, text=label, text_color=TEXT_SEC,
                     font=ctk.CTkFont("Segoe UI", 11)).pack(anchor="w", padx=12, pady=(8, 0))
        ctk.CTkLabel(card, text=value, text_color=color,
                     font=ctk.CTkFont("Segoe UI", 16, "bold")).pack(anchor="w", padx=12, pady=(0, 8))

    #  CONSULTAS

    # Q1 — Top 10 por población
    def _q1_top_poblacion(self):
        top = self.df.nlargest(10, "poblacion")[["ciudad", "pais", "poblacion"]].copy()
        top["poblacion_M"] = (top["poblacion"] / 1e6).round(2)
        self._make_table(top[["ciudad", "pais", "poblacion_M"]].rename(
            columns={"poblacion_M": "Pob. (M)"}), "Top 10 ciudades más pobladas")

        ctk.CTkLabel(self.left_pane, text="Estadísticas",
                     font=ctk.CTkFont("Segoe UI", 13, "bold"),
                     text_color=TEXT_SEC).pack(padx=16, pady=(8, 2), anchor="w")
        self._stat_card(self.left_pane, "Mayor población", top.iloc[0]["ciudad"], ACCENT)
        self._stat_card(self.left_pane, "Promedio Top 10",
                        f"{top['poblacion_M'].mean():.1f} M", WARNING)

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=BG_PANEL)
        colors = plt.cm.cool(np.linspace(0.3, 1.0, len(top)))
        bars = ax.barh(top["ciudad"], top["poblacion_M"], color=colors, edgecolor="none")
        ax.set_xlabel("Población (millones)", color=TEXT_SEC, fontsize=10)
        ax.set_title("Top 10 Ciudades por Población", color=TEXT_PRI, fontsize=13, pad=12)
        ax.tick_params(colors=TEXT_SEC, labelsize=9)
        for spine in ax.spines.values(): spine.set_visible(False)
        ax.xaxis.grid(True, color="#30363D", linewidth=0.6)
        ax.set_axisbelow(True)
        for bar, val in zip(bars, top["poblacion_M"]):
            ax.text(val + 0.1, bar.get_y() + bar.get_height()/2,
                    f"{val:.1f}M", va="center", color=TEXT_PRI, fontsize=8)
        fig.tight_layout()
        self._embed_fig(fig)

    # Q2 — Temperatura vs Precipitación
    def _q2_temp_precip(self):
        df = self.df[["ciudad", "temperatura_media", "precipitacion_mm"]].copy()
        self._make_table(df.rename(columns={"temperatura_media": "Temp (°C)",
                                            "precipitacion_mm": "Precip (mm)"}),
                         "Temperatura y Precipitación")
        self._stat_card(self.left_pane, "Ciudad más cálida",
                        self.df.loc[self.df["temperatura_media"].idxmax(), "ciudad"], DANGER)
        self._stat_card(self.left_pane, "Ciudad más húmeda",
                        self.df.loc[self.df["precipitacion_mm"].idxmax(), "ciudad"], ACCENT)
        corr = self.df["temperatura_media"].corr(self.df["precipitacion_mm"])
        self._stat_card(self.left_pane, "Correlación", f"{corr:.3f}", WARNING)

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=BG_PANEL)
        sc = ax.scatter(self.df["temperatura_media"], self.df["precipitacion_mm"],
                        c=self.df["poblacion"], cmap="plasma",
                        s=80, alpha=0.85, edgecolors="none")
        cb = fig.colorbar(sc, ax=ax)
        cb.set_label("Población", color=TEXT_SEC, fontsize=9)
        cb.ax.yaxis.set_tick_params(color=TEXT_SEC)
        plt.setp(cb.ax.yaxis.get_ticklabels(), color=TEXT_SEC)
        z = np.polyfit(self.df["temperatura_media"], self.df["precipitacion_mm"], 1)
        p = np.poly1d(z)
        xs = np.linspace(self.df["temperatura_media"].min(), self.df["temperatura_media"].max(), 100)
        ax.plot(xs, p(xs), "--", color=ACCENT, linewidth=1.5, alpha=0.8)
        ax.set_xlabel("Temperatura Media (°C)", color=TEXT_SEC, fontsize=10)
        ax.set_ylabel("Precipitación (mm/año)", color=TEXT_SEC, fontsize=10)
        ax.set_title("Temperatura vs Precipitación", color=TEXT_PRI, fontsize=13, pad=12)
        ax.tick_params(colors=TEXT_SEC, labelsize=9)
        for spine in ax.spines.values(): spine.set_color("#30363D")
        fig.tight_layout()
        self._embed_fig(fig)

    # Q3 — PIB vs Esperanza de Vida
    def _q3_pib_vida(self):
        df = self.df[["ciudad", "pais", "pib_per_capita", "esperanza_vida"]].copy()
        self._make_table(df.rename(columns={"pib_per_capita": "PIB/cáp (USD)",
                                            "esperanza_vida": "Esp. Vida (años)"}),
                         "PIB per cápita vs Esperanza de Vida")
        self._stat_card(self.left_pane, "Mayor PIB/cáp.",
                        f"{self.df['pib_per_capita'].max():,.0f} USD — "
                        + self.df.loc[self.df["pib_per_capita"].idxmax(), "ciudad"], ACCENT)
        self._stat_card(self.left_pane, "Mayor esperanza de vida",
                        f"{self.df['esperanza_vida'].max()} años — "
                        + self.df.loc[self.df["esperanza_vida"].idxmax(), "ciudad"], SUCCESS)

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=BG_PANEL)
        colors_c = plt.cm.viridis(
            (self.df["pib_per_capita"] - self.df["pib_per_capita"].min()) /
            (self.df["pib_per_capita"].max() - self.df["pib_per_capita"].min()))
        ax.scatter(self.df["pib_per_capita"], self.df["esperanza_vida"],
                   c=colors_c, s=90, alpha=0.9, edgecolors="none")
        for _, row in self.df.nlargest(5, "pib_per_capita").iterrows():
            ax.annotate(row["ciudad"], (row["pib_per_capita"], row["esperanza_vida"]),
                        fontsize=7, color=TEXT_SEC, xytext=(4, 4), textcoords="offset points")
        ax.set_xlabel("PIB per cápita (USD)", color=TEXT_SEC, fontsize=10)
        ax.set_ylabel("Esperanza de Vida (años)", color=TEXT_SEC, fontsize=10)
        ax.set_title("PIB per cápita vs Esperanza de Vida", color=TEXT_PRI, fontsize=13, pad=12)
        ax.tick_params(colors=TEXT_SEC, labelsize=9)
        for spine in ax.spines.values(): spine.set_color("#30363D")
        fig.tight_layout()
        self._embed_fig(fig)

    # Q4 — Densidad poblacional
    def _q4_densidad(self):
        top = self.df.nlargest(15, "densidad")[["ciudad", "pais", "densidad"]].copy()
        self._make_table(top.rename(columns={"densidad": "Densidad (hab/km²)"}),
                         "Densidad Poblacional (Top 15)")
        self._stat_card(self.left_pane, "Mayor densidad",
                        self.df.loc[self.df["densidad"].idxmax(), "ciudad"], DANGER)
        self._stat_card(self.left_pane, "Promedio global",
                        f"{self.df['densidad'].mean():,.0f} hab/km²", WARNING)

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=BG_PANEL)
        vals = top["densidad"].values
        norm = (vals - vals.min()) / (vals.max() - vals.min())
        colors = plt.cm.YlOrRd(norm)
        bars = ax.bar(range(len(top)), vals, color=colors, edgecolor="none", width=0.7)
        ax.set_xticks(range(len(top)))
        ax.set_xticklabels(top["ciudad"], rotation=45, ha="right", fontsize=8, color=TEXT_SEC)
        ax.set_ylabel("Densidad (hab/km²)", color=TEXT_SEC, fontsize=10)
        ax.set_title("Top 15 Ciudades por Densidad", color=TEXT_PRI, fontsize=13, pad=12)
        ax.tick_params(colors=TEXT_SEC, labelsize=9)
        for spine in ax.spines.values(): spine.set_visible(False)
        ax.yaxis.grid(True, color="#30363D", linewidth=0.6)
        ax.set_axisbelow(True)
        fig.tight_layout()
        self._embed_fig(fig)

    # Q5 — Ciudades costeras vs interior
    def _q5_costeras(self):
        grupo = self.df.groupby("costa").agg(
            Ciudades=("ciudad", "count"),
            Pob_Media=("poblacion", "mean"),
            PIB_Medio=("pib_per_capita", "mean"),
            Turistas_M=("turistas_anuales", "mean")
        ).reset_index()
        grupo["Pob_Media"] = (grupo["Pob_Media"] / 1e6).round(2)
        grupo["PIB_Medio"] = grupo["PIB_Medio"].round(0)
        grupo["Turistas_M"] = (grupo["Turistas_M"] / 1e6).round(2)
        self._make_table(grupo, "Costeras vs Interior — Promedios")

        ctk.CTkLabel(self.left_pane, text="Distribución",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color=TEXT_SEC).pack(padx=16, pady=(8, 2), anchor="w")
        for _, row in grupo.iterrows():
            self._stat_card(self.left_pane, f"{'🌊' if row['costa']=='Sí' else '🏔️'} {row['costa']}",
                            f"{int(row['Ciudades'])} ciudades", ACCENT if row["costa"] == "Sí" else WARNING)

        fig = self._make_fig()
        metrics = ["Pob_Media", "PIB_Medio", "Turistas_M"]
        labels  = ["Pob. Media (M)", "PIB Medio (USD)", "Turistas (M/año)"]
        x = np.arange(len(metrics)); w = 0.35

        ax = fig.add_subplot(111, facecolor=BG_PANEL)
        sí  = grupo[grupo["costa"] == "Sí"][metrics].values.flatten()
        no  = grupo[grupo["costa"] == "No"][metrics].values.flatten()
        ax.bar(x - w/2, sí,  w, label="Costera",  color=ACCENT,   alpha=0.9, edgecolor="none")
        ax.bar(x + w/2, no,  w, label="Interior", color=WARNING, alpha=0.9, edgecolor="none")
        ax.set_xticks(x); ax.set_xticklabels(labels, color=TEXT_SEC, fontsize=9)
        ax.set_title("Ciudades Costeras vs Interior", color=TEXT_PRI, fontsize=13, pad=12)
        ax.tick_params(colors=TEXT_SEC, labelsize=9)
        ax.legend(facecolor=BG_DARK, edgecolor="#30363D", labelcolor=TEXT_PRI, fontsize=9)
        for spine in ax.spines.values(): spine.set_visible(False)
        ax.yaxis.grid(True, color="#30363D", linewidth=0.6); ax.set_axisbelow(True)
        fig.tight_layout()
        self._embed_fig(fig)

    # Q6 — Correlación
    def _q6_correlacion(self):
        num_cols = ["poblacion", "densidad", "temperatura_media", "precipitacion_mm",
                    "pib_per_capita", "esperanza_vida", "altitud_m", "turistas_anuales"]
        corr_df = self.df[num_cols].corr().round(2)
        self._make_table(corr_df.reset_index().rename(columns={"index": ""}),
                         "Matriz de Correlación")

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=BG_PANEL)
        im = ax.imshow(corr_df.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04).ax.yaxis.set_tick_params(color=TEXT_SEC)
        short = ["Pob.", "Dens.", "Temp.", "Prec.", "PIB", "Vida", "Alt.", "Tur."]
        ax.set_xticks(range(len(short))); ax.set_xticklabels(short, color=TEXT_SEC, fontsize=8, rotation=45)
        ax.set_yticks(range(len(short))); ax.set_yticklabels(short, color=TEXT_SEC, fontsize=8)
        for i in range(len(short)):
            for j in range(len(short)):
                ax.text(j, i, f"{corr_df.values[i,j]:.2f}",
                        ha="center", va="center",
                        color="white" if abs(corr_df.values[i,j]) > 0.4 else TEXT_SEC,
                        fontsize=7)
        ax.set_title("Mapa de Correlación entre Variables", color=TEXT_PRI, fontsize=13, pad=12)
        fig.tight_layout()
        self._embed_fig(fig)

    # Q7 — Altitud vs Temperatura
    def _q7_altitud_temp(self):
        df = self.df[["ciudad", "altitud_m", "temperatura_media"]].sort_values("altitud_m", ascending=False)
        self._make_table(df.rename(columns={"altitud_m": "Altitud (m)",
                                            "temperatura_media": "Temp (°C)"}),
                         "Altitud vs Temperatura")
        corr = df["altitud_m"].corr(df["temperatura_media"])
        self._stat_card(self.left_pane, "Correlación altitud-temp.", f"{corr:.3f}", ACCENT)
        self._stat_card(self.left_pane, "Ciudad más alta",
                        self.df.loc[self.df["altitud_m"].idxmax(), "ciudad"], WARNING)

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=BG_PANEL)
        ax.scatter(self.df["altitud_m"], self.df["temperatura_media"],
                   c=self.df["temperatura_media"], cmap="coolwarm",
                   s=80, alpha=0.85, edgecolors="none")
        z = np.polyfit(self.df["altitud_m"], self.df["temperatura_media"], 1)
        p = np.poly1d(z)
        xs = np.linspace(self.df["altitud_m"].min(), self.df["altitud_m"].max(), 100)
        ax.plot(xs, p(xs), "--", color=ACCENT, linewidth=1.5, alpha=0.8, label="Tendencia")
        for _, row in self.df.nlargest(3, "altitud_m").iterrows():
            ax.annotate(row["ciudad"], (row["altitud_m"], row["temperatura_media"]),
                        fontsize=7, color=TEXT_SEC, xytext=(4, 4), textcoords="offset points")
        ax.set_xlabel("Altitud (m)", color=TEXT_SEC, fontsize=10)
        ax.set_ylabel("Temperatura Media (°C)", color=TEXT_SEC, fontsize=10)
        ax.set_title("Altitud vs Temperatura", color=TEXT_PRI, fontsize=13, pad=12)
        ax.tick_params(colors=TEXT_SEC, labelsize=9)
        ax.legend(facecolor=BG_DARK, edgecolor="#30363D", labelcolor=TEXT_PRI, fontsize=9)
        for spine in ax.spines.values(): spine.set_color("#30363D")
        fig.tight_layout()
        self._embed_fig(fig)

    # Q8 — Infraestructura
    def _q8_infraestructura(self):
        df = self.df[["ciudad", "universidades", "hospitales", "parques"]].copy()
        df["índice"] = (df["universidades"]*0.4 + df["hospitales"]*0.35 + df["parques"]*0.25).round(1)
        df = df.sort_values("índice", ascending=False).head(15)
        self._make_table(df, "Índice de Infraestructura Urbana (Top 15)")

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=BG_PANEL)
        x = np.arange(len(df)); w = 0.25
        ax.bar(x - w,   df["universidades"], w, label="Universidades", color="#58A6FF", alpha=0.9)
        ax.bar(x,       df["hospitales"],    w, label="Hospitales",    color="#3FB950", alpha=0.9)
        ax.bar(x + w,   df["parques"],       w, label="Parques",       color="#F78166", alpha=0.9)
        ax.set_xticks(x); ax.set_xticklabels(df["ciudad"], rotation=45, ha="right", fontsize=8, color=TEXT_SEC)
        ax.set_title("Infraestructura Urbana (Top 15)", color=TEXT_PRI, fontsize=13, pad=12)
        ax.tick_params(colors=TEXT_SEC, labelsize=9)
        ax.legend(facecolor=BG_DARK, edgecolor="#30363D", labelcolor=TEXT_PRI, fontsize=9)
        for spine in ax.spines.values(): spine.set_visible(False)
        ax.yaxis.grid(True, color="#30363D", linewidth=0.6); ax.set_axisbelow(True)
        fig.tight_layout()
        self._embed_fig(fig)

    # Q9 — Turismo
    def _q9_turismo(self):
        top = self.df.nlargest(10, "turistas_anuales")[["ciudad", "pais", "turistas_anuales"]].copy()
        top["turistas_M"] = (top["turistas_anuales"] / 1e6).round(1)
        self._make_table(top[["ciudad", "pais", "turistas_M"]].rename(
            columns={"turistas_M": "Turistas (M/año)"}), "Top 10 Destinos Turísticos")
        self._stat_card(self.left_pane, "Destino #1",
                        top.iloc[0]["ciudad"] + f" — {top.iloc[0]['turistas_M']}M", ACCENT)

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=BG_PANEL)
        wedge_props = dict(width=0.55, edgecolor=BG_CARD, linewidth=2)
        colors = plt.cm.Set3(np.linspace(0, 1, len(top)))
        wedges, texts, autotexts = ax.pie(
            top["turistas_M"], labels=top["ciudad"],
            colors=colors, autopct="%1.1f%%",
            pctdistance=0.75, wedgeprops=wedge_props,
            startangle=140, textprops={"color": TEXT_SEC, "fontsize": 8})
        for at in autotexts: at.set_color(TEXT_PRI); at.set_fontsize(7)
        ax.set_title("Distribución de Turistas (Top 10)", color=TEXT_PRI, fontsize=13, pad=12)
        fig.tight_layout()
        self._embed_fig(fig)

    # Q10 — Estadísticas
    def _q10_estadisticas(self):
        num_cols = ["poblacion", "densidad", "temperatura_media", "precipitacion_mm",
                    "pib_per_capita", "esperanza_vida"]
        stats = self.df[num_cols].describe().T[["mean", "std", "min", "max"]].round(1)
        stats.columns = ["Media", "Desv.Std", "Mín.", "Máx."]
        self._make_table(stats.reset_index().rename(columns={"index": "Variable"}),
                         "Estadísticas Descriptivas")
        self._stat_card(self.left_pane, "Total ciudades", str(len(self.df)), ACCENT)
        self._stat_card(self.left_pane, "Países representados",
                        str(self.df["pais"].nunique()), WARNING)

        fig = self._make_fig()
        variables = ["poblacion", "pib_per_capita", "esperanza_vida", "densidad",
                     "temperatura_media", "precipitacion_mm"]
        titles    = ["Población", "PIB/cáp.", "Esp. Vida", "Densidad", "Temp.", "Precip."]
        axes_list = fig.subplots(2, 3)
        for ax, col, title in zip(axes_list.flat, variables, titles):
            ax.set_facecolor(BG_PANEL)
            ax.hist(self.df[col], bins=10, color=ACCENT, alpha=0.8, edgecolor="none")
            ax.set_title(title, color=TEXT_PRI, fontsize=9)
            ax.tick_params(colors=TEXT_SEC, labelsize=7)
            for spine in ax.spines.values(): spine.set_visible(False)
        fig.suptitle("Distribuciones de Variables", color=TEXT_PRI, fontsize=13, y=1.01)
        fig.tight_layout()
        self._embed_fig(fig)

    # Q11 — Por país
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
        self._make_table(grupo, "Comparativa por País")

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=BG_PANEL)
        colors = plt.cm.tab20(np.linspace(0, 1, len(grupo)))
        ax.barh(grupo["pais"], grupo["Pob_Total"], color=colors, edgecolor="none")
        ax.set_xlabel("Población Total (millones)", color=TEXT_SEC, fontsize=10)
        ax.set_title("Población Total por País", color=TEXT_PRI, fontsize=13, pad=12)
        ax.tick_params(colors=TEXT_SEC, labelsize=9)
        for spine in ax.spines.values(): spine.set_visible(False)
        ax.xaxis.grid(True, color="#30363D", linewidth=0.6); ax.set_axisbelow(True)
        fig.tight_layout()
        self._embed_fig(fig)

    # Q12 — Heatmap
    def _q12_heatmap(self):
        num_cols = ["poblacion", "densidad", "temperatura_media", "precipitacion_mm",
                    "pib_per_capita", "esperanza_vida", "altitud_m", "turistas_anuales",
                    "universidades", "hospitales"]
        df_norm = self.df[num_cols].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
        self._make_table(
            self.df[["ciudad", "pais"]].join(df_norm[["pib_per_capita", "esperanza_vida", "turistas_anuales"]].round(2)),
            "Variables Normalizadas (muestra)")

        fig = self._make_fig()
        ax = fig.add_subplot(111, facecolor=BG_PANEL)
        im = ax.imshow(df_norm.values.T, cmap="inferno", aspect="auto")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        short_cols = ["Pob.", "Dens.", "Temp.", "Prec.", "PIB", "Vida", "Alt.", "Tur.", "Univ.", "Hosp."]
        ax.set_yticks(range(len(short_cols))); ax.set_yticklabels(short_cols, color=TEXT_SEC, fontsize=8)
        ax.set_xticks(range(0, len(self.df), max(1, len(self.df)//10)))
        ax.set_xticklabels(self.df["ciudad"].iloc[::max(1, len(self.df)//10)],
                           rotation=45, ha="right", color=TEXT_SEC, fontsize=7)
        ax.set_title("Heatmap — Variables Normalizadas por Ciudad", color=TEXT_PRI, fontsize=13, pad=12)
        fig.tight_layout()
        self._embed_fig(fig)

    def _logout(self):
        if messagebox.askyesno("Cerrar sesión", "¿Deseas cerrar sesión?"):
            self.destroy()
            login = LoginWindow()
            login.mainloop()


if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()