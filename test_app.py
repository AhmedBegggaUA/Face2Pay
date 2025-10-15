#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación Face2Pay puede ejecutarse.
Prueba las importaciones y funciones básicas sin ejecutar Streamlit.
"""

import sys
import os

def test_imports():
    """Verifica que todos los módulos necesarios pueden importarse"""
    print("🔍 Verificando importaciones...")
    
    try:
        import streamlit
        print("✅ streamlit importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando streamlit: {e}")
        return False
    
    try:
        import cv2
        print("✅ opencv-python importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando cv2: {e}")
        return False
    
    try:
        import numpy
        print("✅ numpy importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando numpy: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando Pillow: {e}")
        return False
    
    try:
        import face_recognition
        print("✅ face-recognition importado correctamente")
    except ImportError as e:
        print(f"⚠️ Advertencia: face-recognition no disponible: {e}")
        print("   (Esto es esperado si las dependencias del sistema no están instaladas)")
    
    return True

def test_app_syntax():
    """Verifica que app.py tiene sintaxis Python válida"""
    print("\n🔍 Verificando sintaxis de app.py...")
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        compile(code, 'app.py', 'exec')
        print("✅ app.py tiene sintaxis válida")
        return True
    except SyntaxError as e:
        print(f"❌ Error de sintaxis en app.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Error leyendo app.py: {e}")
        return False

def test_requirements():
    """Verifica que requirements.txt existe y contiene dependencias"""
    print("\n🔍 Verificando requirements.txt...")
    
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if len(lines) > 0:
            print(f"✅ requirements.txt contiene {len(lines)} dependencias")
            for line in lines:
                print(f"   - {line}")
            return True
        else:
            print("❌ requirements.txt está vacío")
            return False
    except Exception as e:
        print(f"❌ Error leyendo requirements.txt: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("Face2Pay - Script de Pruebas")
    print("=" * 60)
    print()
    
    results = []
    
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)
    
    # Ejecutar pruebas
    results.append(("Importaciones", test_imports()))
    results.append(("Sintaxis de app.py", test_app_syntax()))
    results.append(("Requirements.txt", test_requirements()))
    
    # Resumen
    print("\n" + "=" * 60)
    print("Resumen de Pruebas")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status}: {test_name}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 ¡Todas las pruebas pasaron!")
        print("\nPara ejecutar la aplicación:")
        print("  streamlit run app.py")
        return 0
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa los errores arriba.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
