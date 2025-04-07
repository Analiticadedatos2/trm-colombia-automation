import requests
import pandas as pd
from datetime import datetime

def main():
    try:
        # Extraer TRM
        url = "https://www.datos.gov.co/resource/32sa-8pi3.json?$limit=1&$order=vigenciadesde DESC"
        data = requests.get(url, timeout=10).json()[0]
        trm = float(data['valor'])
        fecha = data['vigenciadesde']
        
        # Guardar en CSV
        df = pd.DataFrame({'Fecha': [fecha], 'TRM': [trm]})
        df.to_csv('trm_diaria.csv', mode='a', header=not pd.io.common.file_exists('trm_diaria.csv'), index=False)
        print(f"✅ TRM {fecha}: ${trm:,.2f} COP guardada")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
