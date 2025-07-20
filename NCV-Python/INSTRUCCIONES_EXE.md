# 🚀 Cómo convertir NetworkConnVerifier a .exe

## 📋 Requisitos Previos

1. **Python 3.7+** instalado en tu sistema
2. **Conexión a internet** para descargar dependencias
3. **Permisos de administrador** (recomendado)

## 🔧 Pasos para crear el ejecutable

### Opción 1: Usando el script automático (Recomendado)

1. **Abre PowerShell como Administrador**
   - Presiona `Win + X`
   - Selecciona "Windows PowerShell (Administrador)"

2. **Navega al directorio del proyecto**
   ```powershell
   cd "C:\Users\andre\Desktop\NetworkConnVerifier\NCV-Python"
   ```

3. **Ejecuta el script de construcción con icono**
   ```powershell
   python build_with_icon.py
   ```

4. **¡Listo!** El ejecutable se creará en la carpeta `dist/`

### Opción 2: Manual paso a paso

1. **Instalar PyInstaller**
   ```powershell
   pip install pyinstaller
   ```

2. **Instalar dependencias del proyecto**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Crear el ejecutable**
   ```powershell
   pyinstaller --onefile --windowed --name=NetworkConnVerifier NetConnVerGUI.py
   ```

## 📁 Resultado

Después de la construcción, encontrarás:
- `dist/NetworkConnVerifier.exe` - Tu ejecutable final
- `build/` - Archivos temporales de construcción
- `NetworkConnVerifier.spec` - Archivo de configuración

## 🎯 Características del ejecutable

✅ **Completamente independiente** - No requiere Python instalado  
✅ **Sin ventana de consola** - Interfaz gráfica limpia  
✅ **Archivo único** - Fácil de distribuir  
✅ **Compatible con Windows 10/11**  

## 🚀 Distribución

1. **Copia** `NetworkConnVerifier.exe` a cualquier carpeta
2. **Ejecuta** haciendo doble clic
3. **¡Funciona!** Sin instalación adicional

## 🔧 Solución de problemas

### Error: "No se puede ejecutar el script"
- **Solución**: Ejecuta PowerShell como administrador

### Error: "PyInstaller no se reconoce"
- **Solución**: Reinstala PyInstaller: `pip install --upgrade pyinstaller`

### Error: "Falta matplotlib"
- **Solución**: Instala manualmente: `pip install matplotlib ping3`

### El antivirus bloquea la construcción
- **Solución**: Agrega temporalmente la carpeta del proyecto a las exclusiones del antivirus

### El ejecutable no funciona en otra PC
- **Solución**: Asegúrate de usar `--onefile --windowed` en el comando

## 📊 Tamaño del ejecutable

- **Tamaño esperado**: ~50-80 MB
- **Tiempo de construcción**: 2-5 minutos
- **Tiempo de inicio**: 3-5 segundos

## 🎨 Personalización (Opcional)

### Agregar un icono
1. Coloca tu archivo `.ico` en la carpeta `img/`
2. Ejecuta el script con icono:
   ```powershell
   python build_with_icon.py
   ```

### Cambiar el nombre del ejecutable
```powershell
pyinstaller --onefile --windowed --name=MiMonitorDeRed NetConnVerGUI.py
```

## 📞 Soporte

Si encuentras problemas:
1. Verifica que Python esté en el PATH
2. Ejecuta como administrador
3. Desactiva temporalmente el antivirus
4. Asegúrate de tener suficiente espacio en disco (al menos 500MB)

---

**¡Tu NetworkConnVerifier está listo para distribuir! 🎉** 