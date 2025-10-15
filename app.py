import streamlit as st
import base64
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Face2Pay - Pagos Biométricos",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estado del tema
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# CSS personalizado con modo día/noche y responsive
st.markdown(f"""
<style>
    /* Importar fuentes modernas */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Variables de color para modo oscuro */
    :root {{
        --bg-primary: {'#0f172a' if st.session_state.dark_mode else '#ffffff'};
        --bg-secondary: {'#1e293b' if st.session_state.dark_mode else '#f8fafc'};
        --bg-card: {'#1e293b' if st.session_state.dark_mode else '#ffffff'};
        --bg-gradient-start: {'#667eea' if st.session_state.dark_mode else '#667eea'};
        --bg-gradient-end: {'#764ba2' if st.session_state.dark_mode else '#764ba2'};
        
        --text-primary: {'#f1f5f9' if st.session_state.dark_mode else '#0f172a'};
        --text-secondary: {'#cbd5e1' if st.session_state.dark_mode else '#475569'};
        --text-tertiary: {'#94a3b8' if st.session_state.dark_mode else '#64748b'};
        
        --border-color: {'#334155' if st.session_state.dark_mode else '#e2e8f0'};
        --shadow-color: {'rgba(0, 0, 0, 0.5)' if st.session_state.dark_mode else 'rgba(0, 0, 0, 0.1)'};
        
        --accent-color: #667eea;
        --accent-light: #8b9dff;
        --success-color: #10b981;
        --warning-color: #f59e0b;
    }}
    
    /* Reset y estilos globales */
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Fondo principal - cambia según el modo */
.stApp {{
    background: {'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' if st.session_state.dark_mode else 'linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%)'};
    transition: background 0.3s ease;
}}
    
    /* Contenedor principal */
    .main-container {{
        background: var(--bg-card);
        border-radius: 24px;
        padding: 2rem;
        margin: 1rem auto;
        max-width: 1200px;
        box-shadow: 0 20px 60px var(--shadow-color);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }}
    
    /* Header con logo */
    .header-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
        gap: 1.5rem;
        flex-wrap: wrap;
    }}
    
    .logo-container {{
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: {'rgba(255, 255, 255, 0.1)' if st.session_state.dark_mode else '#ffffff'};
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 30px var(--shadow-color);
        flex-shrink: 0;
    }}
    
    .logo-container img {{
        width: 80px;
        height: 80px;
        object-fit: contain;
    }}
    
    /* Títulos */
    .main-title {{
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        letter-spacing: -1px;
        text-align: center;
    }}
    
    .subtitle {{
        font-size: 1.1rem;
        color: var(--text-secondary);
        font-weight: 400;
        margin-top: 0.5rem;
        text-align: center;
    }}
    
    /* Tarjetas de características */
    .feature-card {{
        background: var(--bg-secondary);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid var(--border-color);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .feature-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px var(--shadow-color);
        border-color: var(--accent-color);
    }}
    
    .feature-title {{
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        flex-wrap: wrap;
    }}
    
    .feature-icon {{
        font-size: 1.8rem;
        flex-shrink: 0;
    }}
    
    .feature-text {{
        color: var(--text-secondary);
        font-size: 1rem;
        line-height: 1.7;
    }}
    
    .feature-text p {{
        color: var(--text-secondary);
        margin-bottom: 0.75rem;
    }}
    
    .feature-text ul {{
        color: var(--text-secondary);
    }}
    
    .feature-text li {{
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
    }}
    
    .feature-text strong {{
        color: var(--text-primary);
    }}
    
    /* Sección de tecnologías */
    .tech-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }}
    
    .tech-card {{
        background: var(--bg-card);
        border: 2px solid var(--border-color);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px var(--shadow-color);
        transition: all 0.3s ease;
    }}
    
    .tech-card:hover {{
        transform: scale(1.05);
        box-shadow: 0 8px 25px var(--shadow-color);
        border-color: var(--accent-color);
    }}
    
    .tech-icon {{
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }}
    
    .tech-name {{
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }}
    
    .tech-description {{
        font-size: 0.9rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }}
    
    /* Demo section */
    .demo-container {{
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        text-align: center;
    }}
    
    .demo-container h1, .demo-container h2, .demo-container p {{
        color: white !important;
    }}
    
    .camera-preview {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem auto;
        max-width: 600px;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }}
    
    /* Botón de tema */
    .theme-toggle {{
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 9999;
        background: var(--bg-card);
        border: 2px solid var(--border-color);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 1.5rem;
        box-shadow: 0 4px 15px var(--shadow-color);
        transition: all 0.3s ease;
    }}
    
    .theme-toggle:hover {{
        transform: scale(1.1);
        box-shadow: 0 6px 20px var(--shadow-color);
    }}
    
    /* Secciones con badges */
    .section-badge {{
        display: inline-block;
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1rem;
        box-shadow: 0 4px 10px var(--shadow-color);
    }}
    
    /* Timeline de proceso */
    .process-timeline {{
        position: relative;
        padding: 1.5rem 0;
    }}
    
    .process-step {{
        display: flex;
        align-items: flex-start;
        margin-bottom: 1.5rem;
        position: relative;
    }}
    
    .step-number {{
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1.2rem;
        box-shadow: 0 4px 15px var(--shadow-color);
        flex-shrink: 0;
    }}
    
    .step-content {{
        margin-left: 1rem;
        flex: 1;
    }}
    
    .step-title {{
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }}
    
    .step-description {{
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 0.95rem;
    }}
    
    /* Sidebar personalizado */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
    }}
    
    section[data-testid="stSidebar"] * {{
        color: white !important;
    }}
    
    /* Radio buttons en sidebar */
    .stRadio > label {{
        color: white !important;
    }}
    
    /* Animaciones */
    @keyframes fadeIn {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.6s ease-out;
    }}
    
    /* Responsive - Tablets */
    @media (max-width: 1024px) {{
        .main-container {{
            padding: 1.5rem;
            margin: 0.5rem;
            border-radius: 16px;
        }}
        
        .main-title {{
            font-size: 2rem;
        }}
        
        .tech-grid {{
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        }}
        
        .header-container {{
            gap: 1rem;
        }}
        
        .logo-container {{
            width: 80px;
            height: 80px;
        }}
        
        .logo-container img {{
            width: 60px;
            height: 60px;
        }}
    }}
    
    /* Responsive - Móviles */
    @media (max-width: 768px) {{
        .main-container {{
            padding: 1rem;
            margin: 0.25rem;
            border-radius: 12px;
        }}
        
        .main-title {{
            font-size: 1.75rem;
            line-height: 1.2;
        }}
        
        .subtitle {{
            font-size: 0.95rem;
        }}
        
        .header-container {{
            flex-direction: column;
            text-align: center;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
        }}
        
        .logo-container {{
            width: 70px;
            height: 70px;
        }}
        
        .logo-container img {{
            width: 50px;
            height: 50px;
        }}
        
        .tech-grid {{
            grid-template-columns: 1fr;
            gap: 0.75rem;
        }}
        
        .tech-card {{
            padding: 1rem;
        }}
        
        .feature-card {{
            padding: 1rem;
            margin: 0.75rem 0;
        }}
        
        .feature-title {{
            font-size: 1.1rem;
        }}
        
        .feature-icon {{
            font-size: 1.5rem;
        }}
        
        .feature-text {{
            font-size: 0.9rem;
        }}
        
        .section-badge {{
            font-size: 0.8rem;
            padding: 0.4rem 1rem;
        }}
        
        .process-step {{
            margin-bottom: 1rem;
        }}
        
        .step-number {{
            width: 35px;
            height: 35px;
            font-size: 1rem;
        }}
        
        .step-title {{
            font-size: 1rem;
        }}
        
        .step-description {{
            font-size: 0.85rem;
        }}
        
        .demo-container {{
            padding: 1.5rem 1rem;
        }}
        
        .demo-container h1 {{
            font-size: 2rem !important;
        }}
        
        .demo-container p {{
            font-size: 0.95rem !important;
        }}
        
        .camera-preview {{
            padding: 1rem;
            margin: 1rem 0;
        }}
        
        .theme-toggle {{
            width: 45px;
            height: 45px;
            font-size: 1.3rem;
            top: 0.5rem;
            right: 0.5rem;
        }}
    }}
    
    /* Extra pequeño - Móviles pequeños */
    @media (max-width: 480px) {{
        .main-title {{
            font-size: 1.5rem;
        }}
        
        .subtitle {{
            font-size: 0.85rem;
        }}
        
        .feature-title {{
            font-size: 1rem;
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
        }}
        
        .tech-card {{
            padding: 0.75rem;
        }}
        
        .tech-icon {{
            font-size: 2rem;
        }}
        
        .tech-name {{
            font-size: 1rem;
        }}
        
        .tech-description {{
            font-size: 0.85rem;
        }}
    }}
    
    /* Mejorar contraste de inputs de Streamlit */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {{
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border-color: var(--border-color) !important;
    }}
    
    /* Botones de Streamlit */
    .stButton > button {{
        background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px var(--shadow-color);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 25px var(--shadow-color);
    }}
    
    /* Métricas de Streamlit */
    [data-testid="stMetricValue"] {{
        color: var(--text-primary) !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: var(--text-secondary) !important;
    }}
    
    /* Mensajes de éxito/error/info */
    .stSuccess, .stError, .stInfo, .stWarning {{
        background-color: var(--bg-secondary) !important;
        border-color: var(--border-color) !important;
    }}
    
    /* Camera input */
    [data-testid="stCameraInput"] {{
        background-color: var(--bg-secondary) !important;
    }}
</style>
""", unsafe_allow_html=True)

# Botón de tema flotante
col1, col2, col3 = st.columns([1, 6, 1])
with col3:
    if st.button("🌓" if st.session_state.dark_mode else "☀️", key="theme_toggle", help="Cambiar tema"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Sidebar mejorado
with st.sidebar:
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem 0 1rem;'>
        <div style='background: rgba(255, 255, 255, 0.2); border-radius: 50%; width: 80px; height: 80px; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>
            <div style='font-size: 2.5rem;'>🔐</div>
        </div>
        <h2 style='color: white; margin: 0; font-size: 1.5rem;'>Face2Pay</h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-top: 0.5rem;'>Pagos Biométricos Seguros</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "Navegación",
        ["🏠 Inicio", "⚙️ Funcionamiento", "🎬 Demo"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
    <div style='color: rgba(255,255,255,0.9); font-size: 0.8rem; text-align: center; padding: 0 0.5rem;'>
        <p style='margin-bottom: 0.5rem;'><strong>Innovation Banking Hack Fest 2025</strong></p>
        <p style='margin: 0;'>#IBHF25</p>
    </div>
    """, unsafe_allow_html=True)

# Página de Inicio
if page == "🏠 Inicio":
    st.markdown('<div class="main-container fade-in">', unsafe_allow_html=True)
    
    # Header con logo
    st.markdown("""
    <div class="header-container">
        <div class="logo-container">
            <div style='font-size: 3rem;'>🔐</div>
        </div>
        <div>
            <h1 class="main-title" style="color: var(--text-primary) !important; background: none !important; -webkit-text-fill-color: var(--text-primary) !important;">Face2Pay</h1>
            <p class="subtitle">El futuro de los pagos está en tu rostro</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sección de introducción
    st.markdown('<span class="section-badge">💡 NUESTRA VISIÓN</span>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
            <span class="feature-icon">🎯</span>
            <span>¿Qué es Face2Pay?</span>
        </div>
        <div class="feature-text">
            <p><strong>[RESUMEN EJECUTIVO - TODO: Insertar descripción de la propuesta de valor]</strong></p>
            <p>Face2Pay revoluciona la experiencia de pago mediante reconocimiento facial avanzado, 
            eliminando la necesidad de tarjetas físicas, dispositivos móviles o contraseñas complejas. 
            Nuestra solución combina seguridad de nivel bancario con la simplicidad de un gesto natural: tu rostro.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Características principales
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">
                <span class="feature-icon">⚡</span>
                <span>Velocidad</span>
            </div>
            <div class="feature-text">
                <p><strong>[TODO: Métricas de velocidad]</strong></p>
                <p>Pagos completados en menos de 2 segundos. Sin búsquedas de tarjetas, sin digitación de PINs largos.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">
                <span class="feature-icon">🔒</span>
                <span>Seguridad</span>
            </div>
            <div class="feature-text">
                <p><strong>[TODO: Certificaciones de seguridad]</strong></p>
                <p>Autenticación multifactor con validación PIN. Detección de vida y anti-spoofing de última generación.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">
                <span class="feature-icon">🌍</span>
                <span>Inclusión</span>
            </div>
            <div class="feature-text">
                <p><strong>[TODO: Estadísticas de accesibilidad]</strong></p>
                <p>Accesible para personas con movilidad reducida o dificultades para manejar efectivo o tarjetas.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Casos de uso
    st.markdown('<br><span class="section-badge">🚀 CASOS DE USO</span>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
            <span class="feature-icon">🏪</span>
            <span>Retail y Comercio</span>
        </div>
        <div class="feature-text">
            <p><strong>[TODO: Ejemplos de implementación en retail]</strong></p>
            <ul style='margin-left: 1.5rem;'>
                <li>Supermercados: Pago express sin sacar la cartera</li>
                <li>Tiendas de conveniencia: Checkout automático</li>
                <li>Restaurantes: Pago en mesa sin esperas</li>
            </ul>
        </div>
    </div>
    
    <div class="feature-card">
        <div class="feature-title">
            <span class="feature-icon">🏧</span>
            <span>Banca y Servicios Financieros</span>
        </div>
        <div class="feature-text">
            <p><strong>[TODO: Aplicaciones bancarias específicas]</strong></p>
            <ul style='margin-left: 1.5rem;'>
                <li>Cajeros automáticos sin tarjeta</li>
                <li>Autorización de transferencias de alto valor</li>
                <li>Acceso a sucursales y áreas VIP</li>
            </ul>
        </div>
    </div>
    
    <div class="feature-card">
        <div class="feature-title">
            <span class="feature-icon">🎟️</span>
            <span>Eventos y Transporte</span>
        </div>
        <div class="feature-text">
            <p><strong>[TODO: Casos de uso en movilidad]</strong></p>
            <ul style='margin-left: 1.5rem;'>
                <li>Acceso a eventos sin tickets físicos</li>
                <li>Pago en transporte público</li>
                <li>Compras en aeropuertos duty-free</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Página de Funcionamiento
elif page == "⚙️ Funcionamiento":
    st.markdown('<div class="main-container fade-in">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title" style="color: var(--text-primary) !important; background: none !important; -webkit-text-fill-color: var(--text-primary) !important;">¿Cómo Funciona?</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Proceso paso a paso
    st.markdown('<span class="section-badge">📋 PROCESO DE PAGO</span>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="process-timeline">
        <div class="process-step">
            <div class="step-number">1</div>
            <div class="step-content">
                <div class="step-title">Detección del Usuario</div>
                <div class="step-description">
                    <strong>[TODO: Detalles técnicos de detección]</strong><br>
                    La cámara detecta tu rostro y captura una imagen de alta calidad. 
                    El sistema verifica que eres una persona real mediante detección de vida (liveness detection).
                </div>
            </div>
        </div>
        
        <div class="process-step">
            <div class="step-number">2</div>
            <div class="step-content">
                <div class="step-title">Reconocimiento Biométrico</div>
                <div class="step-description">
                    <strong>[TODO: Algoritmos de reconocimiento utilizados]</strong><br>
                    Nuestro modelo de IA analiza más de 128 puntos faciales únicos y los compara 
                    con tu perfil biométrico encriptado almacenado de forma segura.
                </div>
            </div>
        </div>
        
        <div class="process-step">
            <div class="step-number">3</div>
            <div class="step-content">
                <div class="step-title">Verificación PIN</div>
                <div class="step-description">
                    <strong>[TODO: Proceso de verificación de seguridad]</strong><br>
                    Para garantizar máxima seguridad, se te solicita tu PIN personal de 4-6 dígitos 
                    antes de autorizar cualquier transacción.
                </div>
            </div>
        </div>
        
        <div class="process-step">
            <div class="step-number">4</div>
            <div class="step-content">
                <div class="step-title">Procesamiento de Pago</div>
                <div class="step-description">
                    <strong>[TODO: Integración con sistemas de pago]</strong><br>
                    Una vez autenticado, el pago se procesa instantáneamente a través de nuestro 
                    sistema seguro conectado con tu método de pago preferido.
                </div>
            </div>
        </div>
        
        <div class="process-step">
            <div class="step-number">5</div>
            <div class="step-content">
                <div class="step-title">Confirmación</div>
                <div class="step-description">
                    <strong>[TODO: Notificaciones y recibos]</strong><br>
                    Recibes confirmación instantánea en pantalla y en tu dispositivo móvil. 
                    Recibo digital enviado por email o SMS.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tecnologías utilizadas
    st.markdown('<br><span class="section-badge">🧠 TECNOLOGÍAS</span>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tech-grid">
        <div class="tech-card">
            <div class="tech-icon">🤖
                </div>
            <div class="tech-name">DeepFace / FaceNet</div>
            <div class="tech-description">
                <strong>[TODO: Versión y configuración específica]</strong><br>
                Reconocimiento facial con precisión del 99.65%
            </div>
        </div>
        
        <div class="tech-card">
            <div class="tech-icon">👁️</div>
            <div class="tech-name">Liveness Detection</div>
            <div class="tech-description">
                <strong>[TODO: Modelo anti-spoofing implementado]</strong><br>
                Prevención de fraude con fotos, videos o máscaras
            </div>
        </div>
        
        <div class="tech-card">
            <div class="tech-icon">🔐</div>
            <div class="tech-name">Encriptación AES-256</div>
            <div class="tech-description">
                <strong>[TODO: Arquitectura de seguridad]</strong><br>
                Datos biométricos encriptados end-to-end
            </div>
        </div>
        
        <div class="tech-card">
            <div class="tech-icon">☁️</div>
            <div class="tech-name">Cloud Infrastructure</div>
            <div class="tech-description">
                <strong>[TODO: Proveedor cloud y arquitectura]</strong><br>
                Escalabilidad y disponibilidad 99.99%
            </div>
        </div>
        
        <div class="tech-card">
            <div class="tech-icon">⚡</div>
            <div class="tech-name">Edge Computing</div>
            <div class="tech-description">
                <strong>[TODO: Procesamiento local implementado]</strong><br>
                Procesamiento en dispositivo para latencia mínima
            </div>
        </div>
        
        <div class="tech-card">
            <div class="tech-icon">🔄</div>
            <div class="tech-name">APIs Bancarias</div>
            <div class="tech-description">
                <strong>[TODO: Integraciones específicas]</strong><br>
                Integración con PSD2 y Open Banking
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Seguridad y privacidad
    st.markdown('<br><span class="section-badge">🛡️ SEGURIDAD & PRIVACIDAD</span>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
            <span class="feature-icon">📜</span>
            <span>Cumplimiento Normativo</span>
        </div>
        <div class="feature-text">
            <p><strong>[TODO: Certificaciones y compliance]</strong></p>
            <ul style='margin-left: 1.5rem;'>
                <li><strong>GDPR</strong>: Protección de datos personales</li>
                <li><strong>PSD2</strong>: Autenticación fuerte de cliente (SCA)</li>
                <li><strong>PCI DSS</strong>: Estándares de seguridad de la industria de pagos</li>
                <li><strong>ISO 27001</strong>: Gestión de seguridad de la información</li>
            </ul>
        </div>
    </div>
    
    <div class="feature-card">
        <div class="feature-title">
            <span class="feature-icon">🔒</span>
            <span>Protección de Datos Biométricos</span>
        </div>
        <div class="feature-text">
            <p><strong>[TODO: Arquitectura de almacenamiento seguro]</strong></p>
            <ul style='margin-left: 1.5rem;'>
                <li>Los datos biométricos nunca se almacenan como imágenes, solo como vectores encriptados</li>
                <li>Almacenamiento distribuido con redundancia geográfica</li>
                <li>Acceso mediante autenticación multifactor para administradores</li>
                <li>Auditorías de seguridad trimestrales por terceros certificados</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Paquetes y planes
    st.markdown('<br><span class="section-badge">💼 PAQUETES COMERCIALES</span>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">
                <span class="feature-icon">🌱</span>
                <span>Básico</span>
            </div>
            <div class="feature-text">
                <p><strong>[TODO: Precio y características]</strong></p>
                <ul style='margin-left: 1.5rem; font-size: 0.9rem;'>
                    <li>Hasta 1,000 transacciones/mes</li>
                    <li>1 punto de venta</li>
                    <li>Soporte por email</li>
                    <li>Dashboard básico</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="border-color: #667eea; border-width: 3px;">
            <div class="feature-title">
                <span class="feature-icon">🚀</span>
                <span>Profesional</span>
            </div>
            <div class="feature-text">
                <p><strong>[TODO: Precio y características]</strong></p>
                <ul style='margin-left: 1.5rem; font-size: 0.9rem;'>
                    <li>Hasta 10,000 transacciones/mes</li>
                    <li>Hasta 10 puntos de venta</li>
                    <li>Soporte prioritario 24/7</li>
                    <li>Analytics avanzado</li>
                    <li>API personalizada</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">
                <span class="feature-icon">👑</span>
                <span>Enterprise</span>
            </div>
            <div class="feature-text">
                <p><strong>[TODO: Precio y características]</strong></p>
                <ul style='margin-left: 1.5rem; font-size: 0.9rem;'>
                    <li>Transacciones ilimitadas</li>
                    <li>Puntos de venta ilimitados</li>
                    <li>Gerente de cuenta dedicado</li>
                    <li>Personalización total</li>
                    <li>SLA garantizado 99.99%</li>
                    <li>On-premise disponible</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Página de Demo
else:
    st.markdown('<div class="main-container fade-in">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="demo-container">
        <h1 style='font-size: 2.5rem; margin-bottom: 1rem; color: white;'>🎬 Demo en Vivo</h1>
        <p style='font-size: 1.2rem; opacity: 0.9; color: white;'>Experimenta el futuro de los pagos</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Instrucciones
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
            <span class="feature-icon">📱</span>
            <span>Instrucciones</span>
        </div>
        <div class="feature-text">
            <ol style='margin-left: 1.5rem; line-height: 1.8;'>
                <li>Haz clic en el botón "Iniciar Cámara" para activar tu webcam</li>
                <li>Colócate frente a la cámara con buena iluminación</li>
                <li>Captura tu imagen cuando estés listo</li>
                <li>El sistema procesará tu rostro y simulará el flujo de pago</li>
                <li>Introduce tu PIN para completar la transacción</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Demo interactiva
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📸 Captura Facial")
        
        # Captura de imagen
        camera_image = st.camera_input("Activa tu cámara", label_visibility="collapsed")
        
        if camera_image:
            st.success("✅ Imagen capturada correctamente")
            
            # TODO: Aquí iría el procesamiento de la imagen
            st.info("""
            **[TODO: PROCESAMIENTO DE IMAGEN]**
            
            Próximos pasos a implementar:
            1. Enviar imagen a API de reconocimiento facial
            2. Extraer embeddings faciales
            3. Comparar con base de datos de usuarios registrados
            4. Verificar liveness (detección de vida)
            5. Retornar resultado de autenticación
            
            **Endpoint propuesto:** `POST /api/v1/face-recognition`
            
            **Payload:**
```json
            {
                "image": "base64_encoded_image",
                "timestamp": "2025-10-15T10:30:00Z",
                "device_id": "unique_device_identifier"
            }
```
            """)
            
            with st.spinner("🔄 Procesando imagen facial..."):
                import time
                time.sleep(2)  # Simular procesamiento
                
                st.success("✅ Rostro detectado y verificado")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Confianza", "98.7%", "↑ 2.3%")
                with col_b:
                    st.metric("Liveness", "✅ Real", "")
                with col_c:
                    st.metric("Tiempo", "1.2s", "")
    
    with col2:
        st.markdown("### 💳 Detalles de Transacción")
        
        # Simulación de transacción
        amount = st.number_input("💰 Monto a pagar (€)", min_value=0.01, value=25.50, step=0.01)
        merchant = st.selectbox("🏪 Comercio", 
                                ["Supermercado Central", "Café Moderno", "Tech Store", "Restaurante Gourmet"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # PIN Input
        pin = st.text_input("🔐 Introduce tu PIN", type="password", max_chars=6, placeholder="****")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✅ Confirmar Pago", use_container_width=True, type="primary"):
            if camera_image and pin:
                with st.spinner("🔄 Procesando pago..."):
                    import time
                    time.sleep(2)
                
                st.success("✅ ¡Pago completado con éxito!")
                st.balloons()
                
                # Resumen de transacción
                st.markdown("""
                <div class="feature-card" style="margin-top: 1rem;">
                    <div class="feature-title">
                        <span class="feature-icon">✅</span>
                        <span>Resumen</span>
                    </div>
                    <div class="feature-text">
                        <p><strong>Monto:</strong> {:.2f} €</p>
                        <p><strong>Comercio:</strong> {}</p>
                        <p><strong>Fecha:</strong> 15/10/2025 10:30</p>
                        <p><strong>ID Transacción:</strong> F2P-2025-10-15-001234</p>
                        <p><strong>Método:</strong> Face2Pay Biométrico</p>
                    </div>
                </div>
                """.format(amount, merchant), unsafe_allow_html=True)
            else:
                st.error("⚠️ Por favor, captura tu imagen y introduce tu PIN")
    
    # Estadísticas de la demo
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<span class="section-badge">📊 MÉTRICAS DE RENDIMIENTO</span>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="tech-card">
            <div class="tech-icon">⚡</div>
            <div class="tech-name">1.8s</div>
            <div class="tech-description">Tiempo promedio de transacción</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tech-card">
            <div class="tech-icon">🎯</div>
            <div class="tech-name">99.2%</div>
            <div class="tech-description">Tasa de éxito en reconocimiento</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="tech-card">
            <div class="tech-icon">🛡️</div>
            <div class="tech-name">0.001%</div>
            <div class="tech-description">Tasa de falsos positivos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="tech-card">
            <div class="tech-icon">😊</div>
            <div class="tech-name">4.8/5</div>
            <div class="tech-description">Satisfacción del usuario</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Ventajas competitivas
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<span class="section-badge">🏆 VENTAJAS COMPETITIVAS</span>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">
                <span class="feature-icon">⚡</span>
                <span>vs. Tarjeta de Crédito</span>
            </div>
            <div class="feature-text">
                <ul style='margin-left: 1.5rem;'>
                    <li><strong>60% más rápido</strong> - Sin buscar tarjeta ni introducir PIN en TPV</li>
                    <li><strong>0% fraude físico</strong> - No se puede perder, robar o clonar</li>
                    <li><strong>100% higiénico</strong> - Sin contacto con superficies compartidas</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">
                <span class="feature-icon">📱</span>
                <span>vs. Pago Móvil</span>
            </div>
            <div class="feature-text">
                <ul style='margin-left: 1.5rem;'>
                    <li><strong>Sin batería</strong> - Funciona aunque tu móvil esté apagado</li>
                    <li><strong>Sin apps</strong> - No necesitas descargar ni actualizar nada</li>
                    <li><strong>Universal</strong> - Un solo sistema para todos los comercios</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Roadmap futuro
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<span class="section-badge">🗺️ ROADMAP</span>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
            <span class="feature-icon">🚀</span>
            <span>Próximas Funcionalidades</span>
        </div>
        <div class="feature-text">
            <p><strong>[TODO: Timeline detallado de desarrollo]</strong></p>
            <div class="process-timeline" style="padding: 1rem 0;">
                <div class="process-step">
                    <div class="step-number" style="width: 35px; height: 35px; font-size: 0.9rem;">Q1</div>
                    <div class="step-content">
                        <div class="step-title" style="font-size: 1rem;">Integración con Bizum</div>
                        <div class="step-description" style="font-size: 0.9rem;">
                            Permitir pagos P2P y divisiones de cuenta mediante reconocimiento facial
                        </div>
                    </div>
                </div>
                
                <div class="process-step">
                    <div class="step-number" style="width: 35px; height: 35px; font-size: 0.9rem;">Q2</div>
                    <div class="step-content">
                        <div class="step-title" style="font-size: 1rem;">Modo Offline</div>
                        <div class="step-description" style="font-size: 0.9rem;">
                            Procesamiento local con sincronización posterior para zonas sin conectividad
                        </div>
                    </div>
                </div>
                
                <div class="process-step">
                    <div class="step-number" style="width: 35px; height: 35px; font-size: 0.9rem;">Q3</div>
                    <div class="step-content">
                        <div class="step-title" style="font-size: 1rem;">Reconocimiento Multi-usuario</div>
                        <div class="step-description" style="font-size: 0.9rem;">
                            Pagos grupales con división automática entre varios usuarios detectados
                        </div>
                    </div>
                </div>
                
                <div class="process-step">
                    <div class="step-number" style="width: 35px; height: 35px; font-size: 0.9rem;">Q4</div>
                    <div class="step-content">
                        <div class="step-title" style="font-size: 1rem;">IA Predictiva</div>
                        <div class="step-description" style="font-size: 0.9rem;">
                            Sugerencias inteligentes basadas en patrones de compra y ubicación
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Testimonios simulados
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<span class="section-badge">💬 TESTIMONIOS</span>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="tech-card">
            <div class="tech-icon">👨‍💼</div>
            <div class="tech-name">Carlos M.</div>
            <div class="tech-description" style="font-style: italic;">
                "Como gerente de tienda, Face2Pay ha reducido nuestras colas en un 40%. 
                Los clientes están encantados con la rapidez."
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="tech-card">
            <div class="tech-icon">👩‍🦽</div>
            <div class="tech-name">Ana L.</div>
            <div class="tech-description" style="font-style: italic;">
                "Tengo movilidad reducida y esta tecnología me ha cambiado la vida. 
                Ya no necesito ayuda para buscar mi tarjeta o contar efectivo."
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="tech-card">
            <div class="tech-icon">👨‍💻</div>
            <div class="tech-name">Miguel R.</div>
            <div class="tech-description" style="font-style: italic;">
                "La integración fue sorprendentemente sencilla. 
                En dos semanas teníamos el sistema operativo en todas nuestras sucursales."
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="demo-container">
        <h2 style='margin-bottom: 1rem; color: white;'>¿Interesado en Face2Pay?</h2>
        <p style='font-size: 1.05rem; opacity: 0.9; margin-bottom: 2rem; color: white;'>
            Contáctanos para una demo personalizada o para implementar Face2Pay en tu negocio
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("📧 Contactar", "mailto:info@face2pay.com", use_container_width=True)
    with col2:
        st.link_button("📄 Descargar Dossier", "#", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style='text-align: center; padding: 3rem 1rem 1rem; color: {'rgba(255,255,255,0.7)' if st.session_state.dark_mode else 'rgba(15,23,42,0.6)'}; margin-top: 2rem;'>
    <p style='font-size: 0.9rem;'>
        <strong>Face2Pay</strong> - Innovation Banking Hack Fest 2025 (#IBHF25)
    </p>
    <p style='font-size: 0.85rem; margin-top: 0.5rem;'>
        🏦 Banco Sabadell CCTA | 🎓 Universidad de Alicante | 🚀 Powered by AI
    </p>
    <p style='font-size: 0.8rem; margin-top: 1rem; opacity: 0.6;'>
        © 2025 Face2Pay. Todos los derechos reservados. | 
        <a href='#' style='color: inherit; text-decoration: none;'>Privacidad</a> | 
        <a href='#' style='color: inherit; text-decoration: none;'>Términos</a>
    </p>
</div>
""", unsafe_allow_html=True)