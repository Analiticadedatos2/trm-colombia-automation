import sys
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('trm_debug.log')
    ]
)

def main():
    try:
        logging.info("Iniciando obtención de TRM")
        
        # Tu lógica actual aquí...
        # Añade logging en cada paso importante
        logging.info("Proceso completado exitosamente")
        return 0
        
    except Exception as e:
        logging.error(f"Error crítico: {str(e)}", exc_info=True)
        return 2  # Código de error

if __name__ == "__main__":
    sys.exit(main())
