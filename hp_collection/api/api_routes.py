from flask import Blueprint, request, jsonify
from hp_collection.helpers import token_required
from hp_collection.models import db, Character, character_schema, characters_schema

api = Blueprint('api', __name__, url_prefix='/api')

# Create Character Endpoint
@api.route('/characters', methods = ['POST'])
@token_required
def create_book(our_user):

    name = request.json['name']
    description = request.json['description']
    house = request.json['house']
    nationality = request.json['nationality']
    occupation = request.json['occupation']
    books_appeared_in = request.json['books_appeared_in']
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    character = Character(name, description, house, nationality, occupation,
                          books_appeared_in, user_token)
    
    # add the character and commit it to the database

    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)      

    return jsonify(response)        # have to jsonify things you get from AND push to API request

#Read 1 Single Character Endpoint
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_character(our_user, id):
    if id:
        character = Character.query.get(id)
        response = character_schema.dump(character)
        return jsonify(response)
    else:
        return jsonify({'message': 'ID is missing'}), 401
    

# Read all the Characters
@api.route('/characters', methods = ['GET'])
@token_required
def get_characters(our_user):
    token = our_user.token
    characters = Character.query.filter_by(user_token = token).all()
    response = characters_schema.dump(characters)

    return jsonify(response)

# Update 1 Character by ID
@api.route('/characters/<id>', methods = ['PUT'])
@token_required
def update_character(our_user, id):
    character = Character.query.get(id)

    character.name = request.json['name']
    character.description = request.json['description']
    character.house = request.json['house']
    character.nationality = request.json['nationality']
    character.occupation = request.json['occupation']
    character.books_appeared_in = request.json['books_appeared_in']
    character.user_token = our_user.token

    db.session.commit()

    response = character_schema.dump(character)

    return jsonify(response)


#Delete 1 Character by ID
@api.route('/characters/<id>', methods = ['DELETE'])
@token_required
def delete_character(our_user, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()

    response = character_schema.dump(character)

    return jsonify(response)