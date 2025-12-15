# from pathlib import Path  
# from requests import Session
# import gzip

# base_url = "https://datasets.imdbws.com/"
# data_dir = Path.home() / "Downloads"
# def download_imdb(dest_file):
#     s = Session()
#     r = s.get(base_url, stream=True)
#     local_path = data_dir / dest_file
#     if local_path.exists():
#         print(f"{local_path} existe déjà. Téléchargement ignoré.")
#         return 
#     with open(local_path, "wb") as f:
#         r.raise_for_status()
#         for chunk in r.iter_content(chunk_size=8192):
#             if chunk: 
#                 f.write(chunk)

# files = ['title.principals.tsv.gz', 'name.basics.tsv.gz', 'title.basics.tsv.gz']
# for file in files:
#     download_imdb(file)



from pathlib import Path  
from requests import Session
import gzip

base_url = "https://datasets.imdbws.com/"
data_dir = Path.home() / "Downloads"

def download_imdb(dest_file):
    # --- CORRECTION ICI : Concaténer l'URL et le nom du fichier ---
    url_complete = base_url + dest_file 
    
    local_path = data_dir / dest_file
    
    if local_path.exists():
        print(f"{local_path} existe déjà. Téléchargement ignoré.")
        return 

    print(f"Démarrage du téléchargement : {dest_file} ...")
    
    s = Session()
    # On utilise url_complete ici, pas base_url
    with s.get(url_complete, stream=True) as r:
        r.raise_for_status() # Vérifie les erreurs HTTP (404, etc)
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: 
                    f.write(chunk)
    print(f"Téléchargement terminé pour : {dest_file}")

files = ['title.principals.tsv.gz', 'name.basics.tsv.gz', 'title.basics.tsv.gz']

# Assurez-vous d'avoir supprimé les anciens fichiers corrompus avant de lancer ceci !
for file in files:
    download_imdb(file)

# Test de lecture (une fois le téléchargement CORRECT terminé)

def explore(name):
    fichier = data_dir / name
    if fichier.exists():
            with gzip.open(fichier, 'rt', encoding='utf8') as f:
                print(f"4 First lines of {fichier.name} :")
                for _ in range(1200):
                    List = []
                    l = f.readline()
                    List.append(l.strip().split('\t')    )
                    print(List[0])


for file in files:
    explore(file)
