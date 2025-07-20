#!/usr/bin/env python3
"""
Script para construir el ejecutable de Network Connection Verifier
Usa PyInstaller para crear un .exe funcional
"""

import os
import sys
import subprocess
import shutil

def install_pyinstaller():
    """Instala PyInstaller si no está disponible"""
    try:
        import PyInstaller
        print("✓ PyInstaller ya está instalado")
    except ImportError:
        print("Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller instalado correctamente")

def install_requirements():
    """Instala las dependencias del proyecto"""
    if os.path.exists("requirements.txt"):
        print("Instalando dependencias...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencias instaladas")

def create_spec_file():
    """Crea el archivo de especificaciones para PyInstaller"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['NetConnVerGUI.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'matplotlib.backends.backend_tkagg',
        'matplotlib.figure',
        'matplotlib.collections',
        'ping3',
        'tkinter',
        'tkinter.ttk',
        'collections',
        'threading',
        'time',
        'math'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NetworkConnVerifier',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin ventana de consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='img/NCV-Icon.ico',  # Tu icono personalizado
)
'''
    
    with open("NetConnVerGUI.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    print("✓ Archivo de especificaciones creado")

def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    print("Construyendo ejecutable...")
    
    # Limpiar builds anteriores
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Construir con PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Un solo archivo ejecutable
        "--windowed",  # Sin ventana de consola
        "--name=NetworkConnVerifier",
        "--icon=img/NCV-Icon.ico",  # Tu icono personalizado
        "--clean",
        "NetConnVerGUI.py"
    ]
    
    subprocess.check_call(cmd)
    print("✓ Ejecutable construido correctamente")

def main():
    """Función principal"""
    print("=== Constructor de Ejecutable NetworkConnVerifier ===\n")
    
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    try:
        # Paso 1: Instalar PyInstaller
        install_pyinstaller()
        
        # Paso 2: Instalar dependencias
        install_requirements()
        
        # Paso 3: Construir ejecutable
        build_executable()
        
        print("\n🎉 ¡Ejecutable creado exitosamente!")
        print("📁 El archivo se encuentra en: dist/NetworkConnVerifier.exe")
        print("\n💡 Para distribuir el programa:")
        print("   - Copia el archivo NetworkConnVerifier.exe a cualquier carpeta")
        print("   - El ejecutable es completamente independiente")
        print("   - No requiere Python instalado en la máquina destino")
        
    except Exception as e:
        print(f"\n❌ Error durante la construcción: {e}")
        print("💡 Asegúrate de que:")
        print("   - Tienes permisos de administrador")
        print("   - Tu antivirus no está bloqueando la construcción")
        print("   - Tienes suficiente espacio en disco")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 