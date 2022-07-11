from flask import Flask, render_template, request
import urllib.request, json
import urllib.parse
import os
import numpy as np
import pandas as pd
from slugify import slugify

app = Flask(__name__)

# api_key
api_key = "8e4f40d4f020b0f1e3ae3b35dbe2a179"

# Load matrix cosine similarity
root_fearure_path = "static/feature/feature.npz"

data = np.load(root_fearure_path, allow_pickle=True)

# 'tfidf', 'info', 'embedding', 'hidden_state', 'all'

tfidf = data["tfidf"]
info = data["info"]
embedding = data["embedding"]
hidden_state = data["hidden_state"]
all_sim = data["all_sim"]


data = pd.read_csv("static/feature/data.csv")

indices = pd.Series(data.index, index=data['title']).drop_duplicates()

def get_recommendations(title, cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:10]
    movie_indices = [i[0] for i in sim_scores]
    return data['title'].iloc[movie_indices]

# Chạy model để vectorization ... => lưu file .npz

# Input: search => tên bộ phim => check tên bộ phim trong excel

# Xu li: lấy tên bộ phim => đọc các trường dữ liệu của bộ phim đó => thả vảo model => so sánh với các trường trong file npz
# Trả về list top 10 bộ phim
# Call Api (thả list 10 bộ phim) => Lấy bộ phim đầu tiên xuất hiện

# Output
# Poster, tên bộ phim, description, 

def search_movie(search, api_key = "8e4f40d4f020b0f1e3ae3b35dbe2a179"):
    url = f"https://api.themoviedb.org/3/search/multi?api_key={api_key}&query={search}"
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    check_results = dict["results"]
    results = []
    
    for result in check_results:
        try:
            if (result['poster_path'] != None) and (result['title'] != None):
                results.append(result)
        except:
            continue
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search = request.form['input_search']
        titleb = slugify(search, separator='%20')
        results = search_movie(titleb)
        
        # Recommendation
        result = results[0]
        title_movie = result['title']
        
        list_rec = get_recommendations(title_movie, embedding)
        results_rec = []
        for title in list_rec:
            # Convert String To URL with '%'
            titlea = slugify(title, separator='%20')
            abc = search_movie(titlea)
            results_rec.append(abc[0])
            
        print(results_rec)

        return render_template ("index.html", movies=results, movies2 = results_rec)
    else:
        return render_template("index.html")
    

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)