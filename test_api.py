import requests
import pytest

BASE_URL = "http://127.0.0.1:5000"

def test_api_is_running():

    response = requests.get(f"{BASE_URL}/movies?limit=1")
    assert response.status_code == 200

def test_search_movie_titanic():
    response = requests.get(f"{BASE_URL}/search/movies/titanic")
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
    assert len(data) > 0
    assert "Titanic" in data[0]['name']

def test_get_movie_by_id():
    """Cherche un film, récupère son ID, et teste la route /movies/{id}"""
    # 1. On cherche d'abord un film pour avoir un ID valide
    search = requests.get(f"{BASE_URL}/search/movies/m")
    movie_id = search.json()[0]['index']
    
    # 2. On teste la route spécifique avec cet ID
    response = requests.get(f"{BASE_URL}/movies/{movie_id}")
    assert response.status_code == 200
    movie_data = response.json()
    
    # 3. Vérifications
    assert movie_data['name'] == search.json()[0]['name']
    assert 'actors' in movie_data
    assert isinstance(movie_data['actors'], list)

def test_search_actor_dujardin():
    """Vérifie la recherche d'acteur"""
    response = requests.get(f"{BASE_URL}/search/actors/dujardin")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "Jean Dujardin" in [d['name'] for d in data]

def test_distance_connue():
    """Vérifie le calcul de distance entre deux acteurs connus"""
    # On récupère les IDs de Kevin Bacon et Jean Dujardin
    res_bacon = requests.get(f"{BASE_URL}/search/actors/Kevin Bacon").json()
    res_jean = requests.get(f"{BASE_URL}/search/actors/Jean Dujardin").json()
    
    id_bacon = res_bacon[0]['index']
    id_jean = res_jean[0]['index']
    
    # On demande la distance
    response = requests.get(f"{BASE_URL}/actors/{id_bacon}/distance/{id_jean}")
    assert response.status_code == 200
    data = response.json()
    
    # La réponse doit être une liste [distance, [chemin]]
    assert isinstance(data, list)
    assert len(data) == 2
    
    distance = data[0]
    path = data[1]
    
    # On sait que la distance est > 0 (généralement 2)
    assert isinstance(distance, int)
    assert distance > 0
    assert len(path) > 1

def test_pagination():
    """Vérifie que les paramètres limit et start fonctionnent"""
    # On demande 5 acteurs
    response = requests.get(f"{BASE_URL}/actors?limit=5")
    data = response.json()
    assert len(data) == 5