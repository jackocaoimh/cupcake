from flask import Flask, render_template, Response, flash, request, redirect, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jackocaoimh:turner12345@localhost/cupcakes'
app.config['SECRET_KEY'] = 'ASDF'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True

db.init_app(app)
connect_db(app)  

# Retrieves all cupcakes 
# Does not need a Get method defined becuase default is GET
@app.route('/api/cupcakes')
def get_cupcakes():
    # what is .to_dict function, flask or python - for look within that ?
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


# POST route for creating cupcake 
@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    data = request.json

    # need clarity on this. Same as other. left side relates to Cupcake model and right side relates to json structure 
    cupcake = Cupcake(flavor=data['flavor'], 
                      size=data['size'],
                      rating=data['rating'],
                      image=data['image'] or None)
    
    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.to_dict()), 201)


# Retrieves specific cupcake 
@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())


# Edit page for specific cupcake - patch method
@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):

    # not sure why this line in necessary 
    # may relate to line further down = data['flavor']
    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    #left side is able to use . notation because it was defined in line above
    # right side uses 'flavor' etc because it is tapping into json hence data
    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.sesion.commit()
    #need clarity here. Not sure why =cupcake.to_dict()
    return jsonify(cupcake=cupcake.to_dict())

# method for deleting cupcake
# Uses cupcake_id in url to find the relatad cupcake
@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
#cupcake_id is passed into function
def delete_cupcake(cupcake_id):
    # set cupcake equal to matching cupcake_id when searching entire db
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    # once cupcake is identified it is added to delete queue
    db.session.delete(cupcake)
    # then commited
    db.session.commit()
    # json message created 
    return jsonify(message='Deleted')