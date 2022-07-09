from flask import Flask, render_template, request
import urllib.request, json
import os

app = Flask(__name__)

api_key = "8e4f40d4f020b0f1e3ae3b35dbe2a179"

import urllib.parse

# String
query = 'con khi'

# Convert String To URL
url = urllib.parse.quote_plus(query)

# Print
print(url)

# Chạy model để vectorization ... => lưu file .npz

# Input: search => tên bộ phim => check tên bộ phim trong excel

# Xu li: lấy tên bộ phim => đọc các trường dữ liệu của bộ phim đó => thả vảo model => so sánh với các trường trong file npz
# Trả về list top 10 bộ phim
# Call Api (thả list 10 bộ phim) => Lấy bộ phim đầu tiên xuất hiện

# Output
# Poster, tên bộ phim, description, 


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search = request.form['input_search']
        api_key = "8e4f40d4f020b0f1e3ae3b35dbe2a179"
        url = f"https://api.themoviedb.org/3/search/multi?api_key={api_key}&query={search}"

        response = urllib.request.urlopen(url)
        data = response.read()
        dict = json.loads(data)
        # print(dict)
        check_results = dict["results"]
        results = []
        
        for result in check_results:
            try:
                if (result['backdrop_path'] != None) and (result['title'] != None):
                    results.append(result)
            except:
                continue


        return render_template ("index.html", movies=results)
    else:
        return render_template("index.html")
    

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)