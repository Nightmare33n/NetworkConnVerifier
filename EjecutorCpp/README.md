# 🚀 Ejecutor C++ para MSYS2

Este ejecutor te permite compilar y ejecutar archivos C++ fácilmente usando MSYS2 en Windows.

## 📋 Requisitos

- **MSYS2** instalado en `C:\msys64\`
- **Python 3.6+** (para el script Python)
- **Archivos .cpp** para compilar

## 🛠️ Instalación

1. Asegúrate de tener MSYS2 instalado en `C:\msys64\`
2. Verifica que el compilador g++ esté disponible en `C:\msys64\mingw64\bin\g++.exe`
3. Si no tienes g++, instálalo desde MSYS2:
   ```bash
   pacman -S mingw-w64-x86_64-gcc
   ```

## 📁 Estructura

```
EjecutorCpp/
├── run.py          # Ejecutor en Python
├── run.bat         # Ejecutor en Batch (Windows)
└── README.md       # Este archivo
```

## 🎯 Uso

### Opción 1: Usando el archivo Batch (Recomendado)

```bash
# Compilar y ejecutar automáticamente (si hay un solo archivo .cpp)
run.bat

# Compilar y ejecutar un archivo específico
run.bat mi_archivo.cpp

# Solo compilar, no ejecutar
run.bat mi_archivo.cpp -c

# Especificar nombre de salida
run.bat mi_archivo.cpp -o mi_programa

# Listar archivos .cpp disponibles
run.bat -l
```

### Opción 2: Usando el script Python

```bash
# Compilar y ejecutar automáticamente
python run.py

# Compilar y ejecutar un archivo específico
python run.py mi_archivo.cpp

# Solo compilar, no ejecutar
python run.py mi_archivo.cpp --compile-only

# Especificar nombre de salida
python run.py mi_archivo.cpp -o mi_programa

# Listar archivos .cpp disponibles
python run.py -l
```

## 🔧 Características

- ✅ **Detección automática** de archivos .cpp
- ✅ **Compilación con warnings** habilitados
- ✅ **Salida organizada** en carpeta `output/`
- ✅ **Mensajes coloridos** para mejor experiencia
- ✅ **Manejo de errores** detallado
- ✅ **Soporte para C++17**

## 📝 Ejemplo de uso

1. **Crea un archivo de prueba:**
   ```cpp
   // test.cpp
   #include <iostream>
   
   int main() {
       std::cout << "¡Hola desde C++!" << std::endl;
       return 0;
   }
   ```

2. **Ejecuta el compilador:**
   ```bash
   run.bat test.cpp
   ```

3. **Resultado esperado:**
   ```
   🔨 Compilando: test.cpp
   📁 Salida: output/test.exe
   ✅ Compilación exitosa!
   
   🚀 Ejecutando: output/test.exe
   ════════════════════════════════════════════════════════════
   ¡Hola desde C++!
   ════════════════════════════════════════════════════════════
   ✅ Programa terminado
   ```

## ⚙️ Configuración

### Cambiar la ruta de MSYS2

Si tu MSYS2 está instalado en otra ubicación, edita los archivos:

**En `run.py`:**
```python
self.msys2_path = r"C:\tu\ruta\a\msys64\mingw64.exe"
self.gcc_path = r"C:\tu\ruta\a\msys64\mingw64\bin\g++.exe"
```

**En `run.bat`:**
```batch
set MSYS2_PATH=C:\tu\ruta\a\msys64
set GCC_PATH=%MSYS2_PATH%\mingw64\bin\g++.exe
```

### Opciones de compilación

Los archivos usan estas opciones por defecto:
- `-Wall`: Mostrar todas las advertencias
- `-Wextra`: Advertencias extra
- `-g3`: Información de debug completa
- `-std=c++17`: Estándar C++17

## 🐛 Solución de problemas

### Error: "No se encontró MSYS2"
- Verifica que MSYS2 esté instalado en `C:\msys64\`
- Si está en otra ubicación, actualiza las rutas en los archivos

### Error: "No se encontró g++"
- Abre MSYS2 y ejecuta: `pacman -S mingw-w64-x86_64-gcc`
- Verifica que el PATH incluya `C:\msys64\mingw64\bin\`

### Error de compilación
- Revisa los errores mostrados en la salida
- Asegúrate de que el código C++ sea válido
- Verifica que todas las librerías necesarias estén instaladas

## 📚 Comandos útiles de MSYS2

```bash
# Actualizar MSYS2
pacman -Syu

# Instalar compilador C++
pacman -S mingw-w64-x86_64-gcc

# Instalar herramientas de desarrollo
pacman -S mingw-w64-x86_64-make
pacman -S mingw-w64-x86_64-cmake

# Verificar instalación
g++ --version
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras un bug o tienes una mejora, no dudes en reportarlo.

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT. 