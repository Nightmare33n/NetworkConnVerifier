#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CPP Shell - Terminal interactiva para C++
Autor: Asistente
Descripción: Una terminal tipo PowerShell especializada para compilar y ejecutar C++
"""

import os
import sys
import subprocess
import glob
import shlex
from pathlib import Path
import readline
import atexit

class CPPShell:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.msys2_path = r"C:\msys64"
        self.gcc_path = r"C:\msys64\mingw64\bin\g++.exe"
        self.output_dir = "output"
        self.history_file = os.path.expanduser("~/.cppshell_history")
        self.load_history()
        
        # Colores para la terminal
        self.colors = {
            'RED': '\033[91m',
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'BLUE': '\033[94m',
            'MAGENTA': '\033[95m',
            'CYAN': '\033[96m',
            'WHITE': '\033[97m',
            'RESET': '\033[0m',
            'BOLD': '\033[1m'
        }
        
    def load_history(self):
        """Carga el historial de comandos"""
        try:
            readline.read_history_file(self.history_file)
        except FileNotFoundError:
            pass
        atexit.register(readline.write_history_file, self.history_file)
    
    def color_print(self, text, color='WHITE'):
        """Imprime texto con color"""
        print(f"{self.colors.get(color, '')}{text}{self.colors['RESET']}")
    
    def get_prompt(self):
        """Genera el prompt de la terminal"""
        current = Path(self.current_dir).name
        if current == "":
            current = Path(self.current_dir).drive.replace(":", "")
        
        return f"{self.colors['CYAN']}cppshell{self.colors['RESET']} {self.colors['GREEN']}{current}{self.colors['RESET']} $ "
    
    def show_help(self):
        """Muestra la ayuda de comandos"""
        help_text = f"""
{self.colors['CYAN']}╔══════════════════════════════════════════════════════════════╗{self.colors['RESET']}
{self.colors['CYAN']}║                    CPP SHELL - AYUDA                         ║{self.colors['RESET']}
{self.colors['CYAN']}╚══════════════════════════════════════════════════════════════╝{self.colors['RESET']}

{self.colors['YELLOW']}Comandos de navegación:{self.colors['RESET']}
  {self.colors['GREEN']}ls{self.colors['RESET']}                    - Listar archivos y carpetas
  {self.colors['GREEN']}cd <directorio>{self.colors['RESET']}        - Cambiar directorio
  {self.colors['GREEN']}cd ..{self.colors['RESET']}                 - Subir un nivel
  {self.colors['GREEN']}pwd{self.colors['RESET']}                   - Mostrar directorio actual
  {self.colors['GREEN']}clear{self.colors['RESET']}                 - Limpiar pantalla

{self.colors['YELLOW']}Comandos de C++:{self.colors['RESET']}
  {self.colors['GREEN']}cpp <archivo.cpp>{self.colors['RESET']}      - Compilar y ejecutar
  {self.colors['GREEN']}cpp -c <archivo.cpp>{self.colors['RESET']}   - Solo compilar
  {self.colors['GREEN']}cpp -l{self.colors['RESET']}                - Listar archivos .cpp
  {self.colors['GREEN']}cpp -r <archivo.exe>{self.colors['RESET']}   - Ejecutar archivo compilado

{self.colors['YELLOW']}Comandos del sistema:{self.colors['RESET']}
  {self.colors['GREEN']}python <archivo.py>{self.colors['RESET']}    - Ejecutar Python
  {self.colors['GREEN']}exit{self.colors['RESET']}                  - Salir de la terminal
  {self.colors['GREEN']}help{self.colors['RESET']}                  - Mostrar esta ayuda

{self.colors['YELLOW']}Ejemplos:{self.colors['RESET']}
  {self.colors['WHITE']}cpp hola.cpp{self.colors['RESET']}           - Compilar y ejecutar hola.cpp
  {self.colors['WHITE']}cpp -c test.cpp{self.colors['RESET']}        - Solo compilar test.cpp
  {self.colors['WHITE']}cd NCV-Cpp{self.colors['RESET']}            - Ir a carpeta NCV-Cpp
  {self.colors['WHITE']}ls{self.colors['RESET']}                    - Ver archivos
"""
        print(help_text)
    
    def list_files(self):
        """Lista archivos y carpetas (comando ls)"""
        try:
            items = os.listdir(self.current_dir)
            files = []
            dirs = []
            
            for item in items:
                item_path = os.path.join(self.current_dir, item)
                if os.path.isdir(item_path):
                    dirs.append(f"{self.colors['BLUE']}{item}/{self.colors['RESET']}")
                else:
                    # Colorear archivos por extensión
                    if item.endswith('.cpp'):
                        files.append(f"{self.colors['GREEN']}{item}{self.colors['RESET']}")
                    elif item.endswith('.exe'):
                        files.append(f"{self.colors['MAGENTA']}{item}{self.colors['RESET']}")
                    elif item.endswith('.py'):
                        files.append(f"{self.colors['YELLOW']}{item}{self.colors['RESET']}")
                    else:
                        files.append(item)
            
            # Mostrar directorios primero
            if dirs:
                print(" ".join(sorted(dirs)))
            if files:
                print(" ".join(sorted(files)))
                
        except Exception as e:
            self.color_print(f"Error al listar archivos: {e}", 'RED')
    
    def change_directory(self, path):
        """Cambia el directorio (comando cd)"""
        try:
            if path == "..":
                new_path = os.path.dirname(self.current_dir)
            else:
                new_path = os.path.abspath(os.path.join(self.current_dir, path))
            
            if os.path.exists(new_path) and os.path.isdir(new_path):
                self.current_dir = new_path
                os.chdir(self.current_dir)
                self.color_print(f"Directorio cambiado a: {self.current_dir}", 'GREEN')
            else:
                self.color_print(f"Error: El directorio '{path}' no existe", 'RED')
        except Exception as e:
            self.color_print(f"Error al cambiar directorio: {e}", 'RED')
    
    def show_current_dir(self):
        """Muestra el directorio actual (comando pwd)"""
        self.color_print(f"Directorio actual: {self.current_dir}", 'CYAN')
    
    def clear_screen(self):
        """Limpia la pantalla (comando clear)"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def find_cpp_files(self):
        """Encuentra archivos .cpp en el directorio actual"""
        cpp_files = []
        for ext in ['*.cpp', '*.cxx', '*.cc']:
            cpp_files.extend(glob.glob(os.path.join(self.current_dir, ext)))
        return cpp_files
    
    def compile_cpp(self, source_file, compile_only=False):
        """Compila un archivo C++"""
        if not os.path.exists(source_file):
            self.color_print(f"Error: El archivo '{source_file}' no existe", 'RED')
            return None
        
        # Crear directorio de salida si no existe
        output_dir = os.path.join(self.current_dir, self.output_dir)
        os.makedirs(output_dir, exist_ok=True)
        
        # Determinar nombre de salida
        output_name = Path(source_file).stem
        output_file = os.path.join(output_dir, f"{output_name}.exe")
        
        # Comando de compilación
        compile_cmd = [
            self.gcc_path,
            "-Wall",
            "-Wextra", 
            "-g3",
            "-std=c++17",
            source_file,
            "-o", output_file
        ]
        
        self.color_print(f"🔨 Compilando: {source_file}", 'MAGENTA')
        self.color_print(f"📁 Salida: {output_file}", 'BLUE')
        
        try:
            result = subprocess.run(
                compile_cmd,
                capture_output=True,
                text=True,
                cwd=self.current_dir
            )
            
            if result.returncode == 0:
                self.color_print("✅ Compilación exitosa!", 'GREEN')
                return output_file if not compile_only else None
            else:
                self.color_print("❌ Error de compilación:", 'RED')
                print(result.stderr)
                return None
                
        except FileNotFoundError:
            self.color_print(f"❌ Error: No se encontró el compilador en {self.gcc_path}", 'RED')
            return None
        except Exception as e:
            self.color_print(f"❌ Error inesperado: {e}", 'RED')
            return None
    
    def run_executable(self, executable_path):
        """Ejecuta un archivo compilado"""
        if not os.path.exists(executable_path):
            self.color_print(f"Error: El archivo '{executable_path}' no existe", 'RED')
            return
        
        self.color_print(f"🚀 Ejecutando: {executable_path}", 'CYAN')
        self.color_print("=" * 50, 'CYAN')
        
        try:
            result = subprocess.run(
                [executable_path],
                capture_output=True,
                text=True,
                cwd=self.current_dir
            )
            
            if result.stdout:
                print(result.stdout)
            
            if result.stderr:
                self.color_print("⚠️  Errores del programa:", 'YELLOW')
                print(result.stderr)
                
            self.color_print("=" * 50, 'CYAN')
            self.color_print(f"✅ Programa terminado con código: {result.returncode}", 'GREEN')
            
        except Exception as e:
            self.color_print(f"❌ Error al ejecutar: {e}", 'RED')
    
    def handle_cpp_command(self, args):
        """Maneja el comando cpp"""
        if not args:
            # Si no hay argumentos, buscar automáticamente
            cpp_files = self.find_cpp_files()
            if len(cpp_files) == 1:
                self.color_print(f"🎯 Archivo encontrado automáticamente: {cpp_files[0]}", 'GREEN')
                return self.handle_cpp_file(cpp_files[0], False)
            elif len(cpp_files) > 1:
                self.color_print("📁 Múltiples archivos .cpp encontrados:", 'YELLOW')
                for i, file in enumerate(cpp_files, 1):
                    print(f"  {i}. {file}")
                self.color_print("💡 Usa: cpp <archivo.cpp>", 'WHITE')
            else:
                self.color_print("📁 No se encontraron archivos .cpp", 'YELLOW')
                self.color_print("💡 Usa: cpp <archivo.cpp>", 'WHITE')
            return
        
        if args[0] == "-l":
            # Listar archivos .cpp
            cpp_files = self.find_cpp_files()
            if cpp_files:
                self.color_print("📁 Archivos .cpp encontrados:", 'BLUE')
                for i, file in enumerate(cpp_files, 1):
                    print(f"  {i}. {file}")
            else:
                self.color_print("📁 No se encontraron archivos .cpp", 'YELLOW')
            return
        
        if args[0] == "-c":
            # Solo compilar
            if len(args) < 2:
                self.color_print("Error: Especifica un archivo para compilar", 'RED')
                return
            self.handle_cpp_file(args[1], True)
            return
        
        if args[0] == "-r":
            # Ejecutar archivo compilado
            if len(args) < 2:
                self.color_print("Error: Especifica un archivo para ejecutar", 'RED')
                return
            self.run_executable(args[1])
            return
        
        # Compilar y ejecutar
        self.handle_cpp_file(args[0], False)
    
    def handle_cpp_file(self, filename, compile_only=False):
        """Maneja la compilación y ejecución de un archivo C++"""
        # Buscar el archivo en el directorio actual
        file_path = os.path.join(self.current_dir, filename)
        
        if not os.path.exists(file_path):
            self.color_print(f"Error: El archivo '{filename}' no existe", 'RED')
            return
        
        executable = self.compile_cpp(file_path, compile_only)
        if executable and not compile_only:
            self.run_executable(executable)
    
    def execute_system_command(self, command):
        """Ejecuta comandos del sistema"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.current_dir
            )
            
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
                
        except Exception as e:
            self.color_print(f"Error al ejecutar comando: {e}", 'RED')
    
    def run(self):
        """Ejecuta la terminal interactiva"""
        self.color_print("🚀 CPP Shell iniciado - Terminal interactiva para C++", 'CYAN')
        self.color_print("💡 Escribe 'help' para ver los comandos disponibles", 'WHITE')
        print()
        
        while True:
            try:
                # Cambiar al directorio actual
                os.chdir(self.current_dir)
                
                # Obtener comando del usuario
                command = input(self.get_prompt()).strip()
                
                if not command:
                    continue
                
                # Guardar en historial
                readline.add_history(command)
                
                # Parsear comando
                args = shlex.split(command)
                if not args:
                    continue
                
                cmd = args[0].lower()
                cmd_args = args[1:]
                
                # Procesar comandos
                if cmd == "exit":
                    self.color_print("👋 ¡Hasta luego!", 'GREEN')
                    break
                elif cmd == "help":
                    self.show_help()
                elif cmd == "ls":
                    self.list_files()
                elif cmd == "cd":
                    if cmd_args:
                        self.change_directory(cmd_args[0])
                    else:
                        self.color_print("Error: Especifica un directorio", 'RED')
                elif cmd == "pwd":
                    self.show_current_dir()
                elif cmd == "clear":
                    self.clear_screen()
                elif cmd == "cpp":
                    self.handle_cpp_command(cmd_args)
                elif cmd == "python":
                    if cmd_args:
                        self.execute_system_command(f"python {' '.join(cmd_args)}")
                    else:
                        self.color_print("Error: Especifica un archivo Python", 'RED')
                else:
                    # Intentar ejecutar como comando del sistema
                    self.execute_system_command(command)
                    
            except KeyboardInterrupt:
                print()
                self.color_print("💡 Usa 'exit' para salir", 'YELLOW')
            except EOFError:
                break
            except Exception as e:
                self.color_print(f"Error: {e}", 'RED')

if __name__ == "__main__":
    shell = CPPShell()
    shell.run() 