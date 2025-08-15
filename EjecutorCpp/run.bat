@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: Configuración de MSYS2
set MSYS2_PATH=C:\msys64
set GCC_PATH=%MSYS2_PATH%\mingw64\bin\g++.exe
set OUTPUT_DIR=output

:: Colores para la salida
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "MAGENTA=[95m"
set "CYAN=[96m"
set "WHITE=[97m"
set "RESET=[0m"

echo %CYAN%╔══════════════════════════════════════════════════════════════╗%RESET%
echo %CYAN%║                    EJECUTOR C++ PARA MSYS2                   ║%RESET%
echo %CYAN%║                                                              ║%RESET%
echo %CYAN%║  Uso: run.bat [archivo.cpp] [opciones]                       ║%RESET%
echo %CYAN%║  Opciones:                                                   ║%RESET%
echo %CYAN%║    -l, --list     Listar archivos .cpp disponibles           ║%RESET%
echo %CYAN%║    -o nombre      Especificar nombre de salida               ║%RESET%
echo %CYAN%║    -c             Solo compilar, no ejecutar                 ║%RESET%
echo %CYAN%╚══════════════════════════════════════════════════════════════╝%RESET%
echo.

:: Verificar que MSYS2 esté instalado
if not exist "%MSYS2_PATH%\mingw64.exe" (
    echo %RED%❌ Error: No se encontró MSYS2 en %MSYS2_PATH%%RESET%
    echo %YELLOW%💡 Asegúrate de tener MSYS2 instalado en C:\msys64\%RESET%
    pause
    exit /b 1
)

:: Verificar que g++ esté disponible
if not exist "%GCC_PATH%" (
    echo %RED%❌ Error: No se encontró g++ en %GCC_PATH%%RESET%
    echo %YELLOW%💡 Asegúrate de tener el compilador instalado en MSYS2%RESET%
    pause
    exit /b 1
)

:: Variables para argumentos
set "SOURCE_FILE="
set "OUTPUT_NAME="
set "COMPILE_ONLY="
set "LIST_FILES="

:: Procesar argumentos
:parse_args
if "%~1"=="" goto :main_logic
if /i "%~1"=="-l" (
    set "LIST_FILES=1"
    shift
    goto :parse_args
)
if /i "%~1"=="--list" (
    set "LIST_FILES=1"
    shift
    goto :parse_args
)
if /i "%~1"=="-o" (
    set "OUTPUT_NAME=%~2"
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="-c" (
    set "COMPILE_ONLY=1"
    shift
    goto :parse_args
)
if not defined SOURCE_FILE (
    set "SOURCE_FILE=%~1"
)
shift
goto :parse_args

:main_logic
:: Listar archivos si se solicita
if defined LIST_FILES (
    echo %BLUE%📁 Archivos .cpp encontrados:%RESET%
    set "found=0"
    for %%f in (*.cpp) do (
        echo %WHITE%  • %%f%RESET%
        set "found=1"
    )
    if !found!==0 (
        echo %YELLOW%📁 No se encontraron archivos .cpp en el directorio actual%RESET%
    )
    goto :end
)

:: Si no se especificó archivo, buscar automáticamente
if not defined SOURCE_FILE (
    set "cpp_count=0"
    for %%f in (*.cpp) do set /a cpp_count+=1
    
    if !cpp_count!==0 (
        echo %YELLOW%📁 No se encontraron archivos .cpp%RESET%
        echo %WHITE%💡 Usa: run.bat archivo.cpp%RESET%
        goto :end
    )
    
    if !cpp_count!==1 (
        for %%f in (*.cpp) do set "SOURCE_FILE=%%f"
        echo %GREEN%🎯 Archivo encontrado automáticamente: !SOURCE_FILE!%RESET%
    ) else (
        echo %YELLOW%📁 Múltiples archivos .cpp encontrados:%RESET%
        for %%f in (*.cpp) do echo %WHITE%  • %%f%RESET%
        echo %WHITE%💡 Usa: run.bat archivo.cpp%RESET%
        goto :end
    )
)

:: Verificar que el archivo existe
if not exist "!SOURCE_FILE!" (
    echo %RED%❌ Error: El archivo !SOURCE_FILE! no existe%RESET%
    goto :end
)

:: Crear directorio de salida
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

:: Determinar nombre de salida
if not defined OUTPUT_NAME (
    for %%f in ("!SOURCE_FILE!") do set "OUTPUT_NAME=%%~nf"
)

:: Compilar
echo %MAGENTA%🔨 Compilando: !SOURCE_FILE!%RESET%
echo %BLUE%📁 Salida: %OUTPUT_DIR%\!OUTPUT_NAME!.exe%RESET%

"%GCC_PATH%" -Wall -Wextra -g3 -std=c++17 "!SOURCE_FILE!" -o "%OUTPUT_DIR%\!OUTPUT_NAME!.exe"

if !errorlevel!==0 (
    echo %GREEN%✅ Compilación exitosa!%RESET%
    
    :: Ejecutar si no es solo compilación
    if not defined COMPILE_ONLY (
        echo.
        echo %CYAN%🚀 Ejecutando: %OUTPUT_DIR%\!OUTPUT_NAME!.exe%RESET%
        echo %CYAN%══════════════════════════════════════════════════════════════%RESET%
        "%OUTPUT_DIR%\!OUTPUT_NAME!.exe"
        echo %CYAN%══════════════════════════════════════════════════════════════%RESET%
        echo %GREEN%✅ Programa terminado%RESET%
    )
) else (
    echo %RED%❌ Error de compilación%RESET%
)

:end
echo.
pause 