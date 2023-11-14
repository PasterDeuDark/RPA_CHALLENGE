# RPA Chalenge

Para  la ejecucion del programa se neceita configurar algunas cosas antes

1. Configurar las variables de entorno las cuales son indispensables para la ejecucion del mismo

```bash

    MONGO_INITDB_ROOT_USERNAME=
    MONGO_INITDB_ROOT_PASSWORD=
    MONGO_USERNAME=
    MONGO_PASSWORD=
    MONGO_HOST=
    MONGO_PORT=27017
    MONGO_DATABASE_NAME=
    MONGO_COLLECTION_NAME=

```
estas variables son tanto para la conexion como para la ejecucion de la DB la cual se utiliza mongodb

```bash

    EMAIL_USER=
    EMAIL_PASSWORD=
    EMAIL_SERVER=
    EMAIL_PORT=
```

estas variables son para sistema de gestion de email

2. se monta la imagen de Mongodb a traves de docker 

```bash
    docker compose up -d
```

3. Se crea un Ambiente de python con

```bash
    python -m venv .venv
```

luego trae las dependencias con 

```bash
    pip install -r requirements.txt
```

despues ejecuta el programa con 

```bash
    python script.py

```

para que este se ejecute cada cierto tiempo recomendaria una ejecucion cada dia con crontab como podriamos hacerlo  de
la siguiente forma


```bash
   crontab -e

    0 0 * * * python3 ./script.py

```