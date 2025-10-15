# Face2Pay - Documentación Técnica

## 📐 Arquitectura de la Aplicación

### Componentes Principales

La aplicación Face2Pay está construida sobre los siguientes componentes:

#### 1. **Interfaz de Usuario (app.py)**
- Framework: Streamlit
- Lenguaje: Python
- Estilo: CSS personalizado embebido

#### 2. **Sistema de Gestión de Estado**
Utiliza `st.session_state` para mantener:
- Base de datos de usuarios simulada
- Usuario actual autenticado
- Paso actual del proceso (1-3)
- Historial de transacciones

#### 3. **Módulos Funcionales**

##### Reconocimiento Facial
```python
def detectar_rostro(imagen):
    """
    Detecta y codifica rostros en una imagen.
    
    En modo producción:
    - Captura imagen de cámara
    - Detecta ubicación del rostro
    - Genera encoding facial
    - Compara con base de datos
    
    En modo demo:
    - Simulación mediante selección de usuario
    """
```

##### Verificación de PIN
```python
def verificar_pin(pin_ingresado):
    """
    Valida el PIN de 4 dígitos del usuario.
    
    Seguridad:
    - Input tipo password (oculto)
    - Máximo 4 caracteres
    - Comparación exacta
    """
```

##### Procesamiento de Transacciones
```python
def realizar_transaccion(monto):
    """
    Procesa un pago y actualiza el saldo.
    
    Validaciones:
    - Verificación de saldo suficiente
    - Actualización de saldo
    - Registro en historial
    - Timestamp de operación
    """
```

## 🎨 Diseño de la Interfaz

### Tema de Colores
- **Color Principal**: `#1E88E5` (Azul Material)
- **Fondo**: `#FFFFFF` (Blanco)
- **Fondo Secundario**: `#F5F5F5` (Gris claro)
- **Texto**: `#262730` (Negro suave)

### Paleta de Estados
- **Info**: `#E3F2FD` (Azul claro)
- **Éxito**: `#C8E6C9` (Verde claro)
- **Error**: `#FFCDD2` (Rojo claro)

### Estructura de Páginas

```
┌─────────────────────────────────────┐
│   Header (Título + Subtítulo)      │
├─────────────┬───────────────────────┤
│             │                       │
│  Sidebar    │   Contenido Principal│
│             │                       │
│  - Info     │   Paso 1: Facial     │
│  - Proceso  │   Paso 2: PIN        │
│  - Usuarios │   Paso 3: Pago       │
│  - Reiniciar│                       │
│             │   Historial           │
└─────────────┴───────────────────────┘
│           Footer                    │
└─────────────────────────────────────┘
```

## 🔄 Flujo de Trabajo

```
[Inicio]
   │
   ▼
[Paso 1: Reconocimiento Facial]
   │ (Usuario seleccionado/reconocido)
   ▼
[Paso 2: Verificación PIN]
   │ (PIN correcto)
   ▼
[Paso 3: Transacción]
   │ (Monto ingresado + confirmación)
   ▼
[Procesamiento]
   │
   ├─► [Saldo suficiente] ──► [Éxito] ──► [Reinicio]
   │
   └─► [Saldo insuficiente] ──► [Error] ──► [Retry]
```

## 💾 Estructura de Datos

### Usuario
```python
{
    'nombre': str,        # Nombre completo
    'pin': str,          # PIN de 4 dígitos
    'saldo': float,      # Saldo disponible
    'encoding': array    # Encoding facial (face_recognition)
}
```

### Transacción
```python
{
    'fecha': str,            # ISO 8601 timestamp
    'usuario': str,          # Nombre del usuario
    'monto': float,          # Cantidad pagada
    'saldo_restante': float  # Saldo después del pago
}
```

## 🔒 Consideraciones de Seguridad

### Implementación Actual (Demo)
- ✅ PIN oculto en input (tipo password)
- ✅ Validación de saldo antes de transacción
- ✅ Registro de todas las transacciones
- ⚠️ Usuarios y PINs hardcodeados (solo demo)
- ⚠️ Sin encriptación (solo demo)

### Recomendaciones para Producción
- 🔐 Encriptación de PINs (bcrypt/argon2)
- 🔐 HTTPS obligatorio
- 🔐 Tokens de sesión temporales
- 🔐 Rate limiting en intentos de PIN
- 🔐 2FA adicional
- 🔐 Base de datos segura (PostgreSQL + encriptación)
- 🔐 Logs de auditoría
- 🔐 Certificación PCI DSS para datos de pago

## 📊 Métricas y Monitoreo

### Datos Rastreados
- Total de transacciones realizadas
- Monto total procesado
- Usuarios activos
- Tiempo promedio por transacción
- Tasa de éxito/fallo

### Historial
- Últimas 5 transacciones visibles en UI
- Todas las transacciones en session_state
- En producción: almacenar en base de datos

## 🚀 Escalabilidad

### Limitaciones Actuales
- Session state local (no persistente)
- Un solo usuario concurrente por sesión
- Sin base de datos real
- Sin API backend

### Mejoras para Producción
1. **Backend API**
   - FastAPI o Flask
   - Endpoints RESTful
   - JWT authentication

2. **Base de Datos**
   - PostgreSQL para datos transaccionales
   - Redis para caché de sesiones
   - S3 para almacenar imágenes faciales

3. **Machine Learning**
   - Modelos de reconocimiento facial entrenados
   - Detección de vida (liveness detection)
   - Anti-spoofing

4. **Infraestructura**
   - Docker containers
   - Kubernetes orchestration
   - Load balancing
   - CDN para assets estáticos

## 🧪 Testing

### Tests Incluidos
- `test_app.py`: Verificación de sintaxis e importaciones

### Tests Recomendados para Producción
```python
# Unit tests
- test_verificar_pin()
- test_realizar_transaccion()
- test_detectar_rostro()

# Integration tests
- test_flujo_completo_pago()
- test_saldo_insuficiente()
- test_pin_incorrecto()

# E2E tests
- test_interfaz_usuario_completa()
- test_multiples_transacciones()
```

## 📱 Compatibilidad

### Navegadores Soportados
- Chrome/Edge (últimas 2 versiones)
- Firefox (últimas 2 versiones)
- Safari (últimas 2 versiones)

### Dispositivos
- Desktop (Windows, macOS, Linux)
- Tablets (iOS, Android)
- Mobile (responsive design)

### Requisitos del Sistema
- Python 3.8+
- 4GB RAM mínimo
- Cámara web (para reconocimiento facial real)

## 🔧 Configuración Avanzada

### Variables de Entorno (.env)
```bash
# En producción, usar variables de entorno
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_THEME_PRIMARY_COLOR=#1E88E5

# Base de datos
DATABASE_URL=postgresql://user:pass@localhost/face2pay

# Seguridad
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
```

### Streamlit Secrets
```toml
# .streamlit/secrets.toml (NO incluir en git)
[database]
url = "postgresql://..."

[security]
secret_key = "..."
```

## 📈 Roadmap

### Versión 1.0 (Actual - Demo)
- ✅ Interfaz básica Streamlit
- ✅ Simulación de reconocimiento facial
- ✅ Verificación de PIN
- ✅ Procesamiento de transacciones
- ✅ Historial básico

### Versión 2.0 (Futuro)
- [ ] Integración con cámara real
- [ ] Reconocimiento facial real
- [ ] Base de datos PostgreSQL
- [ ] API REST backend
- [ ] Autenticación mejorada

### Versión 3.0 (Futuro)
- [ ] Integración bancaria real
- [ ] Multi-currency support
- [ ] Reportes y analytics
- [ ] Mobile app nativa
- [ ] Blockchain para auditoría

## 🤝 Contribución

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Proyecto desarrollado para Hackathon #IBFH2025.

---

**Face2Pay** - Revolucionando los pagos con biometría 🚀
