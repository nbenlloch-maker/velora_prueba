# main.py
import os
import webbrowser               # Para abrir el navegador (WhatsApp)
from urllib.parse import quote  # Para codificar el mensaje en la URL
from pypdf import PdfReader     # Para leer PDFs reales
from screener import analyze_cv
from interviewer import start_interview

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

def cargar_documento(ruta_archivo: str) -> str:
    """
    Lee archivos PDF o TXT desde el disco duro.
    Limpia las comillas que aparecen al arrastrar archivos en la terminal.
    """
    ruta_archivo = ruta_archivo.strip().strip("'").strip('"')
    
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"❌ El archivo no existe: {ruta_archivo}")

    texto_extraido = ""

    # Caso PDF
    if ruta_archivo.lower().endswith('.pdf'):
        try:
            reader = PdfReader(ruta_archivo)
            for page in reader.pages:
                texto_extraido += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error leyendo PDF: {e}")

    # Caso TXT
    elif ruta_archivo.lower().endswith('.txt'):
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                texto_extraido = f.read()
        except Exception as e:
            raise Exception(f"Error leyendo TXT: {e}")
    else:
        raise ValueError("⚠️ Formato no soportado. Usa .pdf o .txt")

    return texto_extraido

def contactar_por_whatsapp(telefono: str, nota: float):
    """
    Abre WhatsApp Web/Desktop con un mensaje pre-redactado.
    """
    if not telefono:
        print("⚠️ No se encontró teléfono en el CV.")
        return

    # Limpiamos el número para la URL
    clean_phone = telefono.replace(" ", "").replace("-", "").replace("+", "")
    
    mensaje = (
        f"Hola! 👋 Soy el asistente Velora. Hemos analizado tu perfil y "
        f"tienes una coincidencia del {nota:.1f}%. ¿Te interesa una entrevista?"
    )
    
    # Creamos el enlace oficial de la API de WhatsApp
    url = f"https://wa.me/{clean_phone}?text={quote(mensaje)}"
    
    print(f"\n📱 Abriendo WhatsApp para: {clean_phone}...")
    webbrowser.open(url)

def main():
    print("--- 🚀 VELORA AI RECRUITER (LOCAL & REAL) ---")
    print("ℹ️  Arrastra los archivos a esta ventana cuando se te pida.")

    try:
        # 1. Carga de Archivos Reales
        path_oferta = input("\n📂 Arrastra aquí la OFERTA (PDF/TXT): ")
        texto_oferta = cargar_documento(path_oferta)
        
        path_cv = input("📄 Arrastra aquí el CV (PDF/TXT): ")
        texto_cv = cargar_documento(path_cv)

        # 2. Fase de Screening (IA)
        resultado = analyze_cv(texto_oferta, texto_cv)
        
        print("\n📊 RESULTADO FASE 1 (Análisis):")
        # Mostramos el JSON generado
        print(resultado.model_dump_json(indent=2))

        if resultado.discarded:
            print("\n❌ CANDIDATO DESCARTADO (Falta requisito obligatorio).")
            return

        # 3. Fase de Entrevista (Si hace falta)
        nota_final = resultado.score
        if resultado.not_found_requirements:
            nota_final = start_interview(resultado)
        
        print("\n" + "="*50)
        print(f"🎯 PUNTUACIÓN FINAL: {nota_final}%")
        print("="*50)

        # 4. Acción Final (WhatsApp)
        # Si la nota es buena (ej: > 70%), proponemos contactar
        if nota_final >= 70:
            print("✅ El candidato es APTO.")
            print(f"📞 Teléfono detectado: {resultado.phone}")
            
            if resultado.phone:
                accion = input("👉 ¿Quieres abrir WhatsApp para contactarle? (s/n): ")
                if accion.lower() == 's':
                    contactar_por_whatsapp(resultado.phone, nota_final)
        else:
            print("⏹️ El candidato no supera el umbral del 70%.")

    except Exception as e:
        print(f"\n❌ Ocurrió un error: {e}")

if __name__ == "__main__":
    main()