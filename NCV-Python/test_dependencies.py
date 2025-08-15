#!/usr/bin/env python3
"""
Script para verificar que todas las dependencias estén instaladas
antes de crear el ejecutable
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Prueba si un módulo se puede importar"""
    try:
        if package_name:
            importlib.import_module(package_name)
        else:
            importlib.import_module(module_name)
        print(f"✓ {module_name}")
        return True
    except ImportError as e:
        print(f"✗ {module_name} - Error: {e}")
        return False

def main():
    """Prueba todas las dependencias necesarias"""
    print("=== Verificación de Dependencias ===\n")
    
    required_modules = [
        ("threading", None),
        ("time", None),
        ("collections", None),
        ("math", None),
        ("tkinter", None),
        ("tkinter.ttk", "tkinter"),
        ("ping3", None),
        ("matplotlib", None),
        ("matplotlib.pyplot", "matplotlib"),
        ("matplotlib.backends.backend_tkagg", "matplotlib"),
        ("matplotlib.collections", "matplotlib"),
    ]
    
    all_good = True
    for module_name, package_name in required_modules:
        if not test_import(module_name, package_name):
            all_good = False
    
    print("\n" + "="*40)
    
    if all_good:
        print("🎉 ¡Todas las dependencias están instaladas correctamente!")
        print("✅ Puedes proceder a crear el ejecutable")
        return 0
    else:
        print("❌ Faltan algunas dependencias")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 