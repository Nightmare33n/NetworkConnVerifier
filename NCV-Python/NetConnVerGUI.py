# This one
import threading
import time
from collections import deque
import math
try:
    from ping3 import ping
except ImportError:
    import os
    import sys
    os.system(f"{sys.executable} -m pip install ping3")
    from ping3 import ping
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import os
    import sys
    os.system(f"{sys.executable} -m pip install tk")
    import tkinter as tk
    from tkinter import ttk
try:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    import os
    import sys
    os.system(f"{sys.executable} -m pip install matplotlib")
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
try:
    import numpy as np
    from scipy.interpolate import make_interp_spline
except ImportError:
    import os
    import sys
    print("Instalando scipy y numpy...")
    os.system(f"{sys.executable} -m pip install scipy numpy")
    import numpy as np
    from scipy.interpolate import make_interp_spline


PING_TARGET = "google.com"
PING_TIMEOUT = 1  # segundos
HISTORIAL_SIZE = 400  # Un poco más largo para barras
FALLOS_PARA_DESCONECTADO = 5
VISIBLE_BARS = 200  # Solo muestra los últimos 200

# Paleta inspirada en el Administrador de tareas de Windows
BG_DARK = "#181a1b"
FG_LIGHT = "#e0e0e0"
GRID_COLOR = "#444"
GREEN = "#39ff14"
YELLOW = "#ffe347"
RED = "#ff3576"
GRAY = "#44475a"
FILL_ALPHA = 0.18

# Gama de colores para barras (de verde a rojo y gris)
COLOR_GRADIENT = [
    (0,   '#39ff14'),   # Verde claro
    (40,  '#00e676'),  # Verde
    (70,  '#ffe347'),  # Amarillo
    (120, '#ffb347'),  # Naranja
    (200, '#ff3576'),  # Rojo
    (9999, '#44475a')  # Gris (desconectado o muy alto)
]

ESTADOS = {
    'Connected': {'color': '#39ff14', 'desc': 'Conexión estable', 'emoji': '🟢'},
    'Slow Connection': {'color': '#ffe347', 'desc': 'Conexión lenta', 'emoji': '🟡'},
    'Disconnected': {'color': '#44475a', 'desc': 'Sin conexión', 'emoji': '⚫'},
    'Very Slow': {'color': '#ff3576', 'desc': 'Muy lenta', 'emoji': '🔴'}
}

class NetConnVerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Verificador de Conexión de Red - Monitor en Vivo")
        self.root.geometry("900x600")
        self.root.configure(bg=BG_DARK)
        self.historial = deque(maxlen=HISTORIAL_SIZE)
        self.time_hist = deque(maxlen=HISTORIAL_SIZE)
        self.estado_actual = 'Disconnected'
        self.color_actual = ESTADOS['Disconnected']['color']
        self.status = tk.StringVar()
        self.status.set("Iniciando...")
        self.ping_label = tk.StringVar()
        self.ping_label.set("-")
        self.prom_label = tk.StringVar()
        self.prom_label.set("-")
        self.grafica_modo = tk.StringVar(value="clasic")
        self._setup_ui()
        self._start_ping_thread()

    def _setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=BG_DARK)
        style.configure('TLabel', background=BG_DARK, foreground=FG_LIGHT, font=("Segoe UI", 13))
        style.configure('Status.TLabel', font=("Segoe UI", 22, "bold"), background=BG_DARK, foreground=FG_LIGHT)
        style.configure('Ping.TLabel', font=("Segoe UI", 16, "bold"), background=BG_DARK, foreground=FG_LIGHT)
        style.configure('Prom.TLabel', font=("Segoe UI", 13), background=BG_DARK, foreground=FG_LIGHT)

        frame = ttk.Frame(self.root, style='TFrame')
        frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Panel superior oscuro
        self.panel_superior = tk.Frame(frame, bg=BG_DARK)
        self.panel_superior.pack(fill=tk.X, padx=0, pady=0)

        # Círculo de estado
        self.canvas_estado = tk.Canvas(self.panel_superior, width=36, height=36, bg=BG_DARK, highlightthickness=0, bd=0)
        self.circulo = self.canvas_estado.create_oval(6, 6, 30, 30, fill=ESTADOS['Disconnected']['color'], outline="")
        self.canvas_estado.pack(pady=(10, 2))

        # Estado
        self.status_lbl = tk.Label(self.panel_superior, textvariable=self.status, font=("Segoe UI", 22, "bold"), bg=BG_DARK, fg=FG_LIGHT)
        self.status_lbl.pack(pady=(0, 2))

        # Ping actual
        self.ping_lbl = tk.Label(self.panel_superior, textvariable=self.ping_label, font=("Segoe UI", 16, "bold"), bg=BG_DARK, fg=FG_LIGHT)
        self.ping_lbl.pack(pady=(0, 0))

        # Promedio
        self.prom_lbl = tk.Label(self.panel_superior, textvariable=self.prom_label, font=("Segoe UI", 13), bg=BG_DARK, fg=FG_LIGHT)
        self.prom_lbl.pack(pady=(0, 4))

        # Leyenda con emojis
        leyenda = tk.Label(
            self.panel_superior,
            text=f"{ESTADOS['Connected']['emoji']} <50ms: Estable   {ESTADOS['Slow Connection']['emoji']} <200ms: Lenta   {ESTADOS['Very Slow']['emoji']} >200ms: Muy lenta   {ESTADOS['Disconnected']['emoji']} Sin respuesta",
            font=("Segoe UI", 11), bg=BG_DARK, fg="#888888")
        leyenda.pack(pady=(0, 8))

        # Botón para cambiar modo de gráfica
        self.boton_modo = tk.Button(self.panel_superior, text="Cambiar modo de gráfica", command=self.toggle_grafica_modo, bg=BG_DARK, fg=FG_LIGHT, activebackground="#222", activeforeground=FG_LIGHT, relief=tk.FLAT, font=("Segoe UI", 11, "bold"))
        self.boton_modo.pack(pady=(0, 8))

        # Gráfica matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 3), facecolor=BG_DARK)
        self.fig.subplots_adjust(left=0.06, right=0.98, top=0.95, bottom=0.15)
        self.ax.set_facecolor(BG_DARK)
        self.ax.tick_params(colors=FG_LIGHT, labelsize=11)
        self.ax.spines['bottom'].set_color(GRID_COLOR)
        self.ax.spines['top'].set_color(GRID_COLOR)
        self.ax.spines['right'].set_color(GRID_COLOR)
        self.ax.spines['left'].set_color(GRID_COLOR)
        
        self.line_collection = LineCollection([], linewidths=2)
        self.ax.add_collection(self.line_collection)
        
        self.barras_collection = LineCollection([], linewidths=1)
        self.ax.add_collection(self.barras_collection)

        self.line_smooth, = self.ax.plot([], [], color=GREEN, linewidth=2, alpha=0.95)

        self.fill = None
        
        self.ax.set_ylabel("Ping (ms)", color=FG_LIGHT, fontsize=13)
        self.ax.set_xlabel("Tiempo", color=FG_LIGHT, fontsize=13)
        self.ax.grid(True, color=GRID_COLOR, linestyle='-', alpha=0.5)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def toggle_grafica_modo(self):
        if self.grafica_modo.get() == "clasic":
            self.grafica_modo.set("minecraft")
        else:
            self.grafica_modo.set("clasic")

    def _start_ping_thread(self):
        thread = threading.Thread(target=self._ping_loop, daemon=True)
        thread.start()
        self._update_all()
        self._animar_estado()

    def _ping_loop(self):
        while True:
            t = time.time()
            ping_time = ping(PING_TARGET, timeout=PING_TIMEOUT, unit="ms")
            if ping_time is not None:
                ping_time = round(ping_time, 1)
            self.historial.append(ping_time)
            self.time_hist.append(t)
            self._update_status()
            time.sleep(0.1)

    def _update_status(self):
        # Determinar estado
        fallos = sum(1 for x in self.historial if x is None)
        pings_ok = [x for x in self.historial if x is not None]
        if fallos >= FALLOS_PARA_DESCONECTADO or not pings_ok:
            estado = 'Disconnected'
        else:
            promedio = sum(pings_ok) / len(pings_ok)
            if promedio < 50:
                estado = 'Connected'
            elif promedio < 200:
                estado = 'Slow Connection'
            else:
                estado = 'Very Slow'
        self.estado_actual = estado
        color = ESTADOS[estado]['color']
        desc = ESTADOS[estado]['desc']
        self.status.set(f"{desc}")
        self.status_lbl.configure(fg=color)
        self.ping_lbl.configure(fg=color)
        self.prom_lbl.configure(fg=color)
        if pings_ok:
            self.ping_label.set(f"Ping actual: {pings_ok[-1]} ms")
            self.prom_label.set(f"Promedio: {round(sum(pings_ok)/len(pings_ok),1)} ms")
        else:
            self.ping_label.set("Ping actual: N/A")
            self.prom_label.set("Promedio: N/A")

    def _update_all(self):
        self._update_plot()
        self.root.after(100, self._update_all)  # Refresco cada 0.1s

    def _color_for_ping(self, ping):
        if ping is None or math.isnan(ping):
            return COLOR_GRADIENT[-1][1]
        for i in range(len(COLOR_GRADIENT)-1):
            v1, c1 = COLOR_GRADIENT[i]
            v2, c2 = COLOR_GRADIENT[i+1]
            if v1 <= ping < v2:
                # Interpolación lineal de color
                f = (ping-v1)/(v2-v1)
                r1,g1,b1 = self._hex_to_rgb(c1)
                r2,g2,b2 = self._hex_to_rgb(c2)
                r = int(r1 + (r2-r1)*f)
                g = int(g1 + (g2-g1)*f)
                b = int(b1 + (b2-b1)*f)
                return f'#{r:02x}{g:02x}{b:02x}'
        return COLOR_GRADIENT[-1][1]

    def _update_plot(self):
        y = [x if x is not None else float('nan') for x in self.historial]
        if not y:
            return
        x = list(range(-len(y)+1, 1))

        if self.grafica_modo.get() == "clasic":
            self.barras_collection.set_visible(False)
            self.line_collection.set_visible(False)
            self.line_smooth.set_visible(True)
            if self.fill:
                self.fill.set_visible(True)

            y_numeric = [v for v in y if not math.isnan(v)]
            x_numeric = [x[i] for i, v in enumerate(y) if not math.isnan(v)]

            if len(x_numeric) > 3:
                x_smooth = np.linspace(min(x_numeric), max(x_numeric), 300)
                spl = make_interp_spline(x_numeric, y_numeric, k=3)
                y_smooth = spl(x_smooth)
                self.line_smooth.set_data(x_smooth, y_smooth)
            else:
                self.line_smooth.set_data(x_numeric, y_numeric)


            if self.fill:
                self.fill.remove()
            
            ultimo_color = self._color_for_ping(y[-1])
            self.fill = self.ax.fill_between(x, y, [0]*len(y), color=ultimo_color, alpha=FILL_ALPHA, interpolate=True)

        else: # minecraft mode
            self.line_collection.set_visible(False)
            self.line_smooth.set_visible(False)
            if self.fill:
                self.fill.set_visible(False)
            self.barras_collection.set_visible(True)

            x_bars = x[-VISIBLE_BARS:]
            y_bars = y[-VISIBLE_BARS:]
            segments = []
            colors = []
            for i, (xpos, val) in enumerate(zip(x_bars, y_bars)):
                if math.isnan(val):
                    color = self._color_for_ping(None)
                    height = 0
                else:
                    color = self._color_for_ping(val)
                    height = val
                segments.append([(xpos, 0), (xpos, height)])
                colors.append(color)
            
            self.barras_collection.set_segments(segments)
            self.barras_collection.set_color(colors)

        self.ax.set_xlim(-VISIBLE_BARS+1, 0)
        if y and not all(math.isnan(v) for v in y):
            self.ax.set_ylim(0, max([v for v in y if not math.isnan(v)]+[100])+20)
        else:
            self.ax.set_ylim(0, 100)
        self.canvas.draw()

    def _animar_estado(self):
        color_destino = ESTADOS[self.estado_actual]['color']
        r1, g1, b1 = self._hex_to_rgb(self.color_actual)
        r2, g2, b2 = self._hex_to_rgb(color_destino)
        r = int(r1 + (r2 - r1) * 0.2)
        g = int(g1 + (g2 - g1) * 0.2)
        b = int(b1 + (b2 - b1) * 0.2)
        color_suave = f'#{r:02x}{g:02x}{b:02x}'
        self.canvas_estado.itemconfig(self.circulo, fill=color_suave)
        self.color_actual = color_suave
        self.root.after(20, self._animar_estado)

    def _hex_to_rgb(self, hexcolor):
        hexcolor = (hexcolor or '#444').lstrip('#')
        if len(hexcolor) != 6:
            hexcolor = '444444'
        return tuple(int(hexcolor[i:i+2], 16) for i in (0, 2, 4))

if __name__ == "__main__":
    root = tk.Tk()
    app = NetConnVerGUI(root)
    root.mainloop()