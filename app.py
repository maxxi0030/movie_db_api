import requests
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# ========== НАСТРОЙКИ ==========
API_KEY = "YOUR_TMDB_API_KEY_HERE"  # Получите ключ на https://www.themoviedb.org/settings/api
BASE_URL = "https://api.themoviedb.org/3"

def get_gender_emoji(gender_id):
    if gender_id == 1:
        return "♀️"
    elif gender_id == 2:
        return "♂️"
    return ""

def search_content(query):
    """Ищет фильм или сериал и возвращает ID и тип контента"""
    url = f"{BASE_URL}/search/multi"
    params = {"api_key": API_KEY, "query": query, "language": "en-US"}
    res = requests.get(url, params=params).json()
    
    if res.get("results"):
        result = res["results"][0]
        return result["id"], result["media_type"] # 'movie' или 'tv'
    return None, None

def get_movie_data(m_id):
    url = f"{BASE_URL}/movie/{m_id}"
    params = {"api_key": API_KEY, "append_to_response": "credits", "language": "en-US"}
    data = requests.get(url, params=params).json()
    
    cast = []
    for actor in data.get("credits", {}).get("cast", []):
        gender = get_gender_emoji(actor.get("gender"))
        cast.append({"name": f"{actor['name']} {gender}", "char": actor["character"]})
        
    return {
        "type": "Movie",
        "title": data.get("title"),
        "overview": data.get("overview"),
        "cast": cast,
        "image": f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get("poster_path") else None
    }

def get_tv_data(s_id, s_num, e_num):
    url = f"{BASE_URL}/tv/{s_id}/season/{s_num}/episode/{e_num}"
    params = {"api_key": API_KEY, "append_to_response": "credits", "language": "en-US"}
    data = requests.get(url, params=params).json()
    
    if "name" not in data: return None
    
    cast = []
    # Объединяем приглашенных и основных актеров серии
    all_actors = data.get("credits", {}).get("guest_stars", []) + data.get("credits", {}).get("cast", [])
    
    for actor in all_actors:
        gender = get_gender_emoji(actor.get("gender"))
        cast.append({"name": f"{actor['name']} {gender}", "char": actor["character"]})
        
    return {
        "type": "TV Episode",
        "title": data.get("name"),
        "overview": data.get("overview"),
        "cast": cast,
        "image": f"https://image.tmdb.org/t/p/w500{data.get('still_path')}" if data.get("still_path") else None
    }

# ========== HTML ИНТЕРФЕЙС ==========
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Media Search</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f4f9; padding-top: 50px; }
        .result-card { background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); overflow: hidden; }
        .cast-list { max-height: 400px; overflow-y: auto; }
    </style>
</head>
<body>
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card p-4 mb-4">
                <h3 class="text-center mb-4">Search Movie or TV Show</h3>
                <form action="/search" method="get">
                    <div class="mb-3">
                        <label>Title</label>
                        <input type="text" name="query" class="form-control" placeholder="Breaking Bad or Inception" required>
                    </div>
                    <div class="row">
                        <div class="col">
                            <label>Season (for TV)</label>
                            <input type="number" name="s" class="form-control" value="1">
                        </div>
                        <div class="col">
                            <label>Episode (for TV)</label>
                            <input type="number" name="e" class="form-control" value="1">
                        </div>
                    </div>
                    <button type="submit" class="btn btn-dark w-100 mt-4">Search</button>
                </form>
            </div>

            {% if data %}
            <div class="result-card p-4">
                <div class="row">
                    <div class="col-md-4">
                        {% if data.image %}
                        <img src="{{ data.image }}" class="img-fluid rounded" alt="poster">
                        {% endif %}
                    </div>
                    <div class="col-md-8">
                        <span class="badge bg-primary mb-2">{{ data.type }}</span>
                        <h2>{{ data.title }}</h2>
                        <p class="mt-3"><strong>Overview:</strong> {{ data.overview }}</p>
                    </div>
                </div>
                <hr>
                <h5>Characters / Cast</h5>
                <div class="cast-list list-group list-group-flush">
                    {% for person in data.cast %}
                    <div class="list-group-item d-flex justify-content-between">
                        <span>{{ person.name }}</span>
                        <span class="text-muted small">{{ person.char }}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
        </div>
    </div>
</div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/search')
def search():
    query = request.args.get('query')
    s = request.args.get('s', 1)
    e = request.args.get('e', 1)
    
    content_id, media_type = search_content(query)
    
    if not content_id:
        return "Not found", 404
    
    if media_type == "movie":
        result_data = get_movie_data(content_id)
    else:
        result_data = get_tv_data(content_id, s, e)
        
    if not result_data:
        return "Details not found", 404
    
    return render_template_string(HTML_TEMPLATE, data=result_data)

if __name__ == "__main__":
    app.run(debug=True)