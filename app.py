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

data_feature = np.load(root_fearure_path, allow_pickle=True)

features = ['tfidf', 'hidden_state', 'all_sim']

# tfidf = data_feature["tfidf"]
# info = data_feature["info"]
# embedding = data_feature["embedding"]
# hidden_state = data_feature["hidden_state"]
# all_sim = data_feature["all_sim"]


data = pd.read_csv("static/feature/data.csv")

indices = pd.Series(data.index, index=data['title']).drop_duplicates()

def get_recommendations(title, cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:10]
    movie_indices = [i[0] for i in sim_scores]
    return data['title'].iloc[movie_indices]



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
        # Get search content from form input
        search_content = request.form['input_search']
        
        result = dict()
        try:
            # Preprocess search content (convert string to url)
            search_content = slugify(search_content, separator='%20')
            
            # Search
            results = search_movie(search_content)
            
            # Get first result
            result = results[0]
            
            # Get title
            title_movie = result['title']
            
            total_result = []
            for feature in features:
                # Get list titles movie from recommendation
                title_movies_recommend = get_recommendations(title_movie, data_feature[feature])
                
                results_recommend = []
                for title_movie in title_movies_recommend:
                    # Preprocess search content (convert string to url)
                    title = slugify(title_movie, separator='%20')
                    result_recommend = search_movie(title)
                    if result_recommend != []:
                        results_recommend.append(result_recommend[0])
                    else:
                        continue
                total_result.append(results_recommend)
            return render_template ("index.html", movie=result, tfidf = total_result[0],
                                    hidden_state = total_result[1], all_sim= total_result[2])
        except:
            print("Khong tim thay")
            
            return render_template("index.html")
            
    else:
        return render_template("index.html")
    

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)
    
# Chạy model để vectorization ... => lưu file .npz

# Input: search => tên bộ phim => check tên bộ phim trong excel

# Xu li: lấy tên bộ phim => đọc các trường dữ liệu của bộ phim đó => thả vảo model => so sánh với các trường trong file npz
# Trả về list top 10 bộ phim
# Call Api (thả list 10 bộ phim) => Lấy bộ phim đầu tiên xuất hiện

# Output
# Poster, tên bộ phim, description, 