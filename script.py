import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# ========== SETTINGS ==========
# Ensure this is a fresh token. If it's old, you need to re-run the /login request.
TVDB_TOKEN = "YOUR_TVDB_TOKEN_HERE"
def get_gender(g):
    if g in [1, "Female", "female"]: return "♀️"
    if g in [2, "Male", "male"]: return "♂️"
    return ""

# ========== TVMAZE LOGIC ==========
def get_tvmaze_data(query, s, e):
    try:
        search = requests.get(f"https://api.tvmaze.com/singlesearch/shows?q={query}").json()
        if not search: return None
        show_id = search['id']
        
        ep_url = f"https://api.tvmaze.com/shows/{show_id}/episodebynumber?season={s}&number={e}&embed=guestcast"
        ep_data = requests.get(ep_url).json()
        
        cast = []
        for item in ep_data.get('_embedded', {}).get('guestcast', []):
            cast.append({"name": item['person']['name'], "char": item['character']['name'], "type": "Guest"})
        
        main_cast_data = requests.get(f"https://api.tvmaze.com/shows/{show_id}/cast").json()
        for item in main_cast_data[:10]:
            cast.append({"name": item['person']['name'], "char": item['character']['name'], "type": "Regular"})

        return {"source": "TVmaze", "title": ep_data.get('name'), "overview": ep_data.get('summary', ''), "cast": cast}
    except Exception as err:
        print(f"TVmaze Error: {err}")
        return None

# ========== THETVDB LOGIC (FIXED) ==========
def get_tvdb_data(query, s, e):
    headers = {"Authorization": f"Bearer {TVDB_TOKEN}", "accept": "application/json"}
    try:
        # 1. Search for the Series ID
        search_res = requests.get(f"https://api4.thetvdb.com/v4/search?q={query}&type=series", headers=headers).json()
        if not search_res.get('data'): return None
        series_id = search_res['data'][0]['tvdb_id']

        # 2. Get Episode ID by Season/Number
        # Note: We use the 'episodes/default' endpoint which is more reliable
        episodes_res = requests.get(f"https://api4.thetvdb.com/v4/series/{series_id}/episodes/default?season={s}", headers=headers).json()
        
        ep_id = None
        for ep in episodes_res.get('data', {}).get('episodes', []):
            if str(ep['number']) == str(e):
                ep_id = ep['id']
                break
        
        if not ep_id: return None

        # 3. Get Extended Episode Info (Actors)
        data = requests.get(f"https://api4.thetvdb.com/v4/episodes/{ep_id}/extended", headers=headers).json()
        ep_info = data.get('data', {})
        
        cast = []
        for char in ep_info.get('characters', []):
            gender = get_gender(char.get('personGender'))
            cast.append({"name": f"{char['personName']} {gender}", "char": char['name'], "type": "Actor"})

        return {"source": "TheTVDB", "title": ep_info.get('name'), "overview": ep_info.get('overview'), "cast": cast}
    except Exception as err:
        print(f"TheTVDB Error: {err}")
        return None

# ========== TEMPLATE & ROUTES (SAME AS BEFORE) ==========
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>{{ data.source }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light p-5">
    <div class="container bg-white p-4 shadow-sm rounded">
        <h1>{{ data.source }} Results</h1><hr>
        <h3>{{ data.title }}</h3>
        <div class="mb-3">{{ data.overview | safe }}</div>
        <h4>Characters:</h4>
        <ul class="list-group">
            {% for p in data.cast %}
            <li class="list-group-item d-flex justify-content-between">
                <span><strong>{{ p.name }}</strong></span>
                <span class="text-muted">{{ p.char }}</span>
            </li>
            {% endfor %}
        </ul>
        <br><a href="/" class="btn btn-secondary">Back</a>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return '''
    <div style="padding: 50px; font-family: sans-serif;">
        <h2>Compare APIs</h2>
        <form action="/compare" method="get">
            <input name="query" value="Breaking Bad" style="padding: 8px;">
            <input name="s" value="1" style="width: 50px; padding: 8px;">
            <input name="e" value="4" style="width: 50px; padding: 8px;">
            <button name="api" value="tvmaze" style="background: green; color: white; padding: 10px;">TVmaze</button>
            <button name="api" value="tvdb" style="background: blue; color: white; padding: 10px;">TheTVDB</button>
        </form>
    </div>
    '''

@app.route('/compare')
def compare():
    api = request.args.get('api')
    q = request.args.get('query')
    s = request.args.get('s')
    e = request.args.get('e')
    data = get_tvmaze_data(q, s, e) if api == 'tvmaze' else get_tvdb_data(q, s, e)
    if not data: return "<h3>Error: Data not found. Check your TheTVDB Token or the Show Name.</h3><a href='/'>Try again</a>"
    return render_template_string(HTML, data=data)

if __name__ == "__main__":
    app.run(debug=True)