## Proyecto final ##

Este es un proyecto, de aplicacion utilizando Flask, un microframework para Python

Para que esta app funcione a nivel local, deberas tener instalado #requirements

clona el repositorio o descarga a tu PC

...
 
abre un terminal con, ctr + shif + ñ, y con el comando:

python -m venv venv

si lo corres en windows activa un protocolo de ejecucion
esto evitara conflictos; en terminal con el comando:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

finalmente activa el entorno virtual, en terminal con:

venv\Scripts\activate

si todo va bien, verás un cartel (venv) a la izq del comando

corre la app en terminal:  python app.py 

deberia aparecer un http, copia y pega en el navegador
ejecuta (enter) y podras observar el funcionamiento de la app.




# Proyecto Flask - Proyecto-Final

Este proyecto está basado en Flask y utiliza la siguiente estructura de carpetas:

## Estructura de carpetas

```
Proyecto-Final/
├── app.py              # Archivo principal de la aplicación Flask
├── requirements.txt    # Dependencias del proyecto
├── static/             # Archivos estáticos (CSS, JS, imágenes)
├── templates/          # Plantillas HTML (Jinja2)
```

## Descripción de carpetas y archivos

- **app.py**: Punto de entrada de la aplicación Flask.
- **requirements.txt**: Lista de paquetes necesarios para ejecutar el proyecto.
- **static/**: Archivos estáticos que se sirven directamente al navegador (CSS, JS, imágenes).
- **templates/**: Archivos HTML que se renderizan desde Flask usando Jinja2.

## Instalación y ejecución

clona el repositorio o descarga a tu PC, si descargas, para pruebas y mas seguridad, 
crea un entorno virtual en terminal de VSCode con:
	-python -m venv venv
	-Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process (evita conflictos)
	-venv\Scripts\activate
se activa el entorno y se observa (venv) al inicio de la linea del comando
luego instala las dependencias:
	-pip install -r requirements.txt
Ejecuta la aplicación:
	-python app.py

## Recomendaciones

- Asegúrate de tener Python y pip instalados en tu sistema.
- Puedes sugerir y agregar más módulos y carpetas según te parezca para mejorar el proyecto
- Para agregar nuevas rutas, edita el archivo 'app.py'
