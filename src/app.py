from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

from config import config
from validaciones import *

app = Flask(__name__)
app.json.sort_keys = False

conexion = MySQL(app)

@app.route('/')
def index():
    return "PokeAPI"

def read_pokemon_id(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id FROM pokemons WHERE id = '{0}';".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            pokemon = {'N° Pokedex':datos[0]}
            return pokemon
        else:
            return None
    except Exception as ex:
        raise ex
    
def delete_pokemon_moves(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM moves_pokemons WHERE pokemon_id = '{0}';".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
    except Exception as ex:
        raise ex

@app.route('/Moves_List', methods = ['GET'])
def moves_list():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, name, type, power, accuracy FROM moves;"
        cursor.execute(sql)
        datos=cursor.fetchall()
        movimientos = []
        for fila in datos:
            movimiento = {'ID':fila[0], 'Move Name':fila[1], 'Type':fila[2], 'Power':fila[3], 'Accuracy':fila[4]}
            movimientos.append(movimiento)
        return jsonify({'Movimientos':movimientos,'mensaje':"Movimientos Listados"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

# Primer Endpoint
@app.route('/Pokemon_List', methods = ['GET'])
def pokemon_list():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id, name FROM pokemons;"
        cursor.execute(sql)
        datos=cursor.fetchall()
        pokemons = []
        for fila in datos:
            pokemon = {'N° Pokedex':fila[0], 'Name':fila[1]}
            pokemons.append(pokemon)
        return jsonify({'Pokemons':pokemons,'mensaje':"Pokemons Listados"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

# Segundo Endpoint
@app.route('/Pokemon_Info/<id>', methods = ['GET'])
def pokemon_info(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM pokemons WHERE id = '{0}'".format(id)
        sql2 = """SELECT moves.id, moves.name, moves.type, moves.power, moves.accuracy FROM pokemons, moves, moves_pokemons 
                    WHERE pokemons.id = moves_pokemons.pokemon_id AND moves.id = moves_pokemons.move_id AND pokemons.id = '{0}';""".format(id)
        cursor.execute(sql)
        datos=cursor.fetchone()
        cursor.execute(sql2)
        datos2=cursor.fetchall()
        movimientos = []
        if datos != None:
            pokemon = {'N° Pokedex':datos[0], 'Type 1': datos[1], 'Type 2': datos[2], 'Name':datos[3], 
                       'Description':datos[4], 'Weight':datos[5], 'Height':datos[6], 'Mega Evolves':datos[7], 'Evolves':datos[8]}
            for fila in datos2:
                movimiento = {'ID Move':fila[0],'Name':fila[1], 'Type':fila[2], 'Power':fila[3], 'Accuracy':fila[4]}
                movimientos.append(movimiento)
            return jsonify({'Pokemon':pokemon, 'Movimientos':movimientos, 'mensaje':"Pokemon encontrado"})
        else:
            return jsonify({'mensaje':"Pokemon no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})

# Endpoints de Actualización
@app.route('/Pokemon_Update/<id>/types', methods = ['PUT'])
def pokemon_udate_types(id):
    if (validar_strings(request.json['type_1']) and validar_strings(request.json['type_2'])):
        try:
            type1 = request.json['type_1']
            type2 = request.json['type_2']
            if type1 == type2:
                return jsonify({'mensaje':"Un Pokemon no puede tener 2 tipos iguales"})
            else:
                pokemon = read_pokemon_id(id)
                if pokemon != None:
                    cursor = conexion.connection.cursor()
                    sql = "UPDATE pokemons SET type_1 = '{0}', type_2 = '{1}' WHERE id = '{2}';".format(request.json['type_1'], request.json['type_2'], id)
                    cursor.execute(sql)
                    conexion.connection.commit()
                    return jsonify({'mensaje':"Pokemon actualizado en la Pokedex"}, pokemon)
                else:
                    return jsonify({'mensaje':"Pokemon no encontrado"})
        except Exception as ex:
            return jsonify({'mensaje':"Error"})
    else:
        return jsonify({'mensaje':"Parámetros inválidos"})

@app.route('/Pokemon_Update/<id>/height', methods = ['PUT'])
def pokemon_update_height(id):
    if (validar_int(request.json['height'])):
        try:
            pokemon = read_pokemon_id(id)
            if pokemon != None:
                cursor = conexion.connection.cursor()
                sql = "UPDATE pokemons SET height = '{0}' WHERE id = '{1}';".format(request.json['height'], id)
                cursor.execute(sql)
                conexion.connection.commit()
                return jsonify({'mensaje':"Pokemon actualizado en la Pokedex"}, pokemon)
            else:
                return jsonify({'mensaje':"Pokemon no encontrado"})
        except Exception as ex:
            return jsonify({'mensaje':"Error"})
    else:
        return jsonify({'mensaje':"Parámetros inválidos"})
    
@app.route('/Pokemon_Update/<id>/weight', methods = ['PUT'])
def pokemon_update_weight(id):
    if (validar_float(request.json['weight'])):
        try:
            pokemon = read_pokemon_id(id)
            if pokemon != None:
                cursor = conexion.connection.cursor()
                sql = "UPDATE pokemons SET weight = '{0}' WHERE id = '{1}';".format(request.json['weight'], id)
                cursor.execute(sql)
                conexion.connection.commit()
                return jsonify({'mensaje':"Pokemon actualizado en la Pokedex"}, pokemon)
            else:
                return jsonify({'mensaje':"Pokemon no encontrado"})
        except Exception as ex:
            return jsonify({'mensaje':"Error"})
    else:
        return jsonify({'mensaje':"Parámetros inválidos"})
    
@app.route('/Pokemon_Update/<id>/add_moves', methods = ['POST'])
def pokemon_add_moves(id):
    if (validar_int(request.json['move_id'])):
        try:
            pokemon = read_pokemon_id(id)
            if pokemon != None:
                cursor = conexion.connection.cursor()
                sql = "INSERT INTO moves_pokemons (move_id, pokemon_id) VALUES ({0}, {1});".format(request.json['move_id'], id)
                cursor.execute(sql)
                conexion.connection.commit()
                return jsonify({'mensaje':"Pokemon actualizado en la Pokedex"}, pokemon)
            else:
                return jsonify({'mensaje':"Pokemon no encontrado"})
        except Exception as ex:
            return jsonify({'mensaje':"Error"})
    else:
        return jsonify({'mensaje':"Parámetros inválidos"})
    
@app.route('/Pokemon_Update/<id>/remove_moves/<move_id>', methods = ['DELETE'])
def pokemon_remove_moves(id, move_id):
    try:
        pokemon = read_pokemon_id(id)
        if pokemon != None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM moves_pokemons WHERE pokemon_id = '{0}' AND move_id = '{1}';".format(id,move_id)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje':"Pokemon actualizado en la Pokedex"}, pokemon)
        else:
            return jsonify({'mensaje':"Pokemon no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})
    
@app.route('/Pokemon_Update/<id>/update_moves/<move_id>', methods = ['PUT'])
def pokemon_update_moves(id,move_id):
    if (validar_int(request.json['move_id'])):
        try:
            pokemon = read_pokemon_id(id)
            if pokemon != None:
                cursor = conexion.connection.cursor()
                sql = "UPDATE moves_pokemons SET move_id = '{0}' WHERE pokemon_id = '{1}' AND move_id = '{2}';".format(request.json['move_id'], id, move_id)
                cursor.execute(sql)
                conexion.connection.commit()
                return jsonify({'mensaje':"Pokemon actualizado en la Pokedex"}, pokemon)
            else:
                return jsonify({'mensaje':"Pokemon no encontrado"})
        except Exception as ex:
            return jsonify({'mensaje':"Error"})
    else:
            return jsonify({'mensaje':"Parámetros inválidos"})

# Endpoints de Eliminacion y Creacion
@app.route('/Pokemon_Register', methods = ['POST'])
def pokemon_registration():
    if (validar_strings(request.json['type_1']) and validar_strings(request.json['type_2']) and 
        validar_strings(request.json['name']) and validar_strings(request.json['description']) and 
        validar_float(request.json['weight']) and validar_int(request.json['height']) and
        validar_int(request.json['mega_evolves']) and validar_int(request.json['evolves'])):
        try:
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO pokemons (type_1, type_2, name, description, weight, height, mega_evolves, evolves) 
                        VALUES ('{0}', '{1}', '{2}', '{3}', {4}, {5}, {6}, {7});""".format(request.json['type_1'], request.json['type_2'], 
                                                                                            request.json['name'], request.json['description'], 
                                                                                            request.json['weight'], request.json['height'], 
                                                                                            request.json['mega_evolves'], request.json['evolves'])
            sql2 = "SELECT id FROM pokemons ORDER BY id DESC LIMIT 1"
            cursor.execute(sql)
            conexion.connection.commit()
            cursor.execute(sql2)
            datos = cursor.fetchone()
            pokemon = {'N° Pokedex':datos[0]}
            return jsonify({'mensaje':"Pokemon registrado en la Pokedex"}, pokemon)
        except Exception as ex:
            return jsonify({'mensaje':"Error"})
    else:
        return jsonify({'mensaje':"Parámetros inválidos"})
    
@app.route('/Pokemon_Elimination/<id>', methods = ['DELETE'])
def pokemon_Elimination(id):
    try:
        pokemon = read_pokemon_id(id)
        if pokemon != None:
            cursor = conexion.connection.cursor()
            delete_pokemon_moves(id)
            sql = "DELETE FROM pokemons WHERE id = '{0}';".format(id)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje':"Pokemon eliminado de la Pokedex"}, pokemon)
        else:
            return jsonify({'mensaje':"Pokemon no encontrado en la Pokedex"})
    except Exception as ex:
        return jsonify({'mensaje':"Error"})


def page_not_found(error):
    return "<h1>La página no existe</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,page_not_found)
    app.run()