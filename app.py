"""
Examen Unidad III 
Autor: [Tu Nombre]
Fecha: [Fecha Actual]

Descripción:
Objetivo del examen
Desarrollar una API básica con Flask que permita:

Crear un diccionario de dispositivos de red.
Agregar nuevos dispositivos.
Modificar dispositivos existentes.
Mostrar un listado de todos los dispositivos en formato HTML, 
donde cada dispositivo se muestre en un <div> con nombre, 
descripción y características

Requisitos técnicos

Usar Flask.
Usar un diccionario como estructura principal de almacenamiento.
Implementar al menos tres rutas:

GET /dispositivos_html: muestra todos los dispositivos en HTML.
POST /dispositivos: agrega un nuevo dispositivo.
PUT /dispositivos/<id>: modifica un dispositivo existente.

Ejemplo del Diccionario de dispositivos: 
{
  "id": "router01",
  "nombre": "Router Principal",
  "descripcion": "Router de borde para salida a Internet",
  "ip": "192.168.1.1",
  "mac": "00:1A:2B:3C:4D:5E",
  "ubicacion": "Sala de servidores",
  "tipo": "Router",
  "otros": ""
}

Recuerda tener al menos 3 commits en tu repositorio. 

Para puntos extra
Puedes ocupar css para añadir puntos a tu examen, perzonalizalo con estilos como el siguiente:
<style>
    .dispositivo {
        border: 1px solid #ccc;
        padding: 10px;
        margin: 10px;
    }
</style>

Puntos extra para añador formula en el cmapo de otros
la formula es la siguente: 

último octeto de la IP * 3 + longitud del nombre del dispositivo + ":" + nombre (Cambiando los espacios por _)

"""

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# Commit 3: Mostrar todos los dispositivos

dispositivos = {
    "router01": {
        "id": "router01",
        "nombre": "Router Principal",
        "descripcion": "Router que conecta a Internet",
        "ip": "192.168.1.1",
        "mac": "00:1A:2B:3C:4D:5E",
        "ubicacion": "Sala de servidores",
        "tipo": "Router",
        "otros": ""
    },
    "switch01": {
        "id": "switch01",
        "nombre": "Switch Oficina",
        "descripcion": "Switch de red para área administrativa",
        "ip": "192.168.1.10",
        "mac": "AA:BB:CC:DD:EE:11",
        "ubicacion": "Piso 1",
        "tipo": "Switch",
        "otros": ""
    },
    "ap01": {
        "id": "ap01",
        "nombre": "Access Point Principal",
        "descripcion": "Punto de acceso WiFi principal",
        "ip": "192.168.1.20",
        "mac": "FF:EE:DD:CC:BB:AA",
        "ubicacion": "Recepción",
        "tipo": "Access Point",
        "otros": ""
    }
}

@app.route('/dispositivos_html', methods=['GET'])
def mostrar_dispositivos_html():
    html = """
    <html>
    <head>
        <title>Dispositivos de Red</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 20px;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            .dispositivo {
                border: 1px solid #ccc;
                padding: 10px;
                margin: 10px auto;
                border-radius: 10px;
                background-color: #fff;
                width: 60%;
                box-shadow: 0px 0px 5px #aaa;
            }
            .dispositivo h2 {
                color: #0066cc;
            }
        </style>
    </head>
    <body>
        <h1>Lista de Dispositivos</h1>
        {% for d in dispositivos.values() %}
            <div class="dispositivo">
                <h2>{{ d['nombre'] }}</h2>
                <p><b>ID:</b> {{ d['id'] }}</p>
                <p><b>Descripción:</b> {{ d['descripcion'] }}</p>
                <p><b>IP:</b> {{ d['ip'] }}</p>
                <p><b>MAC:</b> {{ d['mac'] }}</p>
                <p><b>Ubicación:</b> {{ d['ubicacion'] }}</p>
                <p><b>Tipo:</b> {{ d['tipo'] }}</p>
                <p><b>Otros:</b> {{ d['otros'] }}</p>
            </div>
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(html, dispositivos=dispositivos)

@app.route('/dispositivos', methods=['POST'])
def agregar_dispositivo():
    data = request.get_json()
    id = data.get('id')

    if not id:
        return jsonify({"error": "Debe incluir un 'id'"}), 400
    if id in dispositivos:
        return jsonify({"error": "El dispositivo ya existe"}), 400

    try:
        ultimo_octeto = int(data['ip'].split('.')[-1])
    except:
        return jsonify({"error": "La IP no es válida"}), 400

    formula = ultimo_octeto * 3 + len(data['nombre'])
    otros = f"{formula}:{data['nombre'].replace(' ', '_')}"
    data['otros'] = otros

    dispositivos[id] = data
    return jsonify({"mensaje": "Dispositivo agregado correctamente"}), 201

if __name__ == '__main__':
    app.run(debug=True)
