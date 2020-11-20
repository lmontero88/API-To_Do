from flask import Flask,render_template,request,jsonify
from model import List, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask (__name__)

app.url_map.strict_slashes = False # este me admite que deje el url con el slash al final.
app.config['DEBUG'] = True # Este es para poder ver los errores 
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Se usa para poder usar SQLALQUEMY que es quien traduce el codigo de python a lenguaje de base de dato SQL
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://<user>:<passwd>@<ip>:<port>/<databasename>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://lmontero88:Lilian1988@localhost:3306/to_do_list' # en este link se direcciona la informacion que se genera hacia a la base de dato. Tambien hay que instalar mysql-connector-python
db.init_app(app) # inicializar la aplicacion flask con la base de dato sqlalchemy
Migrate(app, db) # este migra toda las clases de tabla a dato Sql(solo los esquemas, no la data)
manager = Manager(app) # este tambien debe importarse desde el flask_script
manager.add_command('db', MigrateCommand) # init migrate upgrade downgrade

@app.route("/")#creando las rutas de acceso a la base de datos
def main(): 
    return render_template('index.html')# este es para que la API tenga una pagina visible en html. Para usar render template se importa arriba en flask. Se crea una carpeta llamada TEMPLATES  que contiene el archivo index.html

""" @app.route("/api/list/", methods = ['GET','POST']) #creando las rutas para acceder a los distintas peticiones.
@app.route('/api/contacts/<id>', methods=['GET', 'PUT', 'DELETE'])#creando las rutas para acceder a los distintas peticiones pero a traves del Id.
def lists(id = None): # en esta funcion se realizan todas las validaciones para cada petición.
    if request.methods == 'GET': #para usar el request es necesarion importarlos desde flask. El request es un objeto de flask que permite identificar la peticion que hace el cliente ('GET'), y se puede acceder por el atributo .methods
        if id is not None: # si el id no es None
            list = List.query.get(id) # creo esta variable list que hace una consulta(query) a la clase List y devuelveme por el Id que te consulté toda la fila que pertenece a ese id, ej: Id:2 y me daria el label y done vinculado a ese Id
            if list: # si esta fila existe entonces devuelveme en formaro json la fila segun el metodo que serealizo la clase List
                return jsonify(list.serialize()), 200 # explicacion de linea anterior y el 200 es que todo esta OK
            else:
                return jsonify({"msg": "List doesn't exist"}), 404 # en el caso que no encuentre la fila del Id pues mandame el mensaje y el error 404 que no fue encontrada ninguna fila por el numero de Id
        else:
            list = List.query.all()
            list = list(map(lambda list: list.serialize(), lists))
            return jsonify(lists), 200
 """
@app.route("/api/list/<user>",methods = ['GET'])
def get_list(user):
    lists = List.query.filter_by(user=user)
    json_lists = list(map(lambda l: l.serialize(), lists))
    return jsonify(json_lists)

@app.route("/api/list/",methods = ['GET'])
def get_all_list ():
    listas = List.query.all()
    listas = list(map(lambda contact: contact.serialize(), listas))
    return jsonify(listas), 200


@app.route("/api/list/",methods = ['POST'])
def post_list():
    user = request.json.get('user', None)
    label = request.json.get('label', None)
    done = request.json.get('done', False)

    if not user:
        return jsonify({"msg": "name is required"}), 400
    if not label:
        return jsonify({"msg": "label is required"}), 400

    list = List()
    list.user = user
    list.label = label
    list.done = done
    
    list.save()

    return jsonify(list.serialize()), 201

@app.route("/api/list/<id>",methods = ['PUT'])
def put_list(id):
    user = request.json.get('user', None)
    label = request.json.get('label', None)
    done = request.json.get('done', False)

    if not user:
            return jsonify({"msg": "user is required"}), 400
    if not label:
            return jsonify({"msg": "label is required"}), 400

    list = List.query.get(id)# get solo busca en base de datos por id

    if not list:
        return jsonify({"msg": "List doesn't exist"}), 404

    list.user = user
    list.label = label
    list.done = done

    list.update()

    return jsonify(list.serialize()), 200

@app.route("/api/list/user/<user>",methods = ['DELETE'])
def delete_list(user):
    lists = List.query.filter_by(user=user)

    for l in lists:
        l.delete()
   
    return jsonify({
        'mensaje': 'Tareas eliminadas del usuario ' + user
    })

@app.route("/api/list/<id>",methods = ['DELETE'])
def del_tarea(id):
    list = List.query.get(id)
    if not list:
        return jsonify({"msg": "Label doesn't exist"}), 404
        
    list.delete()
    return jsonify({"succes": "label deleted"}), 200



if __name__=='__main__':#esto es para iniciar servidor Flask
    manager.run() 
