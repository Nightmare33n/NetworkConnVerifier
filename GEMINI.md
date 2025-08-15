# Project Overview

This project, "NetworkConnVerifier", is a network connectivity monitoring tool with a sophisticated graphical user interface (GUI) and a command-line interface (CLI). It is primarily written in Python and uses the `ping3`, `matplotlib`, and `tkinter` libraries. The project also includes a separate C++ development environment for compiling and running C++ code using MSYS2 on Windows.

The main application, located in the `NCV-Python` directory, provides real-time monitoring of network connectivity, including ping times and stability. The GUI version offers two visualization modes: a classic line graph and a Minecraft-style bar graph, providing a modern and user-friendly experience.

The C++ portion of the project, found in the `EjecutorCpp` and `NCV-Cpp` directories, appears to be a separate utility for C++ development and demonstration, not directly integrated with the Python application.

## Building and Running

### Python Application (NCV-Python)

To run the network connectivity verifier, you need Python 3.8+ and the required dependencies.

1.  **Install dependencies:**
    ```bash
    pip install -r NCV-Python/requirements.txt
    ```

2.  **Run the CLI version:**
    ```bash
    python NCV-Python/NetConnVer.py
    ```

3.  **Run the GUI version:**
    ```bash
    python NCV-Python/NetConnVerGUI.py
    ```

### C++ Execution Environment (EjecutorCpp)

The C++ execution environment is designed for Windows with MSYS2.

1.  **Prerequisites:**
    *   MSYS2 installed in `C:\msys64\`
    *   g++ compiler available in `C:\msys64\mingw64\bin\g++.exe`

2.  **Usage (from within the `EjecutorCpp` directory):**

    *   **Using Batch (recommended for Windows):**
        ```batch
        # Compile and run a specific file
        run.bat <file.cpp>

        # List available .cpp files
        run.bat -l
        ```

    *   **Using Python:**
        ```bash
        # Compile and run a specific file
        python run.py <file.cpp>

        # List available .cpp files
        python run.py -l
        ```

## Development Conventions

*   **Python:** The Python code is well-structured and follows common Python conventions. It uses type hinting and includes error handling for missing dependencies. The GUI application is built using `tkinter` and `matplotlib`, with a clear separation of UI and logic.
*   **C++:** The C++ code is simple and serves as an example. The `EjecutorCpp` environment provides a standardized way to compile and run C++ files with specific compiler flags (`-Wall`, `-Wextra`, `-g3`, `-std=c++17`).
*   **Cross-Platform:** The Python application is designed to be cross-platform (Windows, Linux, MacOS), while the C++ execution environment is specific to Windows with MSYS2.
