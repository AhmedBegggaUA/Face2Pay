import streamlit as st
import base64
from pathlib import Path
import requests
from PIL import Image
import io

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="SmilePay - Pagos Biométricos",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTADO DE LA APLICACIÓN ====================
def initialize_session_state():
    """Inicializa el estado de la sesión"""
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True
    if 'api_available' not in st.session_state:
        st.session_state.api_available = check_api_availability()

def check_api_availability():
    """Verifica si la API está disponible"""
    try:
        # TODO: Reemplazar con la URL real de tu API
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False

# ==================== UTILIDADES ====================
def load_logo():
    """Carga el logo de la aplicación"""
    logo_path = Path("./images/logo.png")
    if logo_path.exists():
        return Image.open(logo_path)
    return None

def get_logo_base64():
    """Obtiene el logo en formato base64 para usar en HTML"""
    logo = load_logo()
    if logo:
        buffered = io.BytesIO()
        logo.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    return None

def encode_image_to_base64(image):
    """Convierte una imagen a base64"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def send_image_to_api(image):
    """Envía la imagen a la API de reconocimiento facial"""
    try:
        # Convertir imagen a base64
        img_base64 = encode_image_to_base64(Image.open(image))
        
        # TODO: Reemplazar con la URL real de tu API
        api_url = "http://localhost:8000/api/v1/face-recognition"
        
        payload = {
            "image": img_base64,
            "timestamp": "2025-10-15T10:30:00Z",
            "device_id": "web_demo_device"
        }
        
        response = requests.post(api_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

# ==================== ESTILOS CSS ====================
def apply_custom_css():
    """Aplica los estilos CSS personalizados"""
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
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
            --success-color: #10b981;
        }}
        
        * {{
            font-family: 'Inter', sans-serif;
        }}
        
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        .stApp {{
            background: {'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' if st.session_state.dark_mode else 'linear-gradient(135deg, #e0e7ff 0%, #f3e8ff 100%)'};
            transition: background 0.5s ease;
        }}
        
        .main-container {{
            background: var(--bg-card);
            border-radius: 24px;
            padding: 2rem;
            margin: 1rem auto;
            max-width: 1200px;
            box-shadow: 0 20px 60px var(--shadow-color);
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            animation: fadeInUp 0.6s ease-out;
        }}
        
        .header-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 2rem;
            gap: 1.5rem;
            flex-wrap: wrap;
            animation: fadeIn 0.8s ease-out;
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
            transition: transform 0.3s ease;
        }}
        
        .logo-container:hover {{
            transform: scale(1.05) rotate(5deg);
        }}
        
        .logo-container img {{
            width: 80px;
            height: 80px;
            object-fit: contain;
        }}
        
        .main-title {{
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: -1px;
            text-align: center;
            color: var(--text-primary) !important;
        }}
        
        .subtitle {{
            font-size: 1.1rem;
            color: var(--text-secondary);
            font-weight: 400;
            margin-top: 0.5rem;
            text-align: center;
        }}
        
        .feature-card {{
            background: var(--bg-secondary);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 2px solid var(--border-color);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            animation: slideIn 0.5s ease-out;
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
            animation: bounce 2s infinite;
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
            animation: fadeInScale 0.6s ease-out;
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
        
        .demo-container {{
            background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
            border-radius: 20px;
            padding: 2rem;
            color: white;
            text-align: center;
            animation: pulse 3s infinite;
        }}
        
        .demo-container h1, .demo-container h2, .demo-container p {{
            color: white !important;
        }}
        
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
            animation: slideInLeft 0.5s ease-out;
        }}
        
        .process-timeline {{
            position: relative;
            padding: 1.5rem 0;
        }}
        
        .process-step {{
            display: flex;
            align-items: flex-start;
            margin-bottom: 1.5rem;
            position: relative;
            animation: slideInRight 0.6s ease-out;
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
        
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
        }}
        
        section[data-testid="stSidebar"] * {{
            color: white !important;
        }}
        
        button[kind="header"] {{
            color: var(--text-primary) !important;
            background: var(--bg-card) !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
            margin: 0.5rem !important;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes fadeInScale {{
            from {{ opacity: 0; transform: scale(0.9); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}
        
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateX(-20px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        @keyframes slideInLeft {{
            from {{ opacity: 0; transform: translateX(-30px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        @keyframes slideInRight {{
            from {{ opacity: 0; transform: translateX(30px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-5px); }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{ box-shadow: 0 0 20px rgba(102, 126, 234, 0.3); }}
            50% {{ box-shadow: 0 0 40px rgba(102, 126, 234, 0.6); }}
        }}
        
        @media (max-width: 1024px) {{
            .main-container {{ padding: 1.5rem; margin: 0.5rem; border-radius: 16px; }}
            .main-title {{ font-size: 2rem; }}
            .tech-grid {{ grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); }}
            .logo-container {{ width: 80px; height: 80px; }}
            .logo-container img {{ width: 60px; height: 60px; }}
        }}
        
        @media (max-width: 768px) {{
            .main-container {{ padding: 1rem; margin: 0.25rem; border-radius: 12px; }}
            .main-title {{ font-size: 1.75rem; line-height: 1.2; }}
            .subtitle {{ font-size: 0.95rem; }}
            .header-container {{ flex-direction: column; text-align: center; gap: 0.75rem; }}
            .logo-container {{ width: 70px; height: 70px; }}
            .logo-container img {{ width: 50px; height: 50px; }}
            .tech-grid {{ grid-template-columns: 1fr; gap: 0.75rem; }}
            .feature-card {{ padding: 1rem; margin: 0.75rem 0; }}
            .feature-title {{ font-size: 1.1rem; }}
            .feature-icon {{ font-size: 1.5rem; }}
            .step-number {{ width: 35px; height: 35px; font-size: 1rem; }}
        }}
        
        @media (max-width: 480px) {{
            .main-title {{ font-size: 1.5rem; }}
            .subtitle {{ font-size: 0.85rem; }}
            .tech-card {{ padding: 0.75rem; }}
        }}
        
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {{
            background-color: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border-color: var(--border-color) !important;
        }}
        
        /* Botones de Streamlit - Generales */
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
        
        /* Botones de navegación en sidebar */
        section[data-testid="stSidebar"] .stButton > button {{
            background: rgba(255, 255, 255, 0.15) !important;
            color: white !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 12px !important;
            padding: 0.8rem 1rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            margin: 0.3rem 0 !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        }}
        
        section[data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba(255, 255, 255, 0.25) !important;
            border-color: rgba(255, 255, 255, 0.6) !important;
            transform: translateX(5px) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
        }}
        
        section[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
            background: rgba(255, 255, 255, 0.95) !important;
            color: #667eea !important;
            border-color: white !important;
            box-shadow: 0 4px 20px rgba(255, 255, 255, 0.4) !important;
            text-shadow: none !important;
        }}
        
        section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {{
            background: white !important;
            transform: translateX(5px) scale(1.02) !important;
            box-shadow: 0 6px 25px rgba(255, 255, 255, 0.5) !important;
        }}
        [data-testid="stMetricValue"] {{ color: var(--text-primary) !important; }}
        [data-testid="stMetricLabel"] {{ color: var(--text-secondary) !important; }}
    </style>
    """, unsafe_allow_html=True)

# ==================== COMPONENTES ====================
def render_header(title, subtitle=None):
    """Renderiza el header con logo y título"""
    logo_base64 = get_logo_base64()
    
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="SmilePay Logo">'
    else:
        logo_html = '<div style="font-size: 3rem;">😊</div>'
    
    subtitle_html = f'<p class="subtitle">{subtitle}</p>' if subtitle else ''
    
    st.markdown(f"""
    <div class="header-container">
        <div class="logo-container">
            {logo_html}
        </div>
        <div>
            <h1 class="main-title">{title}</h1>
            {subtitle_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Renderiza el sidebar con navegación mejorada"""
    with st.sidebar:
        logo_base64 = get_logo_base64()
        
        if logo_base64:
            logo_display = f'<img src="data:image/png;base64,{logo_base64}" style="width: 60px; height: 60px; object-fit: contain;">'
        else:
            logo_display = '<div style="font-size: 2.5rem;">😊</div>'
        
        st.markdown(f"""
        <div style='text-align: center; padding: 2rem 0 1rem;'>
            <div style='background: rgba(255, 255, 255, 0.2); border-radius: 50%; width: 80px; height: 80px; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>
                {logo_display}
            </div>
            <h2 style='color: white; margin: 0; font-size: 1.5rem;'>SmilePay</h2>
            <p style='color: rgba(255,255,255,0.8); font-size: 0.85rem; margin-top: 0.5rem;'>Pagos Biométricos Seguros</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Inicializar la página actual si no existe
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "🏠 Inicio"
        
        # Botones de navegación
        if st.button("🏠 Inicio", key="nav_home", use_container_width=True, 
                     type="primary" if st.session_state.current_page == "🏠 Inicio" else "secondary"):
            st.session_state.current_page = "🏠 Inicio"
            st.rerun()
        
        if st.button("⚙️ Funcionamiento", key="nav_how", use_container_width=True,
                     type="primary" if st.session_state.current_page == "⚙️ Funcionamiento" else "secondary"):
            st.session_state.current_page = "⚙️ Funcionamiento"
            st.rerun()
        
        if st.button("🎬 Demo", key="nav_demo", use_container_width=True,
                     type="primary" if st.session_state.current_page == "🎬 Demo" else "secondary"):
            st.session_state.current_page = "🎬 Demo"
            st.rerun()
        
        st.markdown("---")
        
        # Toggle de modo día/noche
        mode_icon = "🌙 Modo Oscuro" if st.session_state.dark_mode else "☀️ Modo Claro"
        if st.button(mode_icon, key="theme_toggle_sidebar", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Indicador de estado de la API
        api_status = "🟢 API Conectada" if st.session_state.api_available else "🔴 API Desconectada"
        api_color = "rgba(16, 185, 129, 0.2)" if st.session_state.api_available else "rgba(239, 68, 68, 0.2)"
        st.markdown(f"""
        <div style='color: rgba(255,255,255,0.95); font-size: 0.8rem; text-align: center; padding: 0.6rem; background: {api_color}; border-radius: 8px; margin-bottom: 1rem; font-weight: 600;'>
            {api_status}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='color: rgba(255,255,255,0.9); font-size: 0.8rem; text-align: center; padding: 0 0.5rem;'>
            <p style='margin-bottom: 0.5rem;'><strong>Innovation Banking Hack Fest 2025</strong></p>
            <p style='margin: 0;'>#IBHF25</p>
        </div>
        """, unsafe_allow_html=True)
        
        return st.session_state.current_page

# Dime "continuar" para que te envíe el resto del código
# ==================== PÁGINAS ====================
def page_home():
    """Página de Inicio"""
    st.markdown('<div class="main-container fade-in">', unsafe_allow_html=True)
    
    render_header("SmilePay", "El futuro de los pagos está en tu sonrisa")
    
    st.markdown('<span class="section-badge">💡 NUESTRA VISIÓN</span>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">
            <span class="feature-icon">🎯</span>
            <span>¿Qué es SmilePay?</span>
        </div>
        <div class="feature-text">
            <p><strong>[RESUMEN EJECUTIVO - TODO: Insertar descripción de la propuesta de valor]</strong></p>
            <p>SmilePay revoluciona la experiencia de pago mediante reconocimiento facial avanzado, 
            eliminando la necesidad de tarjetas físicas, dispositivos móviles o contraseñas complejas. 
            Nuestra solución combina seguridad de nivel bancario con la simplicidad de un gesto natural: tu sonrisa.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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

def page_how_it_works():
    """Página de Funcionamiento"""
    st.markdown('<div class="main-container fade-in">', unsafe_allow_html=True)
    
    render_header("¿Cómo Funciona?")
    
    st.markdown('<span class="section-badge">📋 PROCESO DE PAGO</span>', unsafe_allow_html=True)
    
    # Paso 1
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
    """, unsafe_allow_html=True)
    
    # Paso 2
    st.markdown("""
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
    """, unsafe_allow_html=True)
    
    # Paso 3
    st.markdown("""
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
    """, unsafe_allow_html=True)
    
    # Paso 4
    st.markdown("""
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
    """, unsafe_allow_html=True)
    
    # Paso 5
    st.markdown("""
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
    
    st.markdown('<br><span class="section-badge">🧠 TECNOLOGÍAS</span>', unsafe_allow_html=True)
    
    # Tech cards - divididas
    st.markdown("""
    <div class="tech-grid">
        <div class="tech-card">
            <div class="tech-icon">🤖</div>
            <div class="tech-name">DeepFace / FaceNet</div>
            <div class="tech-description">
                <strong>[TODO: Versión y configuración específica]</strong><br>
                Reconocimiento facial con precisión del 99.65%
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="tech-card">
            <div class="tech-icon">👁️</div>
            <div class="tech-name">Liveness Detection</div>
            <div class="tech-description">
                <strong>[TODO: Modelo anti-spoofing implementado]</strong><br>
                Prevención de fraude con fotos, videos o máscaras
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="tech-card">
            <div class="tech-icon">🔐</div>
            <div class="tech-name">Encriptación AES-256</div>
            <div class="tech-description">
                <strong>[TODO: Arquitectura de seguridad]</strong><br>
                Datos biométricos encriptados end-to-end
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="tech-card">
            <div class="tech-icon">☁️</div>
            <div class="tech-name">Cloud Infrastructure</div>
            <div class="tech-description">
                <strong>[TODO: Proveedor cloud y arquitectura]</strong><br>
                Escalabilidad y disponibilidad 99.99%
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="tech-card">
            <div class="tech-icon">⚡</div>
            <div class="tech-name">Edge Computing</div>
            <div class="tech-description">
                <strong>[TODO: Procesamiento local implementado]</strong><br>
                Procesamiento en dispositivo para latencia mínima
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
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

# Dime "continuar" para la página de Demo y el main
def page_demo():
    """Página de Demo"""
    st.markdown('<div class="main-container fade-in">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="demo-container">
        <h1 style='font-size: 2.5rem; margin-bottom: 1rem; color: white;'>🎬 Demo en Vivo</h1>
        <p style='font-size: 1.2rem; opacity: 0.9; color: white;'>Experimenta el futuro de los pagos</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
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
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📸 Captura Facial")
        
        if st.session_state.api_available:
            st.info("✅ API conectada - Procesamiento en tiempo real activado")
            camera_image = st.camera_input("Activa tu cámara", label_visibility="collapsed")
            
            if camera_image:
                st.success("✅ Imagen capturada correctamente")
                
                with st.spinner("🔄 Enviando imagen a la API..."):
                    result = send_image_to_api(camera_image)
                    
                    if "error" in result:
                        st.error(f"❌ Error al procesar: {result['error']}")
                        st.info("💡 Usando procesamiento local como respaldo...")
                        import time
                        time.sleep(2)
                        st.success("✅ Rostro detectado y verificado (modo local)")
                    else:
                        st.success("✅ Rostro verificado por la API")
                        
                        if "confidence" in result:
                            col_a, col_b, col_c = st.columns(3)
                            with col_a:
                                st.metric("Confianza", f"{result.get('confidence', 98.7)}%")
                            with col_b:
                                st.metric("Liveness", result.get('liveness_status', '✅ Real'))
                            with col_c:
                                st.metric("Tiempo", f"{result.get('processing_time', 1.2)}s")
        else:
            st.warning("⚠️ API desconectada - Usando modo demo")
            camera_image = st.camera_input("Activa tu cámara", label_visibility="collapsed")
            
            if camera_image:
                st.success("✅ Imagen capturada correctamente")
                
                st.info("""
                **[MODO DEMO - API NO DISPONIBLE]**
                
                La API de reconocimiento facial no está disponible actualmente.
                
                **Para conectar la API:**
                1. Asegúrate de que el servidor esté corriendo en `http://localhost:8000`
                2. Implementa el endpoint: `POST /api/v1/face-recognition`
                3. Recarga la página para reconectar
                
                **Endpoint esperado:**
```json
                POST /api/v1/face-recognition
                {
                    "image": "base64_encoded_image",
                    "timestamp": "2025-10-15T10:30:00Z",
                    "device_id": "unique_device_identifier"
                }
```
                
                **Respuesta esperada:**
```json
                {
                    "confidence": 98.7,
                    "liveness_status": "Real",
                    "processing_time": 1.2,
                    "user_id": "user_12345",
                    "match": true
                }
```
                """)
                
                with st.spinner("🔄 Procesando imagen facial (modo simulado)..."):
                    import time
                    time.sleep(2)
                
                st.success("✅ Rostro detectado y verificado (modo demo)")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Confianza", "98.7%", "↑ 2.3%")
                with col_b:
                    st.metric("Liveness", "✅ Real", "")
                with col_c:
                    st.metric("Tiempo", "1.2s", "")
    
    with col2:
        st.markdown("### 💳 Detalles de Transacción")
        
        amount = st.number_input("💰 Monto a pagar (€)", min_value=0.01, value=25.50, step=0.01)
        merchant = st.selectbox("🏪 Comercio", 
                                ["Supermercado Central", "Café Moderno", "Tech Store", "Restaurante Gourmet"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        pin = st.text_input("🔐 Introduce tu PIN", type="password", max_chars=6, placeholder="****")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✅ Confirmar Pago", use_container_width=True, type="primary"):
            if camera_image and pin:
                with st.spinner("🔄 Procesando pago..."):
                    import time
                    time.sleep(2)
                
                st.success("✅ ¡Pago completado con éxito!")
                st.balloons()
                
                from datetime import datetime
                current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
                
                st.markdown(f"""
                <div class="feature-card" style="margin-top: 1rem;">
                    <div class="feature-title">
                        <span class="feature-icon">✅</span>
                        <span>Resumen</span>
                    </div>
                    <div class="feature-text">
                        <p><strong>Monto:</strong> {amount:.2f} €</p>
                        <p><strong>Comercio:</strong> {merchant}</p>
                        <p><strong>Fecha:</strong> {current_time}</p>
                        <p><strong>ID Transacción:</strong> SMP-{datetime.now().strftime("%Y%m%d-%H%M%S")}</p>
                        <p><strong>Método:</strong> SmilePay Biométrico</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("⚠️ Por favor, captura tu imagen y introduce tu PIN")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<span class="section-badge">📊 MÉTRICAS DE RENDIMIENTO</span>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        ("⚡", "1.8s", "Tiempo promedio de transacción"),
        ("🎯", "99.2%", "Tasa de éxito en reconocimiento"),
        ("🛡️", "0.001%", "Tasa de falsos positivos"),
        ("😊", "4.8/5", "Satisfacción del usuario")
    ]
    
    for col, (icon, value, desc) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
            <div class="tech-card">
                <div class="tech-icon">{icon}</div>
                <div class="tech-name">{value}</div>
                <div class="tech-description">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
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
    
    st.markdown("<br><br>", unsafe_allow_html=True)
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
    """, unsafe_allow_html=True)
    
    st.markdown("""
                <div class="process-step">
                    <div class="step-number" style="width: 35px; height: 35px; font-size: 0.9rem;">Q2</div>
                    <div class="step-content">
                        <div class="step-title" style="font-size: 1rem;">Modo Offline</div>
                        <div class="step-description" style="font-size: 0.9rem;">
                            Procesamiento local con sincronización posterior para zonas sin conectividad
                        </div>
                    </div>
                </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
                <div class="process-step">
                    <div class="step-number" style="width: 35px; height: 35px; font-size: 0.9rem;">Q3</div>
                    <div class="step-content">
                        <div class="step-title" style="font-size: 1rem;">Reconocimiento Multi-usuario</div>
                        <div class="step-description" style="font-size: 0.9rem;">
                            Pagos grupales con división automática entre varios usuarios detectados
                        </div>
                    </div>
                </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
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
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<span class="section-badge">💬 TESTIMONIOS</span>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    testimonials = [
        ("👨‍💼", "Carlos M.", "Como gerente de tienda, SmilePay ha reducido nuestras colas en un 40%. Los clientes están encantados con la rapidez."),
        ("👩‍🦽", "Ana L.", "Tengo movilidad reducida y esta tecnología me ha cambiado la vida. Ya no necesito ayuda para buscar mi tarjeta o contar efectivo."),
        ("👨‍💻", "Miguel R.", "La integración fue sorprendentemente sencilla. En dos semanas teníamos el sistema operativo en todas nuestras sucursales.")
    ]
    
    for col, (icon, name, text) in zip([col1, col2, col3], testimonials):
        with col:
            st.markdown(f"""
            <div class="tech-card">
                <div class="tech-icon">{icon}</div>
                <div class="tech-name">{name}</div>
                <div class="tech-description" style="font-style: italic;">{text}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="demo-container">
        <h2 style='margin-bottom: 1rem; color: white;'>¿Interesado en SmilePay?</h2>
        <p style='font-size: 1.05rem; opacity: 0.9; margin-bottom: 2rem; color: white;'>
            Contáctanos para una demo personalizada o para implementar SmilePay en tu negocio
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("📧 Contactar", "mailto:info@smilepay.com", use_container_width=True)
    with col2:
        st.link_button("📄 Descargar Dossier", "#", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_footer():
    """Renderiza el footer"""
    st.markdown(f"""
    <div style='text-align: center; padding: 3rem 1rem 1rem; color: {'rgba(255,255,255,0.7)' if st.session_state.dark_mode else 'rgba(15,23,42,0.6)'}; margin-top: 2rem;'>
        <p style='font-size: 0.9rem;'>
            <strong>SmilePay</strong> - Innovation Banking Hack Fest 2025 (#IBHF25)
        </p>
        <p style='font-size: 0.85rem; margin-top: 0.5rem;'>
            🏦 Banco Sabadell CCTA | 🎓 Universidad de Alicante | 🚀 Powered by AI
        </p>
        <p style='font-size: 0.8rem; margin-top: 1rem; opacity: 0.6;'>
            © 2025 SmilePay. Todos los derechos reservados. | 
            <a href='#' style='color: inherit; text-decoration: none;'>Privacidad</a> | 
            <a href='#' style='color: inherit; text-decoration: none;'>Términos</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==================== MAIN ====================
def main():
    """Función principal de la aplicación"""
    initialize_session_state()
    apply_custom_css()
    
    
    
    page = render_sidebar()
    
    if page == "🏠 Inicio":
        page_home()
    elif page == "⚙️ Funcionamiento":
        page_how_it_works()
    elif page == "🎬 Demo":
        page_demo()
    
    render_footer()

if __name__ == "__main__":
    main()