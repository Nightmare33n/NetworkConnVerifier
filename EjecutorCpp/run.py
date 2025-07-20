#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejecutor C++ para MSYS2
Autor: Asistente
Descripción: Compila y ejecuta archivos C++ usando MSYS2
"""

import os
import sys
import subprocess
import argparse
import glob
from pathlib import Path

class CppExecutor:
    def __init__(self):
        self.msys2_path = r"C:\msys64\mingw64.exe"
        self.gcc_path = r"C:\msys64\mingw64\bin\g++.exe"
        self.output_dir = "output"
        
    def check_msys2_installation(self):
        """Verifica que MSYS2 esté instalado correctamente"""
        if not os.path.exists(self.msys2_path):
            print("❌ Error: No se encontró MSYS2 en la ruta especificada")
            print(f"Ruta esperada: {self.msys2_path}")
            return False
        return True
    
    def find_cpp_files(self, directory="."):
        """Encuentra todos los archivos .cpp en el directorio"""
        cpp_files = []
        for ext in ['*.cpp', '*.cxx', '*.cc']:
            cpp_files.extend(glob.glob(os.path.join(directory, ext)))
        return cpp_files
    
    def compile_file(self, source_file, output_name=None):
        """Compila un archivo C++ usando MSYS2"""
        if not output_name:
            output_name = Path(source_file).stem
            
        # Crear directorio de salida si no existe
        os.makedirs(self.output_dir, exist_ok=True)
        
        output_file = os.path.join(self.output_dir, f"{output_name}.exe")
        
        # Comando de compilación
        compile_cmd = [
            self.gcc_path,
            "-Wall",           # Mostrar todas las advertencias
            "-Wextra",         # Advertencias extra
            "-g3",            # Información de debug
            "-std=c++17",     # Estándar C++17
            source_file,
            "-o", output_file
        ]
        
        print(f"🔨 Compilando: {source_file}")
        print(f"📁 Salida: {output_file}")
        
        try:
            result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                print("✅ Compilación exitosa!")
                return output_file
            else:
                print("❌ Error de compilación:")
                print(result.stderr)
                return None
                
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el compilador en {self.gcc_path}")
            return None
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return None
    
    def run_executable(self, executable_path):
        """Ejecuta el archivo compilado"""
        print(f"🚀 Ejecutando: {executable_path}")
        print("=" * 50)
        
        try:
            result = subprocess.run(
                [executable_path],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.stdout:
                print("📤 Salida del programa:")
                print(result.stdout)
            
            if result.stderr:
                print("⚠️  Errores del programa:")
                print(result.stderr)
                
            print("=" * 50)
            print(f"✅ Programa terminado con código: {result.returncode}")
            
        except Exception as e:
            print(f"❌ Error al ejecutar: {e}")
    
    def compile_and_run(self, source_file, output_name=None):
        """Compila y ejecuta un archivo C++"""
        if not self.check_msys2_installation():
            return False
            
        executable = self.compile_file(source_file, output_name)
        if executable:
            self.run_executable(executable)
            return True
        return False
    
    def list_cpp_files(self):
        """Lista todos los archivos C++ disponibles"""
        cpp_files = self.find_cpp_files()
        if cpp_files:
            print("📁 Archivos C++ encontrados:")
            for i, file in enumerate(cpp_files, 1):
                print(f"  {i}. {file}")
        else:
            print("📁 No se encontraron archivos .cpp en el directorio actual")
        return cpp_files

def main():
    parser = argparse.ArgumentParser(description="Ejecutor C++ para MSYS2")
    parser.add_argument("file", nargs="?", help="Archivo .cpp a compilar y ejecutar")
    parser.add_argument("-l", "--list", action="store_true", help="Listar archivos .cpp disponibles")
    parser.add_argument("-o", "--output", help="Nombre del archivo de salida")
    
    args = parser.parse_args()
    
    executor = CppExecutor()
    
    if args.list:
        executor.list_cpp_files()
        return
    
    if not args.file:
        # Si no se especifica archivo, buscar automáticamente
        cpp_files = executor.find_cpp_files()
        if len(cpp_files) == 1:
            print(f"🎯 Archivo encontrado automáticamente: {cpp_files[0]}")
            executor.compile_and_run(cpp_files[0], args.output)
        elif len(cpp_files) > 1:
            print("📁 Múltiples archivos .cpp encontrados:")
            for i, file in enumerate(cpp_files, 1):
                print(f"  {i}. {file}")
            print("\n💡 Usa: python run.py <archivo.cpp>")
        else:
            print("📁 No se encontraron archivos .cpp")
            print("💡 Usa: python run.py <archivo.cpp>")
        return
    
    # Verificar que el archivo existe
    if not os.path.exists(args.file):
        print(f"❌ Error: El archivo {args.file} no existe")
        return
    
    # Compilar y ejecutar
    executor.compile_and_run(args.file, args.output)

if __name__ == "__main__":
    main()
