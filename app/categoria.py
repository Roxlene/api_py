#Importar Librerias Instaladas
#pip install flask
#pip install flask-sqlalchemy   -----Para Conectar a una BD SQL
#pip install flack-marshmallow  -----Definir Esquema con la BD
#pip install marshmallow-sqlalchemy
#pip install pymysql            ------Para Conectar a MySQL Driver MySQL

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:28143033@localhost:5432/sigespro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#Creacion de tabla Categoria
class Categoria(db.Model):
    cat_id = db.Column(db.Integer,primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desp = db.Column(db.String(100))

    def __init__(self, cat_nom, cat_desp):
        self.cat_nom = cat_nom
        self.cat_desp = cat_desp

#Corrida de migracion
with app.app_context():
    db.create_all()

#Creacion de schema Categoria
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nom', 'cat_desp')

#Mostrar solo un resultado
categoria_schema = CategoriaSchema()

#Mostrar mas de un resultado
categorias_schema = CategoriaSchema(many=True)



#rutas

#Mensaje de bienvenida en la raiz
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message":"Bienvenido a python"})

#Get all Categoria
@app.route('/categorias', methods=['GET'])
def Categorias_all():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)

#Get a Categoria
@app.route('/categorias/<id>', methods=['GET'])
def Categoria_id(id):
        a_categoria = Categoria.query.get(id)
        if a_categoria:
            return categoria_schema.jsonify(a_categoria)
        else:
            return jsonify({'message': 'El id introducido no pertenece a ningun regirtro'})


#POST a Categoria
@app.route('/categorias', methods=['POST'])
def Categoria_insert():
    requests = request.get_json(force=True)
    cat_nom = requests['cat_nom']
    cat_desp = requests['cat_desp']
    nuevo_registro = Categoria(cat_nom, cat_desp)
    db.session.add(nuevo_registro)
    db.session.commit()
    return categoria_schema.jsonify(nuevo_registro)

#PUT a Categoria
@app.route('/categorias/<id>', methods=['PUT'])
def Categoria_update(id):
    try:
        requests = request.get_json(force=True)
        actualizado = Categoria.query.get(id)
        cat_nom = requests['cat_nom']
        cat_desp = requests['cat_desp']
        actualizado.cat_nom = cat_nom
        actualizado.cat_desp = cat_desp
        db.session.commit()
        return categoria_schema.jsonify(actualizado)
    except:
        return jsonify({'message': 'El id introducido no pertenece a ningun regirtro'})

#DELETE a Categoria
@app.route('/categorias/<id>', methods=['DELETE'])
def Categoria_delete(id):
    try:
        eliminado = Categoria.query.get(id)
        db.session.delete(eliminado)
        db.session.commit()
        return categoria_schema.jsonify(eliminado)
    except:
        return jsonify({'message': 'El id introducido no pertenece a ningun regirtro'})

if __name__ == '__main__':
    app.run(debug=True)