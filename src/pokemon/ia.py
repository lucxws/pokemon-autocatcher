from PIL import Image
import imagehash
import sqlite3
import requests
import numpy as np

class PokemonIA:
    def __init__(self, database_path):
        self.database_path = database_path
        
        self.connect = self.__connect__()
        self.cursor = self.__cursor__()
    
    def __connect__(self):
        return sqlite3.connect(self.database_path)
    
    def __cursor__(self):
        return self.connect.cursor()
    
    def close_connection(self):
        return self.connect.close()
    
    def search_pokemon_name(self, hashes):
        self.cursor.execute(f"""
        SELECT "pokemon_name", "pokemon_name_it", "pokemon_name_es", "pokemon_name_de", "pokemon_name_fr", "pokemon_name_cn", "pokemon_name_kr", "pokemon_name_jp"
        FROM "Pokemon#8738"
        WHERE image_hashes = '{hashes}';
        """)
        __names__ = self.cursor.fetchall()
        return __names__

    def get_hashes(self, image):
        img = Image.open(requests.get(image, stream=True).raw)
        arr = np.array(img)
        arr[arr[:, :, 3] == 0] = 0
        img = Image.fromarray(arr).convert('RGB')    
        return imagehash.phash(img)
    
    def add_pokemon(self, num, image_hashes, name, name_it, name_es, name_de, name_fr, name_cn, name_kr, name_jp):
        self.cursor.execute(f"""
        INSERT INTO "Pokemon#8738" (id, image_hashes, pokemon_name, pokemon_name_it, pokemon_name_es, pokemon_name_de, pokemon_name_fr, pokemon_name_cn, pokemon_name_kr, pokemon_name_jp)
        VALUES ('{num}','{image_hashes}', '{name}', '{name_it}', '{name_es}', '{name_de}', '{name_fr}', '{name_cn}', '{name_kr}', '{name_jp}');
        """)
        self.connect.commit()
    
    def get_by_id(self, id):
        self.cursor.execute("SELECT pokemon_name FROM 'Pokemon#8738' WHERE id = '{}'".format(id))
        return self.cursor.fetchone()[0]
         
    
    def recognize_pokemon(self, hashes, name_type):  

        __names__ = self.search_pokemon_name(hashes)
        
        name_dict = {
            "base": __names__[0][0],
            "italian": __names__[0][1],
            "spanish": __names__[0][2],
            "german": __names__[0][3],
            "french": __names__[0][4],
            "chinese": __names__[0][5],
            "korean": __names__[0][6],
            "japanese": __names__[0][7]
        }
        
        desired_name = name_dict.get(name_type)
        if not desired_name:
            desired_name = name_dict.get("base")
        return desired_name

    def get_information(self, hashes):
        
        self.cursor.execute(f"""
        SELECT * FROM "Pokemon#8738"
        WHERE image_hashes = '{hashes}';
        """)
        __information__ = self.cursor.fetchall()
        return __information__
        
        
