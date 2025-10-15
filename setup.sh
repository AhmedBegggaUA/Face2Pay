#!/bin/bash

echo "==================================="
echo "Face2Pay - Setup Script"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 no está instalado. Por favor, instala Python 3.8 o superior."
    exit 1
fi

echo "✅ Python3 encontrado: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Install dependencies
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "==================================="
echo "✅ ¡Instalación completada!"
echo "==================================="
echo ""
echo "Para ejecutar la aplicación:"
echo "1. Activa el entorno virtual: source venv/bin/activate"
echo "2. Ejecuta: streamlit run app.py"
echo ""
