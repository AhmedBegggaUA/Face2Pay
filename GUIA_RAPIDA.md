# Guía Rápida - Face2Pay

## 🚀 Inicio Rápido

### Opción 1: Instalación Automática (Linux/Mac)

```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
streamlit run app.py
```

### Opción 2: Instalación Manual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

## 🎮 Cómo Usar la Aplicación

### Paso 1: Reconocimiento Facial
1. La aplicación mostrará una pantalla de reconocimiento facial
2. En modo demo, selecciona uno de los usuarios disponibles
3. Haz clic en "Reconocer Usuario"

### Paso 2: Verificación PIN
1. Ingresa el PIN del usuario seleccionado
2. Consulta la barra lateral para ver los PINs de demo
3. Haz clic en "Verificar PIN"

### Paso 3: Realizar Transacción
1. Ingresa el monto a pagar
2. Verifica que el saldo sea suficiente
3. Haz clic en "Pagar"
4. ¡Listo! La transacción se completará

## 👥 Usuarios de Demostración

| Usuario | PIN | Saldo |
|---------|-----|-------|
| Juan Pérez | 1234 | $1,500.00 |
| María García | 5678 | $2,300.50 |
| Carlos López | 9012 | $800.75 |

## 🔍 Características de la Demo

- ✅ Reconocimiento facial simulado (selección de usuario)
- ✅ Verificación de PIN funcional
- ✅ Procesamiento de transacciones en tiempo real
- ✅ Gestión de saldo
- ✅ Historial de transacciones
- ✅ Interfaz multilingüe (Español)

## 🛠️ Solución de Problemas

### Error al instalar face-recognition

Si tienes problemas instalando `face-recognition`, asegúrate de tener instalado:

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
sudo apt-get install libx11-dev libgtk-3-dev
```

**macOS:**
```bash
brew install cmake
```

**Windows:**
- Instala Visual Studio Build Tools
- O usa una versión precompilada de dlib

### La aplicación no se abre

Verifica que:
1. El entorno virtual esté activado
2. Todas las dependencias estén instaladas
3. El puerto 8501 no esté en uso
4. Ejecutas el comando desde el directorio del proyecto

### Error de módulos no encontrados

Asegúrate de:
1. Activar el entorno virtual antes de ejecutar
2. Instalar todas las dependencias: `pip install -r requirements.txt`

## 📞 Soporte

Para reportar problemas o sugerencias, abre un issue en el repositorio de GitHub.

## 🎯 Próximos Pasos

Esta es una versión de demostración. En una implementación real:

1. Integración con cámaras reales para captura facial
2. Modelos de reconocimiento facial entrenados con usuarios reales
3. Conexión con sistemas bancarios reales
4. Encriptación de datos sensibles
5. Autenticación multifactor adicional
6. Logs de auditoría y seguridad
7. Compliance con regulaciones financieras

---

**Face2Pay** - Hackathon #IBFH2025 🚀
