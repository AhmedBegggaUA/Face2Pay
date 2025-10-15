# Face2Pay 💳

Sistema de pago innovador mediante reconocimiento facial biométrico desarrollado para el Hackathon #IBFH2025.

## 📋 Descripción

Face2Pay es un dispositivo inteligente que combina tecnología de reconocimiento facial con sistemas de pago seguros. Permite a los usuarios realizar transacciones financieras de manera rápida y segura utilizando su rostro como método de identificación, complementado con un PIN de seguridad.

## 🎯 Características Principales

- **Reconocimiento Facial**: Identificación biométrica del usuario mediante tecnología de reconocimiento facial
- **Verificación por PIN**: Doble capa de seguridad con PIN de 4 dígitos
- **Gestión de Transacciones**: Procesamiento de pagos en tiempo real
- **Interfaz Intuitiva**: Aplicación web desarrollada con Streamlit
- **Historial de Transacciones**: Registro completo de todas las operaciones realizadas
- **Gestión de Saldo**: Control en tiempo real del saldo disponible

## 🚀 Proceso de Pago

1. **Reconocimiento Facial** 👤
   - El sistema captura la imagen del usuario
   - Realiza el reconocimiento facial
   - Identifica al usuario en la base de datos

2. **Verificación de PIN** 🔐
   - El usuario ingresa su PIN de 4 dígitos
   - El sistema valida la autenticidad

3. **Transacción** 💰
   - El usuario ingresa el monto a pagar
   - Se verifica el saldo disponible
   - Se procesa el pago y se actualiza el saldo

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**: Lenguaje de programación principal
- **Streamlit**: Framework para la interfaz web
- **OpenCV**: Procesamiento de imágenes
- **face-recognition**: Biblioteca de reconocimiento facial
- **NumPy**: Cálculos numéricos
- **Pillow**: Manejo de imágenes

## 📦 Instalación

### Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/AhmedBegggaUA/Face2Pay.git
cd Face2Pay
```

2. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## 🎮 Uso

1. Ejecutar la aplicación:
```bash
streamlit run app.py
```

2. La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

3. Para la demostración, puedes usar estos usuarios de prueba:

| Usuario | PIN | Saldo Inicial |
|---------|-----|---------------|
| Juan Pérez | 1234 | $1,500.00 |
| María García | 5678 | $2,300.50 |
| Carlos López | 9012 | $800.75 |

## 📱 Capturas de Pantalla

La aplicación presenta tres pasos principales:

1. **Pantalla de Reconocimiento Facial**: Captura e identificación del usuario
2. **Pantalla de Verificación PIN**: Validación de seguridad
3. **Pantalla de Transacción**: Procesamiento del pago

## 🔒 Seguridad

Face2Pay implementa múltiples capas de seguridad:

- **Autenticación biométrica**: Reconocimiento facial único por usuario
- **Verificación por PIN**: Código de seguridad personal
- **Validación de saldo**: Verificación antes de cada transacción
- **Registro de transacciones**: Auditoría completa de operaciones

## 🏆 Hackathon #IBFH2025

Este proyecto fue desarrollado para el Hackathon #IBFH2025, demostrando la integración de tecnologías biométricas con sistemas de pago modernos.

## 👥 Equipo de Desarrollo

Proyecto desarrollado por el equipo de Face2Pay para el Hackathon #IBFH2025.

## 📄 Licencia

Este proyecto está desarrollado con fines educativos y de demostración para el Hackathon #IBFH2025.

## 🤝 Contribuciones

Este es un proyecto de demostración para el hackathon. Para consultas o sugerencias, por favor abre un issue en el repositorio.

## 📞 Contacto

Para más información sobre el proyecto Face2Pay, visita nuestro repositorio en GitHub.

---

**Face2Pay** - Innovando en sistemas de pago biométricos 🚀