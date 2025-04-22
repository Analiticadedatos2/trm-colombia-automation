import requests
import pandas as pd
from datetime import datetime
import os
from pathlib import Path

# Configuración
DATA_URL = "https://www.datos.gov.co/resource/32sa-8pi3.json?$limit=30&$order=vigenciadesde DESC"
HISTORIC_FILE = 'data/trm_historico.csv'
DAILY_FILE = 'data/trm_diaria.csv'
BACKUP_TRM = 4200.00  # Valor de respaldo

def setup_directories():
    """Crear estructura de directorios si no existe"""
    Path('data').mkdir(exist_ok=True)

def fetch_trm_data():
    """Obtener datos de TRM de la API"""
    try:
        response = requests.get(DATA_URL, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"⚠️ Error al obtener datos: {str(e)}")
        return None

def process_trm_data(data):
    """Procesar datos de la API"""
    if not data:
        print("ℹ️ Usando valor de respaldo")
        return BACKUP_TRM, datetime.now().strftime("%Y-%m-%d")
    
    latest = data[0]
    return float(latest['valor']), latest['vigenciadesde']

def update_historic_data(trm, fecha):
    """Actualizar archivo histórico con validación de duplicados"""
    new_entry = pd.DataFrame({
        'Fecha': [fecha],
        'TRM': [trm],
        'Fecha_Registro': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    })
    
    if os.path.exists(HISTORIC_FILE):
        historic = pd.read_csv(HISTORIC_FILE)
        # Verificar si la fecha ya existe
        if fecha not in historic['Fecha'].values:
            updated = pd.concat([new_entry, historic])
            updated.to_csv(HISTORIC_FILE, index=False)
            print("📊 Histórico actualizado")
        else:
            print("⏩ Registro ya existe en histórico")
    else:
        new_entry.to_csv(HISTORIC_FILE, index=False)
        print("📁 Archivo histórico creado")

def update_daily_file(trm, fecha):
    """Actualizar archivo diario (siempre agrega)"""
    new_entry = pd.DataFrame({
        'Fecha': [fecha],
        'TRM': [trm],
        'Timestamp': [datetime.now().isoformat()]
    })
    
    write_header = not os.path.exists(DAILY_FILE)
    new_entry.to_csv(DAILY_FILE, mode='a', header=write_header, index=False)
    print("📅 Registro diario agregado")

def generate_stats():
    """Generar estadísticas básicas si hay histórico"""
    if os.path.exists(HISTORIC_FILE):
        df = pd.read_csv(HISTORIC_FILE)
        stats = {
            'Registros': len(df),
            'TRM_Maxima': df['TRM'].max(),
            'TRM_Minima': df['TRM'].min(),
            'TRM_Promedio': round(df['TRM'].mean(), 2),
            'Primera_Fecha': df['Fecha'].iloc[-1],
            'Ultima_Fecha': df['Fecha'].iloc[0]
        }
        pd.DataFrame.from_dict(stats, orient='index').to_csv('data/trm_estadisticas.csv')
        print("📈 Estadísticas generadas")

def main():
    print("\n🔄 Iniciando actualización TRM...")
    setup_directories()
    
    try:
        # Flujo principal
        data = fetch_trm_data()
        trm, fecha = process_trm_data(data)
        
        print(f"\n💵 TRM {fecha}: ${trm:,.2f} COP")
        
        update_historic_data(trm, fecha)
        update_daily_file(trm, fecha)
        generate_stats()
        
        print("\n✅ Proceso completado exitosamente")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error crítico: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
