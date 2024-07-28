# SolManAd

SolManAd es un sistema de gestión de solicitudes de mantenimiento.

## Instalación y configuración

Sigue los pasos a continuación para clonar el repositorio, configurar el entorno virtual, instalar las dependencias, crear un superusuario, inicializar la base de datos con datos de prueba y ejecutar el servidor.

### 1. Clonar el repositorio

Clona el repositorio en tu máquina local:

```bash
git clone https://github.com/OscarCuba18/SolManAd.git
cd SolManAd

### 2. Crear y activar el entorno virtual

python -m venv SolManAd_Venv
SolManAd_Venv\Scripts\activate

### 3. Intalar dependencias
pip install -r requirements.txt

### 4. Ejecutar migraciones
python manage.py migrate

### 5. Crear superusuario
python manage.py createsuperuser

### 6. Poblar la base de datos con datos de prueba
python seeder.py

### 6. Poblar la base de datos con datos de prueba
Ejecutar el servidor

python manage.py runserver