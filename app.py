from flask import Flask, render_template_string, request, redirect, url_for
import requests

app = Flask(__name__)

# URL de votre API (celle qui tourne dans le notebook sur le port 5000)
API_URL = "http://127.0.0.1:5000"

# --- TEMPLATE HTML MODERNE (THEME SOMBRE) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IMDB Explorer</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome pour les icônes -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {
            --imdb-yellow: #f5c518;
            --imdb-yellow-hover: #e3b616;
            --bg-dark: #121212;
            --card-bg: #1f1f1f;
        }
        
        body { 
            background-color: var(--bg-dark); 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding-bottom: 50px;
        }

        /* En-tête */
        .navbar-custom {
            background-color: #000;
            border-bottom: 1px solid #333;
            padding: 1rem 0;
            margin-bottom: 2rem;
        }
        .navbar-brand {
            font-weight: 900;
            color: var(--imdb-yellow) !important;
            font-size: 1.8rem;
            letter-spacing: 1px;
            text-transform: uppercase;
        }

        /* Cartes */
        .card {
            background-color: var(--card-bg);
            border: 1px solid #333;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            transition: transform 0.2s;
        }
        
        .card-header {
            background-color: rgba(255,255,255,0.05);
            border-bottom: 1px solid #333;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9rem;
            letter-spacing: 1px;
        }
        
        .card-header-icon {
            margin-right: 8px;
            color: var(--imdb-yellow);
        }

        /* Boutons personnalisés */
        .btn-imdb {
            background-color: var(--imdb-yellow);
            color: #000;
            font-weight: 700;
            border: none;
        }
        .btn-imdb:hover {
            background-color: var(--imdb-yellow-hover);
            color: #000;
        }

        .btn-outline-imdb {
            border: 1px solid var(--imdb-yellow);
            color: var(--imdb-yellow);
        }
        .btn-outline-imdb:hover {
            background-color: var(--imdb-yellow);
            color: #000;
        }

        /* Listes et Tableaux */
        .scrollable-list { 
            max-height: 500px; 
            overflow-y: auto; 
            scrollbar-width: thin;
            scrollbar-color: #444 #1f1f1f;
        }
        
        .table {
            --bs-table-bg: transparent;
            --bs-table-color: #ddd;
            font-size: 0.95rem;
        }
        .table-hover tbody tr:hover {
            color: #fff;
            background-color: rgba(245, 197, 24, 0.1);
        }

        /* Badges et Tags */
        .badge-movie {
            background-color: #333;
            border: 1px solid #555;
            color: #ccc;
            font-weight: normal;
            padding: 8px 12px;
            font-size: 0.9rem;
        }

        /* Section Distance */
        .distance-step {
            position: relative;
            padding-left: 20px;
            border-left: 2px solid var(--imdb-yellow);
            margin-left: 10px;
            padding-bottom: 20px;
        }
        .distance-step:last-child {
            border-left: none;
        }
        .distance-step::before {
            content: '';
            position: absolute;
            left: -6px;
            top: 0;
            width: 10px;
            height: 10px;
            background: var(--imdb-yellow);
            border-radius: 50%;
        }
    </style>
</head>
<body>

<!-- Navbar -->
<nav class="navbar navbar-custom sticky-top">
    <div class="container">
        <a class="navbar-brand" href="/">
            <i class="fas fa-film me-2"></i>IMDB Explorer
        </a>
        <div class="d-flex">
            <a href="/" class="btn btn-sm btn-outline-light"><i class="fas fa-home me-1"></i> Accueil</a>
        </div>
    </div>
</nav>

<div class="container">
    <div class="row">
        <!-- COLONNE GAUCHE : OUTILS -->
        <div class="col-lg-4 mb-4">
            
            <!-- Recherche Acteur -->
            <div class="card">
                <div class="card-header">
                    <i class="fas fa-search card-header-icon"></i> Recherche Acteur
                </div>
                <div class="card-body">
                    <form action="/search_actor" method="get">
                        <div class="input-group mb-3">
                            <span class="input-group-text bg-dark border-secondary text-secondary"><i class="fas fa-user"></i></span>
                            <input type="text" class="form-control bg-dark text-light border-secondary" name="name" placeholder="Ex: Jean Dujardin" required>
                        </div>
                        <button type="submit" class="btn btn-imdb w-100">Rechercher</button>
                    </form>
                </div>
            </div>

            <!-- Calcul Distance -->
            <div class="card">
                <div class="card-header">
                    <i class="fas fa-project-diagram card-header-icon"></i> Six Degrees
                </div>
                <div class="card-body">
                    <p class="text-muted small mb-3">Trouvez le lien entre deux acteurs.</p>
                    <form action="/distance" method="get">
                        <div class="mb-2">
                            <label class="form-label text-secondary small">Acteur de départ</label>
                            <input type="text" class="form-control bg-dark text-light border-secondary form-control-sm" name="actor1" placeholder="Ex: Kevin Bacon" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label text-secondary small">Acteur cible</label>
                            <input type="text" class="form-control bg-dark text-light border-secondary form-control-sm" name="actor2" placeholder="Ex: Tom Cruise" required>
                        </div>
                        <button type="submit" class="btn btn-outline-imdb w-100 btn-sm">
                            <i class="fas fa-calculator me-1"></i> Calculer la distance
                        </button>
                    </form>
                </div>
            </div>
            
            <!-- Résultats Recherche -->
            {% if search_results %}
            <div class="card border-primary">
                <div class="card-header text-primary">
                    <i class="fas fa-list card-header-icon"></i> Résultats
                </div>
                <div class="list-group list-group-flush">
                    {% for actor in search_results %}
                        <a href="/actor/{{ actor.index }}" class="list-group-item list-group-item-action bg-dark text-light border-secondary d-flex justify-content-between align-items-center">
                            {{ actor.name }}
                            <i class="fas fa-chevron-right text-muted small"></i>
                        </a>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            <!-- Résultats Distance -->
            {% if distance_data %}
            <div class="card border-warning">
                <div class="card-header text-warning">
                    <i class="fas fa-route card-header-icon"></i> Connexion : {{ distance_data[0] }} degrés
                </div>
                <div class="card-body">
                    {% if distance_data[0] == -1 %}
                        <div class="alert alert-danger mb-0">
                            <i class="fas fa-times-circle me-2"></i>Aucun lien trouvé.
                        </div>
                    {% else %}
                        <div class="mt-2">
                            {% for i in range(0, distance_data[1]|length, 2) %}
                                <div class="distance-step">
                                    <strong class="text-white">{{ distance_data[1][i] }}</strong>
                                    {% if i + 1 < distance_data[1]|length %}
                                        <div class="text-muted small mt-1">
                                            <i class="fas fa-film text-warning me-1"></i> {{ distance_data[1][i+1] }}
                                        </div>
                                    {% endif %}
                                </div>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
            </div>
            {% endif %}

        </div>

        <!-- COLONNE DROITE : CONTENU -->
        <div class="col-lg-8">
            
            <!-- Détails Acteur -->
            {% if actor_detail %}
            <div class="card mb-4 border-light">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <h2 class="card-title text-warning mb-0">{{ actor_detail.name }}</h2>
                        <a href="/" class="btn-close btn-close-white"></a>
                    </div>
                    <h6 class="text-muted mb-3">Filmographie ({{ actor_detail.movies|length }} titres)</h6>
                    <div class="d-flex flex-wrap gap-2">
                        {% for m in actor_detail.movies %}
                            <span class="badge-movie">
                                {{ m.name }} <span class="text-muted ms-1">({{ m.year }})</span>
                            </span>
                        {% endfor %}
                    </div>
                </div>
            </div>
            {% endif %}

            <!-- Tableaux Principaux -->
            <div class="card">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <span><i class="fas fa-database card-header-icon"></i> Base de Données</span>
                    {% if sort_order != 'name' %}
                        <a href="/?sort=name" class="btn btn-xs btn-outline-secondary" style="font-size: 0.7rem;">
                            <i class="fas fa-sort-alpha-down me-1"></i> Trier par Nom
                        </a>
                    {% else %}
                        <a href="/" class="btn btn-xs btn-secondary" style="font-size: 0.7rem;">
                            <i class="fas fa-undo me-1"></i> Reset Tri
                        </a>
                    {% endif %}
                </div>
                <div class="card-body p-0">
                    
                    <!-- Onglets -->
                    <ul class="nav nav-tabs nav-justified border-secondary" id="dbTabs" role="tablist">
                        <li class="nav-item" role="presentation">
                            <button class="nav-link active text-light rounded-0" id="movies-tab" data-bs-toggle="tab" data-bs-target="#movies" type="button">
                                <i class="fas fa-film me-2"></i>Films
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link text-light rounded-0" id="actors-tab" data-bs-toggle="tab" data-bs-target="#actors" type="button">
                                <i class="fas fa-users me-2"></i>Acteurs
                            </button>
                        </li>
                    </ul>

                    <div class="tab-content" id="dbTabsContent">
                        
                        <!-- Contenu Films -->
                        <div class="tab-pane fade show active" id="movies" role="tabpanel">
                            <div class="scrollable-list">
                                <table class="table table-hover mb-0 align-middle">
                                    <thead class="sticky-top bg-dark">
                                        <tr>
                                            <th class="ps-4">Titre</th>
                                            <th class="text-end pe-4">Année</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for m in movies_list %}
                                        <tr>
                                            <td class="ps-4 text-white">{{ m.name }}</td>
                                            <td class="text-end pe-4 text-secondary">{{ m.year }}</td>
                                        </tr>
                                        {% else %}
                                        <tr><td colspan="2" class="text-center p-4 text-muted">Aucune donnée chargée. Vérifiez l'API.</td></tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <!-- Contenu Acteurs -->
                        <div class="tab-pane fade" id="actors" role="tabpanel">
                            <div class="scrollable-list">
                                <table class="table table-hover mb-0 align-middle">
                                    <thead class="sticky-top bg-dark">
                                        <tr>
                                            <th class="ps-4">Nom</th>
                                            <th class="text-end pe-4">Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for a in actors_list %}
                                        <tr>
                                            <td class="ps-4 text-white">{{ a.name }}</td>
                                            <td class="text-end pe-4">
                                                <a href="/actor/{{ a.index }}" class="btn btn-sm btn-outline-info rounded-pill">
                                                    <i class="fas fa-eye"></i>
                                                </a>
                                            </td>
                                        </tr>
                                        {% else %}
                                        <tr><td colspan="2" class="text-center p-4 text-muted">Aucune donnée chargée. Vérifiez l'API.</td></tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                    </div>
                    
                    <!-- Pagination -->
                    <div class="card-footer bg-transparent border-top border-secondary py-3">
                        <div class="d-flex justify-content-between align-items-center">
                            <a href="/?start={{ start - 50 if start > 0 else 0 }}&sort={{ sort_order }}" 
                               class="btn btn-sm btn-outline-secondary {% if start == 0 %}disabled{% endif %}">
                                <i class="fas fa-chevron-left me-1"></i> Précédent
                            </a>
                            <span class="text-muted small">Éléments {{ start }} à {{ start + 50 }}</span>
                            <a href="/?start={{ start + 50 }}&sort={{ sort_order }}" 
                               class="btn btn-sm btn-outline-secondary">
                                Suivant <i class="fas fa-chevron-right ms-1"></i>
                            </a>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>
</div>

<!-- Scripts -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# --- ROUTES FLASK ---

@app.route("/")
def index():
    start = int(request.args.get("start", 0))
    limit = 50
    sort_order = request.args.get("sort", None)
    
    params = f"?start={start}&limit={limit}"
    if sort_order:
        params += f"&order={sort_order}"

    print(f"Tentative de connexion à: {API_URL}/movies{params}") 
    
    try:
        movies_resp = requests.get(f"{API_URL}/movies{params}")
        actors_resp = requests.get(f"{API_URL}/actors{params}")
        
        if movies_resp.status_code == 200:
            movies_list = movies_resp.json()
        else:
            print("ERREUR API FILMS:", movies_resp.status_code)
            movies_list = []

        if actors_resp.status_code == 200:
            actors_list = actors_resp.json()
        else:
            print("ERREUR API ACTEURS:", actors_resp.status_code)
            actors_list = []
            
    except Exception as e:
        print("ERREUR DE CONNEXION :", e)
        movies_list = []
        actors_list = []

    return render_template_string(HTML_TEMPLATE, 
                                  movies_list=movies_list, 
                                  actors_list=actors_list, 
                                  start=start,
                                  sort_order=sort_order)

@app.route("/search_actor")
def search_actor():
    name = request.args.get("name")
    results = []
    if name:
        try:
            resp = requests.get(f"{API_URL}/search/actors/{name}")
            results = resp.json()
        except:
            pass
    
    # On renvoie vers l'accueil mais avec des résultats de recherche
    # Note: On laisse les listes vides pour se concentrer sur la recherche
    return render_template_string(HTML_TEMPLATE, 
                                  search_results=results, 
                                  movies_list=[], actors_list=[], start=0, sort_order=None)

@app.route("/actor/<int:id>")
def get_actor_detail(id):
    try:
        resp = requests.get(f"{API_URL}/actors/{id}")
        actor_data = resp.json()
    except:
        actor_data = None
        
    return render_template_string(HTML_TEMPLATE, 
                                  actor_detail=actor_data,
                                  movies_list=[], actors_list=[], start=0, sort_order=None)

@app.route("/distance")
def compute_distance():
    name1 = request.args.get("actor1")
    name2 = request.args.get("actor2")
    distance_data = None
    
    try:
        search1 = requests.get(f"{API_URL}/search/actors/{name1}").json()
        search2 = requests.get(f"{API_URL}/search/actors/{name2}").json()
        
        if search1 and search2:
            id1 = search1[0]['index']
            id2 = search2[0]['index']
            
            resp = requests.get(f"{API_URL}/actors/{id1}/distance/{id2}")
            if resp.status_code == 200:
                distance_data = resp.json()
            else:
                 distance_data = [-1, []]
        else:
             distance_data = [-1, []]
            
    except Exception as e:
        print(e)
        distance_data = [-1, []]

    return render_template_string(HTML_TEMPLATE, 
                                  distance_data=distance_data,
                                  movies_list=[], actors_list=[], start=0, sort_order=None)

if __name__ == "__main__":
    print("Assurez-vous que l'API MP2 tourne sur le port 5000 !")
    # use_reloader=False est CRUCIAL dans un notebook
    app.run(port=5001, debug=True, use_reloader=False)