import requests
import pandas as pd
from datetime import datetime
import os
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Configuración
API_URL = "https://www.datos.gov.co/resource/32sa-8pi3.json?$limit=30&$order=vigenciadesde DESC"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def obtener_datos_trm():
    """Obtiene datos de TRM desde la API"""
    try:
        response = requests.get(API_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error al obtener datos: {str(e)}")
        return None

def procesar_datos(data):
    """Procesa los datos de la API"""
    if not data:
        logging.warning("Usando valores de respaldo")
        return 4000.00, datetime.now().strftime("%Y-%m-%d")
    
    ultimo = data[0]
    return float(ultimo['valor']), ultimo['vigenciadesde']

def guardar_datos(trm, fecha):
    """Guarda datos en archivos CSV"""
    # Crear dataframe con los datos actuales
    nuevo_registro = pd.DataFrame({
        'Fecha': [fecha],
        'TRM': [trm],
        'Actualizado': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    })
    
    # Archivo diario (siempre se agrega)
    diario_path = 'data/trm_diaria.csv'
    nuevo_registro.to_csv(diario_path, mode='a', header=not os.path.exists(diario_path), index=False)
    
    # Archivo histórico (evita duplicados)
    historico_path = 'data/trm_historico.csv'
    if os.path.exists(historico_path):
        historico = pd.read_csv(historico_path)
        if fecha not in historico['Fecha'].values:
            pd.concat([nuevo_registro, historico]).to_csv(historico_path, index=False)
    else:
        nuevo_registro.to_csv(historico_path, index=False)

def main():
    logging.info("Iniciando proceso de actualización TRM")
    
    try:
        # Obtener y procesar datos
        datos = obtener_datos_trm()
        trm, fecha = procesar_datos(datos)
        
        logging.info(f"TRM obtenida: ${trm:,.2f} COP para {fecha}")
        
        # Guardar datos
        guardar_datos(trm, fecha)
        logging.info("Datos guardados exitosamente")
        
    except Exception as e:
        logging.error(f"Error en el proceso principal: {str(e)}")
        raise

if __name__ == "__main__":
    main()
