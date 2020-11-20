from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class List(db.Model): # a partir de esta clase se genera:
    __tablename__ = 'list' #la tabla llamada list, los nombre de tabla por convencion es en singular
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    user = db.Column(db.String(100))
    label = db.Column(db.String(100), nullable = True)
    done = db.Column(db.Boolean, default=False)

    def serialize(self): # esta funcion lo que hace es que retorna los campos en Json, se puede ver porque returna con llaves
        return{
            'id': self.id,
            'user': self.user,
            'label': self.label,
            'done': self.done
        }

    def save(self): # estos metodos se crean para la clase List para luego ser llamados en los 'GET' 'POST' 'PUT' y 'DELETE' segun correspondan
        db.session.add(self) # session es un objeto de flask_sqlalchemy que indica el espacio donde se van a realizar los metodos de add y commit tambien de lask_sqlalchemy
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

