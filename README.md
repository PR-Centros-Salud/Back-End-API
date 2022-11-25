# ¿COMO DESPLEGAR EL SISTEMA?

<br>

## SOFTWARE NECESARIO

<br>

* Python 3.10 +
* NodeJS
* YARN
* ExpoGO (Disponible tanto en IOS como en ANDROID)

<br>

## PARA DESPLIEGUE DEL BACK-END

<br>

Clonamos el repositorio

    git clone https://github.com/PR-Centros-Salud/Back-End-API.git &&
    cd Back-End-API

### MacOS or Linux
    source ./venv/bin/activate

### Windows
    ./venv/bin/activate

En caso de tener algun error con el entorno virtual, basta con verificar el paquete causante del error e instalarlo a mano.

<br>

Instalado el repositorio y levantado el entorno virtual hay que modificar el *.env* de la siguiente manera:

    DB_USERNAME=(nombre de usuario de la base de datos(MySQL))
    DB_PASSWORD=(password del usuario de la base de datos(MySQL))
    DB_HOST=(URL del host de la base de datos(MySQL))
    DB_PORT=(puerto de la base de datos(MySQL))
    DB_NAME=(nombre de la base de datos(MySQL))
    SECRET_KEY=(llave secreta para hasheo de tokens JWT)
    ALGORITHM=HS256 (Algoritmo para hashear tokens JWT)
    ACCESS_TOKEN_EXPIRE_MINUTES=(tiempo de expiracion de los tokens JWT)
    SUPER_ADMIN_SECRET=(llave secreta para creacion de superadmins)
    TWILIO_ACCOUNT_SID=(SID de twilio)
    TWILIO_AUTH_TOKEN=(auth token de twilio)
    TWILIO_NUMBER=(numero de telefono twilio)

<br>

Por ultimo basta con recargar los cambios.

    cd app

### MacOS or Linux
    uvicorn main:app --reload

### Windows
    python -m uvicorn main:app --reload