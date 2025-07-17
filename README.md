# NetworkConnVerifier

Monitoriza tu conexión a internet en tiempo real con una interfaz moderna y dos modos de visualización:

- **Terminal:** Verifica el estado de tu conexión, ping y estabilidad en tiempo real.
- **Interfaz gráfica (GUI):** Visualiza el ping en tiempo real con dos modos de gráfica:
  - **Clásico:** Línea multicolor y área bajo la curva, con detección de picos de lag.
  - **Minecraft:** Barras verticales tipo debug de Minecraft, con gradiente de colores según el ping.

## Características
- Detección de conexión, desconexión y latencia alta.
- Visualización clara y moderna, modo oscuro.
- Leyenda de colores y emojis para fácil interpretación.
- Ultra fluido: refresco cada 0.01s.
- Optimizado para bajo consumo de CPU.
- Botón para alternar entre modos de gráfica.

## Requisitos
- Python 3.8+
- Windows, Linux o MacOS

## Instalación
1. Clona o descarga este repositorio.
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso
### Terminal
```bash
python NetConnVer.py
```

### Interfaz gráfica
```bash
python NetConnVerGUI.py
```

## Dependencias
- ping3
- matplotlib
- tkinter (incluido en la mayoría de instalaciones de Python)

## Captura de pantalla
![screenshot](screenshot.png)

---

**Hecho con ❤️ para monitorear tu red como un pro.** 