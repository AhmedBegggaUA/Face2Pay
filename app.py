import streamlit as st
import cv2
import numpy as np
from PIL import Image
import face_recognition
import os
import json
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Face2Pay - Sistema de Pago Facial",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1E88E5;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .subtitle {
        text-align: center;
        color: #424242;
        font-size: 1.5em;
        margin-bottom: 30px;
    }
    .section-header {
        color: #1E88E5;
        font-size: 2em;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #C8E6C9;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #FFCDD2;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar variables de sesión
if 'usuarios_db' not in st.session_state:
    st.session_state.usuarios_db = {
        'usuario1': {
            'nombre': 'Juan Pérez',
            'pin': '1234',
            'saldo': 1500.00,
            'encoding': None
        },
        'usuario2': {
            'nombre': 'María García',
            'pin': '5678',
            'saldo': 2300.50,
            'encoding': None
        },
        'usuario3': {
            'nombre': 'Carlos López',
            'pin': '9012',
            'saldo': 800.75,
            'encoding': None
        }
    }

if 'usuario_actual' not in st.session_state:
    st.session_state.usuario_actual = None

if 'paso_actual' not in st.session_state:
    st.session_state.paso_actual = 1  # 1: Reconocimiento facial, 2: PIN, 3: Transacción

if 'transacciones' not in st.session_state:
    st.session_state.transacciones = []

# Funciones auxiliares
def detectar_rostro(imagen):
    """Detecta rostros en una imagen"""
    try:
        # Convertir la imagen a RGB si es necesario
        if len(imagen.shape) == 2:
            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGB)
        else:
            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        
        # Detectar ubicaciones de rostros
        ubicaciones_rostros = face_recognition.face_locations(imagen_rgb)
        
        if len(ubicaciones_rostros) > 0:
            # Obtener encodings
            encodings = face_recognition.face_encodings(imagen_rgb, ubicaciones_rostros)
            return True, encodings, ubicaciones_rostros
        return False, None, None
    except Exception as e:
        st.error(f"Error al detectar rostro: {str(e)}")
        return False, None, None

def verificar_pin(pin_ingresado):
    """Verifica el PIN del usuario actual"""
    if st.session_state.usuario_actual:
        usuario_id = st.session_state.usuario_actual
        return st.session_state.usuarios_db[usuario_id]['pin'] == pin_ingresado
    return False

def realizar_transaccion(monto):
    """Procesa una transacción"""
    if st.session_state.usuario_actual:
        usuario_id = st.session_state.usuario_actual
        usuario = st.session_state.usuarios_db[usuario_id]
        
        if usuario['saldo'] >= monto:
            usuario['saldo'] -= monto
            transaccion = {
                'fecha': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'usuario': usuario['nombre'],
                'monto': monto,
                'saldo_restante': usuario['saldo']
            }
            st.session_state.transacciones.append(transaccion)
            return True, usuario['saldo']
        return False, usuario['saldo']
    return False, 0

def reiniciar_sesion():
    """Reinicia la sesión actual"""
    st.session_state.usuario_actual = None
    st.session_state.paso_actual = 1

# Header
st.markdown('<h1 class="main-title">💳 Face2Pay</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sistema de Pago mediante Reconocimiento Facial - Hackathon #IBFH2025</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📋 Información del Sistema")
    st.markdown("---")
    
    st.markdown("#### ℹ️ Acerca de Face2Pay")
    st.markdown("""
    Face2Pay es un innovador dispositivo de pago que utiliza reconocimiento facial 
    para identificar usuarios de manera segura y realizar transacciones financieras.
    """)
    
    st.markdown("#### 🔐 Proceso de Pago")
    st.markdown("""
    1. **Reconocimiento Facial**: El sistema captura y analiza tu rostro
    2. **Verificación PIN**: Ingresa tu PIN de seguridad
    3. **Transacción**: Realiza tu pago de forma segura
    """)
    
    st.markdown("---")
    st.markdown("#### 👥 Usuarios Demo")
    for usuario_id, datos in st.session_state.usuarios_db.items():
        st.markdown(f"**{datos['nombre']}**")
        st.markdown(f"- PIN: `{datos['pin']}`")
        st.markdown(f"- Saldo: ${datos['saldo']:.2f}")
        st.markdown("---")
    
    if st.button("🔄 Reiniciar Sesión", use_container_width=True):
        reiniciar_sesion()
        st.rerun()

# Contenido principal
st.markdown("---")

# Estado actual
col1, col2, col3 = st.columns(3)
with col1:
    if st.session_state.paso_actual >= 1:
        st.markdown("✅ **Paso 1: Reconocimiento Facial**")
    else:
        st.markdown("⭕ **Paso 1: Reconocimiento Facial**")

with col2:
    if st.session_state.paso_actual >= 2:
        st.markdown("✅ **Paso 2: Verificación PIN**")
    else:
        st.markdown("⭕ **Paso 2: Verificación PIN**")

with col3:
    if st.session_state.paso_actual >= 3:
        st.markdown("✅ **Paso 3: Transacción**")
    else:
        st.markdown("⭕ **Paso 3: Transacción**")

st.markdown("---")

# Paso 1: Reconocimiento Facial
if st.session_state.paso_actual == 1:
    st.markdown('<h2 class="section-header">👤 Reconocimiento Facial</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    <h3>📸 Captura tu rostro para identificarte</h3>
    <p>Para esta demostración, simularemos el reconocimiento facial. 
    Selecciona un usuario para continuar con el proceso de pago.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulación de reconocimiento facial
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Selecciona tu identidad (Demo)")
        usuario_seleccionado = st.selectbox(
            "Usuario:",
            options=list(st.session_state.usuarios_db.keys()),
            format_func=lambda x: st.session_state.usuarios_db[x]['nombre']
        )
        
        if st.button("🎯 Reconocer Usuario", type="primary", use_container_width=True):
            st.session_state.usuario_actual = usuario_seleccionado
            st.session_state.paso_actual = 2
            st.success(f"✅ Usuario reconocido: {st.session_state.usuarios_db[usuario_seleccionado]['nombre']}")
            st.rerun()
    
    with col2:
        st.image("https://via.placeholder.com/300x300.png?text=Face+Recognition", 
                caption="Simulación de Cámara")

# Paso 2: Verificación PIN
elif st.session_state.paso_actual == 2:
    st.markdown('<h2 class="section-header">🔐 Verificación de PIN</h2>', unsafe_allow_html=True)
    
    usuario = st.session_state.usuarios_db[st.session_state.usuario_actual]
    
    st.markdown(f"""
    <div class="info-box">
    <h3>👤 Usuario: {usuario['nombre']}</h3>
    <p>Por favor, ingresa tu PIN de seguridad para continuar.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        pin_ingresado = st.text_input(
            "PIN de 4 dígitos:",
            max_chars=4,
            type="password",
            placeholder="****"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("✅ Verificar PIN", type="primary", use_container_width=True):
                if verificar_pin(pin_ingresado):
                    st.session_state.paso_actual = 3
                    st.success("✅ PIN correcto. Acceso concedido.")
                    st.rerun()
                else:
                    st.error("❌ PIN incorrecto. Intenta nuevamente.")
        
        with col_btn2:
            if st.button("🔙 Volver", use_container_width=True):
                st.session_state.paso_actual = 1
                st.session_state.usuario_actual = None
                st.rerun()

# Paso 3: Transacción
elif st.session_state.paso_actual == 3:
    st.markdown('<h2 class="section-header">💰 Realizar Transacción</h2>', unsafe_allow_html=True)
    
    usuario = st.session_state.usuarios_db[st.session_state.usuario_actual]
    
    st.markdown(f"""
    <div class="success-box">
    <h3>👤 Usuario: {usuario['nombre']}</h3>
    <h4>💵 Saldo actual: ${usuario['saldo']:.2f}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        monto = st.number_input(
            "Monto a pagar ($):",
            min_value=0.01,
            max_value=float(usuario['saldo']),
            value=10.00,
            step=0.01
        )
        
        st.markdown(f"**Saldo restante después del pago:** ${usuario['saldo'] - monto:.2f}")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("💳 Pagar", type="primary", use_container_width=True):
                exito, saldo_restante = realizar_transaccion(monto)
                
                if exito:
                    st.balloons()
                    st.success(f"""
                    ✅ ¡Pago realizado con éxito!
                    
                    **Monto pagado:** ${monto:.2f}
                    
                    **Saldo restante:** ${saldo_restante:.2f}
                    """)
                    
                    # Esperar un momento antes de reiniciar
                    import time
                    time.sleep(2)
                    reiniciar_sesion()
                    st.rerun()
                else:
                    st.error("❌ Saldo insuficiente para realizar la transacción.")
        
        with col_btn2:
            if st.button("❌ Cancelar", use_container_width=True):
                reiniciar_sesion()
                st.rerun()

# Sección de historial de transacciones
if len(st.session_state.transacciones) > 0:
    st.markdown("---")
    st.markdown('<h2 class="section-header">📊 Historial de Transacciones</h2>', unsafe_allow_html=True)
    
    for i, trans in enumerate(reversed(st.session_state.transacciones[-5:])):
        st.markdown(f"""
        <div class="info-box">
        <strong>Transacción #{len(st.session_state.transacciones) - i}</strong><br>
        📅 Fecha: {trans['fecha']}<br>
        👤 Usuario: {trans['usuario']}<br>
        💵 Monto: ${trans['monto']:.2f}<br>
        💰 Saldo restante: ${trans['saldo_restante']:.2f}
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #757575;">
    <p><strong>Face2Pay</strong> - Hackathon #IBFH2025</p>
    <p>Sistema de pago seguro mediante reconocimiento facial biométrico</p>
</div>
""", unsafe_allow_html=True)
