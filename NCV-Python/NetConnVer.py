import os
import time
from collections import deque
try:
    from ping3 import ping
except ImportError:
    print("Instalando ping3...")
    os.system("pip install ping3")
    from ping3 import ping

PING_TARGET = "google.com"
PING_TIMEOUT = 0.2  # segundos
HISTORIAL_SIZE = 10
FALLOS_PARA_DESCONECTADO = 3

# Colores para terminal (opcional, si tu terminal los soporta)
VERDE = '\033[92m'
AMARILLO = '\033[93m'
ROJO = '\033[91m'
RESET = '\033[0m'


def determinar_estado(historial):
    fallos = sum(1 for x in historial if x is None)
    if fallos >= FALLOS_PARA_DESCONECTADO:
        return 'Disconnected', '❌', ROJO
    pings_ok = [x for x in historial if x is not None]
    if not pings_ok:
        return 'Disconnected', '❌', ROJO
    promedio = sum(pings_ok) / len(pings_ok)
    if promedio < 50:
        return 'Connected', '✅', VERDE
    elif promedio < 200:
        return 'Slow Connection', '🐌', AMARILLO
    else:
        return 'Connected', '✅', VERDE

def mostrar_historial(historial):
    out = ''
    for x in historial:
        if x is None:
            out += '❌ '
        elif x < 50:
            out += '🟢 '
        elif x < 200:
            out += '🟡 '
        else:
            out += '🔴 '
    return out.strip()

def log_live():
    historial = deque(maxlen=HISTORIAL_SIZE)
    while True:
        start = time.time()
        ping_time = ping(PING_TARGET, timeout=PING_TIMEOUT, unit="ms")
        if ping_time is not None:
            ping_time = round(ping_time, 1)
        historial.append(ping_time)
        estado, emoji, color = determinar_estado(historial)
        pings_ok = [x for x in historial if x is not None]
        promedio = round(sum(pings_ok) / len(pings_ok), 1) if pings_ok else None
        ultimo = f"{pings_ok[-1]} ms" if pings_ok else "N/A"
        historial_str = mostrar_historial(historial)
        status_line = f"{color}{emoji} {estado} | Último: {ultimo} | Promedio: {promedio if promedio is not None else 'N/A'} ms | [{historial_str}]{RESET}"
        # Limpiar la línea antes de imprimir (ANSI: \033[2K borra toda la línea, \r regresa al inicio)
        print(f"\033[2K\r{status_line}", end='', flush=True)
        # Espera lo mínimo posible, pero deja respirar a la CPU
        elapsed = time.time() - start
        wait = max(0, 0.001 - elapsed)  # intenta actualizar cada milisegundo
        time.sleep(wait)

if __name__ == "__main__":
    print("Monitoreando conexión a internet en tiempo real...")
    print("Presiona Ctrl+C para salir.")
    log_live() 