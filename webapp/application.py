# dependencies
# from CorgiData import CorgiData
from CorgiData import CorgiData

from flask import Flask, jsonify, request

#################################################
# Database Setup
#################################################
cg = CorgiData()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def show_apis():
    """List all available api routes."""
    return (
        f"<h4>Available Routes:</h4>"
        f'<a href="/api/v1.0/pets">/api/v1.0/pets</a><br/>'       
        f'<a href="/api/v1.0/pets/Patterson">/api/v1.0/pets/(name)</a><br/>'       
        f'<a href="/api/v1.0/pet_training">/api/v1.0/pet_training</a><br/>' 
        f'<a href="/api/v1.0/pet_training/Judson">/api/v1.0/pet_training/(name)</a><br/>' 
        f'<a href="/"><h4>Back</h4></a><br/>' 
    )      

@app.route("/api/v1.0/pets")
def get_all_pets():
    return jsonify(cg.get_pet_data())

@app.route("/api/v1.0/pets/<pet_name>")
def get_one_pet(pet_name):
    return jsonify(cg.get_pet_data(pet_name))    

@app.route("/api/v1.0/pet_training")
def get_all_training():
    cur_args = request.args
    if len(cur_args) == 0:
        return jsonify(cg.get_pet_training_data())
    else:
        args_dict = { key: value for key, value in cur_args.items()}
        print("args_dict\n", args_dict)
        return jsonify(cg.get_pet_training_orm(args_dict))


@app.route("/api/v1.0/pet_training/<pet_name>")
def get_one_training(pet_name):
    return jsonify(cg.get_pet_training_data(pet_name))


if __name__ == '__main__':
    app.run(threaded=True, port=5000)