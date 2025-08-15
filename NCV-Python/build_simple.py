#!/usr/bin/env python3
"""
Script simple para construir el ejecutable con icono personalizado
Sin limpiar carpetas anteriores para evitar errores de permisos
"""

import os
import sys
import subprocess

def main():
    """Construye el ejecutable con el icono personalizado"""
    print("=== Constructor Simple de Ejecutable con Icono ===\n")
    
    # Verificar que existe el icono
    icon_path = "img/NCV-Icon.ico"
    if not os.path.exists(icon_path):
        print(f"❌ Error: No se encuentra el icono en {icon_path}")
        print("💡 Asegúrate de que el archivo NCV-Icon.ico esté en la carpeta img/")
        return 1
    
    print(f"✓ Icono encontrado: {icon_path}")
    
    # Comando de construcción con icono (sin limpiar carpetas anteriores)
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Un solo archivo ejecutable
        "--windowed",  # Sin ventana de consola
        "--name=NetworkConnVerifier",
        f"--icon={icon_path}",  # Tu icono personalizado
        "--noconfirm",  # No preguntar antes de sobrescribir
        "NetConnVerGUI.py"
    ]
    
    print("🔨 Construyendo ejecutable con icono personalizado...")
    print("⏳ Esto puede tomar 2-5 minutos...")
    
    try:
        subprocess.check_call(cmd)
        print("\n🎉 ¡Ejecutable creado exitosamente con tu icono!")
        print("📁 Ubicación: dist/NetworkConnVerifier.exe")
        print("🎨 El ejecutable tendrá tu icono personalizado")
        
        # Verificar que se creó
        exe_path = "dist/NetworkConnVerifier.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📊 Tamaño del ejecutable: {size_mb:.1f} MB")
            print("\n✅ ¡Listo! Puedes usar el ejecutable en cualquier PC")
        else:
            print("⚠️  El ejecutable no se encontró en dist/")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error durante la construcción: {e}")
        print("💡 Asegúrate de que PyInstaller esté instalado:")
        print("   pip install pyinstaller")
        return 1
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 