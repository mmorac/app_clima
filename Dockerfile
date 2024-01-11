#Instala la última versión de alpine y actualiza
FROM alpine:latest
RUN apk update && apk add --no-cache gcc musl-dev linux-headers

#Configurar imagen
RUN apk update 
RUN apk add py-pip
RUN apk add --no-cache python3-dev
RUN pip install --upgrade pip --break-system-packages

#Configurar workspace
#El directorio de trabajo puede llevar cualquier nombre
WORKDIR /app
#Copio todos los archivos de la carpeta donde está el Dockerfile en /app 
COPY . /app/

#Instalar las librerías de Python
RUN pip install -r requirements.txt
#Ejecutar en consola el script principal de Python
CMD ["python3", "app.py"]