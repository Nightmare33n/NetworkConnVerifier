#!/usr/bin/env python3
"""
Script para construir el ejecutable con icono personalizado
"""

import os
import sys
import subprocess
import shutil
import time

def safe_remove_dir(dir_path):
    """Elimina un directorio de forma segura, manejando errores de permisos"""
    if not os.path.exists(dir_path):
        return True
    
    try:
        shutil.rmtree(dir_path)
        print(f"✓ {dir_path} limpiado")
        return True
    except PermissionError as e:
        print(f"⚠️  No se pudo eliminar {dir_path}: {e}")
        print("💡 Cierra cualquier programa que esté usando archivos en esa carpeta")
        print("💡 O elimina manualmente la carpeta y vuelve a intentar")
        return False
    except Exception as e:
        print(f"⚠️  Error al limpiar {dir_path}: {e}")
        return False

def main():
    """Construye el ejecutable con el icono personalizado"""
    print("=== Constructor de Ejecutable con Icono Personalizado ===\n")
    
    # Verificar que existe el icono
    icon_path = "img/NCV-Icon.ico"
    if not os.path.exists(icon_path):
        print(f"❌ Error: No se encuentra el icono en {icon_path}")
        print("💡 Asegúrate de que el archivo NCV-Icon.ico esté en la carpeta img/")
        return 1
    
    print(f"✓ Icono encontrado: {icon_path}")
    
    # Limpiar builds anteriores de forma segura
    print("🧹 Limpiando builds anteriores...")
    build_ok = safe_remove_dir("build")
    dist_ok = safe_remove_dir("dist")
    
    if not build_ok or not dist_ok:
        print("\n❌ No se pudieron limpiar las carpetas anteriores")
        print("💡 Soluciones:")
        print("   1. Cierra el ejecutable si lo tienes abierto")
        print("   2. Cierra el Explorador de Windows en esa carpeta")
        print("   3. Elimina manualmente las carpetas build/ y dist/")
        print("   4. Vuelve a ejecutar este script")
        return 1
    
    # Comando de construcción con icono
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Un solo archivo ejecutable
        "--windowed",  # Sin ventana de consola
        "--name=NetworkConnVerifier",
        f"--icon={icon_path}",  # Tu icono personalizado
        "--clean",
        "NetConnVerGUI.py"
    ]
    
    print("🔨 Construyendo ejecutable con icono personalizado...")
    print(f"Comando: {' '.join(cmd)}")
    
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
        else:
            print("⚠️  El ejecutable no se encontró en dist/")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error durante la construcción: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 