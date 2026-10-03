#!/usr/bin/env bash

# Exit on error
set -e

# Navigate to project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================================"
echo "         🌊 AquaFlow Tracker — Starting Project 🌊          "
echo "============================================================"

# Function to find a working Python executable (skips broken WindowsApp stubs)
find_python() {
    for cmd in "python" "python3" "py"; do
        if command -v "$cmd" &>/dev/null; then
            if "$cmd" --version &>/dev/null; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    return 1
}

# 1. Ensure .env file exists
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "[i] .env file not found. Copying from .env.example..."
        cp .env.example .env
        echo "[✓] Created .env file."
    else
        echo "[!] Warning: Neither .env nor .env.example found."
    fi
else
    echo "[✓] Found .env configuration file."
fi

# 2. Virtual environment detection and activation
VENV_ACTIVATED=0
for VENV_DIR in ".venv" ".venv-2" "venv" "env"; do
    if [ -d "$VENV_DIR" ]; then
        if [ -f "$VENV_DIR/Scripts/activate" ]; then
            echo "[i] Activating virtual environment from '$VENV_DIR/Scripts/activate'..."
            source "$VENV_DIR/Scripts/activate"
            VENV_ACTIVATED=1
            break
        elif [ -f "$VENV_DIR/bin/activate" ]; then
            echo "[i] Activating virtual environment from '$VENV_DIR/bin/activate'..."
            source "$VENV_DIR/bin/activate"
            VENV_ACTIVATED=1
            break
        fi
    fi
done

if [ $VENV_ACTIVATED -eq 0 ]; then
    echo "[i] No existing virtual environment found. Creating '.venv'..."
    SYS_PYTHON=$(find_python) || {
        echo "[X] Error: No working Python installation found in PATH."
        exit 1
    }

    $SYS_PYTHON -m venv .venv
    if [ -f ".venv/Scripts/activate" ]; then
        source .venv/Scripts/activate
    elif [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
    fi
    echo "[✓] Created and activated virtual environment '.venv'."
fi

# 3. Determine active Python binary
PY_CMD=$(find_python) || {
    echo "[X] Error: Python executable not found after activation."
    exit 1
}

# 4. Check & install dependencies if needed
if [ -f "requirements.txt" ]; then
    if ! $PY_CMD -c "import flask, dotenv, supabase" &>/dev/null; then
        echo "[i] Installing missing dependencies from requirements.txt..."
        $PY_CMD -m pip install -r requirements.txt
        echo "[✓] Dependencies installed successfully."
    else
        echo "[✓] All core dependencies are installed."
    fi
fi

# 5. Determine host and port
HOST="127.0.0.1"
PORT="5000"
if [ -f ".env" ]; then
    ENV_HOST=$(grep -E "^HOST=" .env | cut -d '=' -f2 | tr -d '\r" ' || true)
    ENV_PORT=$(grep -E "^PORT=" .env | cut -d '=' -f2 | tr -d '\r" ' || true)
    if [ -n "$ENV_HOST" ]; then HOST="$ENV_HOST"; fi
    if [ -n "$ENV_PORT" ]; then PORT="$ENV_PORT"; fi
fi

# 6. Start Application
echo "------------------------------------------------------------"
echo "🚀 Server launching at: http://${HOST}:${PORT}"
echo "💡 Press Ctrl+C to stop the server."
echo "------------------------------------------------------------"

exec $PY_CMD app.py
