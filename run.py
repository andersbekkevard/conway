#!/usr/bin/env python3
"""
Conway's Game of Life - Launcher Script

This script automatically activates the virtual environment and runs the main application.
Use this instead of manually activating venv and running main.py.

Usage:
    python run.py
    # OR
    python3 run.py
    # OR (if executable)
    ./run.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def find_venv_path():
    """Find the virtual environment directory."""
    current_dir = Path(__file__).parent

    # Common venv directory names
    venv_names = ["venv", ".venv", "env", ".env"]

    for venv_name in venv_names:
        venv_path = current_dir / venv_name
        if venv_path.exists() and venv_path.is_dir():
            return venv_path

    return None


def get_python_executable(venv_path):
    """Get the Python executable path from the virtual environment."""
    system = platform.system().lower()

    if system == "windows":
        python_exe = venv_path / "Scripts" / "python.exe"
        if not python_exe.exists():
            python_exe = venv_path / "Scripts" / "python3.exe"
    else:  # Unix/Linux/macOS
        python_exe = venv_path / "bin" / "python"
        if not python_exe.exists():
            python_exe = venv_path / "bin" / "python3"

    return python_exe if python_exe.exists() else None


def check_dependencies(python_exe):
    """Check if required dependencies are installed in the venv."""
    try:
        # Check for pygame, numpy, and scipy
        result = subprocess.run(
            [
                str(python_exe),
                "-c",
                "import pygame, numpy, scipy; print('Dependencies OK')",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )

        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def install_dependencies(python_exe):
    """Install dependencies from requirements.txt."""
    requirements_file = Path(__file__).parent / "requirements.txt"

    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        return False

    print("📦 Installing dependencies...")
    try:
        result = subprocess.run(
            [str(python_exe), "-m", "pip", "install", "-r", str(requirements_file)],
            timeout=120,
        )

        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Installation timed out!")
        return False


def run_main(python_exe):
    """Run the main.py file using the venv Python."""
    main_file = Path(__file__).parent / "main.py"

    if not main_file.exists():
        print("❌ main.py not found!")
        return False

    print("🎮 Starting Conway's Game of Life...")
    print(f"🐍 Using Python: {python_exe}")
    print("─" * 50)

    try:
        # Run main.py with the venv Python
        result = subprocess.run([str(python_exe), str(main_file)])
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\n🛑 Game stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error running main.py: {e}")
        return False


def main():
    """Main launcher function."""
    print("🚀 Conway's Game of Life Launcher")
    print("=" * 40)

    # Find virtual environment
    venv_path = find_venv_path()
    if not venv_path:
        print("❌ Virtual environment not found!")
        print("Expected to find one of: venv, .venv, env, .env")
        print("\nPlease create a virtual environment:")
        print("  python -m venv venv")
        print("  source venv/bin/activate  # macOS/Linux")
        print("  # OR")
        print("  venv\\Scripts\\activate     # Windows")
        print("  pip install -r requirements.txt")
        return 1

    print(f"✅ Found virtual environment: {venv_path}")

    # Get Python executable
    python_exe = get_python_executable(venv_path)
    if not python_exe:
        print(f"❌ Python executable not found in {venv_path}")
        print("The virtual environment might be corrupted.")
        return 1

    print(f"✅ Found Python executable: {python_exe}")

    # Check dependencies
    if not check_dependencies(python_exe):
        print("⚠️  Dependencies missing or outdated")
        if not install_dependencies(python_exe):
            print("❌ Failed to install dependencies!")
            print("\nTry manually:")
            print(f"  source {venv_path}/bin/activate")
            print("  pip install -r requirements.txt")
            return 1
        print("✅ Dependencies installed successfully")
    else:
        print("✅ All dependencies are available")

    # Run the game
    success = run_main(python_exe)

    if success:
        print("\n🎉 Game finished successfully!")
        return 0
    else:
        print("\n❌ Game ended with errors")
        return 1


if __name__ == "__main__":
    sys.exit(main())
