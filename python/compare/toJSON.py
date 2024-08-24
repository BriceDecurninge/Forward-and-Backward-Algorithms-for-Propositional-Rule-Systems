import json
import os

# from dictionary to JSON
# cf generate.py to see how the data is structured

def store(data, file) :

    # Serializing json
    json_object = json.dumps(data, indent=4, ensure_ascii=False)    
    
    # Writing to sample.json
    # Créer le chemin du fichier
    file_path = os.path.join(os.getcwd(), "compare", file + ".json")

    # Créer le répertoire si nécessaire
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Ouvrir le fichier en mode écriture (création s'il n'existe pas et écrasement s'il existe déjà)
    with open(file_path, "w+") as outfile:
        outfile.write(json_object)
    
    outfile.close() 

    return 