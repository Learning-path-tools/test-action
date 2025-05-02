"""
Archivo de configuración global para el framework de automatización.
Contiene variables y configuraciones utilizadas en todo el proyecto.
"""
import os
from dotenv import load_dotenv
'''
from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.resource import ResourceManagementClient

#ID de suscripción de Azure
subscription_id = '3912f235-0a8c-4af2-8ca4-95f2e457cf4a'
    # Configurar las credenciales utilizando DefaultAzureCredential
credentials = DefaultAzureCredential()
    # Cliente para interactuar con los recursos de Azure
resource_client = ResourceManagementClient(credentials, subscription_id)
    # Cliente para interactuar con los servicios de contenedor de Azure
aks_client = ContainerServiceClient(credentials, subscription_id)
    # Obtener la lista de clústeres AKS
clusters = aks_client.managed_clusters.list()
Nombre = []
    # Mostrar información sobre cada clúster
for cluster in clusters:    
    Nombre.append(cluster.name)

    # Cerrar sesiones
aks_client.close()
resource_client.close()
'''

# Carga variables de entorno a mi entorno virtual 
load_dotenv()

# URL base del 
BASE_URLS = [
    f"https://ftdspprod{str(i).zfill(3)}.ftds.rockwellautomation.com/"
    for i in range(1, 21)  # Genera URLs de produccion del 001 al 020
]
# URL base por defecto (la primera en la lista)
DEFAULT_BASE_URL = BASE_URLS[-1]
# Timeouts globales (en segundos)
DEFAULT_TIMEOUT = 120
IMPLICIT_WAIT = 5
PAGE_LOAD_TIMEOUT = 10

# Configuración de navegador por defecto
DEFAULT_BROWSER = "chrome"

# Rutas de directorios
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")

# Credenciales
TEST_USERNAME = os.getenv("TEST_USERNAME","")
TEST_PASSWORD = os.getenv("TEST_PASSWORD","")

# Asegura que los directorios necesarios existen
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)