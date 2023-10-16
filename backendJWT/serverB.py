from flask import Flask, jsonify

app = Flask(__name__)

# Tuyến đường /bactors
@app.route('/bactors', methods=['GET'])
def get_bactors():
    # Xử lý yêu cầu API để lấy danh sách diễn viên
    actors = [
        {'name': 'Actor 1', 'age': 30},
        {'name': 'Actor 2', 'age': 35},
        {'name': 'Actor 3', 'age': 40}
    ]

    # Trả về kết quả danh sách diễn viên cho ServerA
    return jsonify(actors), 200

# Tuyến đường /bfilms
@app.route('/bfilms', methods=['GET'])
def get_bfilms():
    # Xử lý yêu cầu API để lấy danh sách phim
    films = [
        {'title': 'Film 1', 'year': 2010},
        {'title': 'Film 2', 'year': 2015},
        {'title': 'Film 3', 'year': 2020}
    ]

    # Trả về kết quả danh sách phim cho ServerA
    return jsonify(films), 200

if __name__ == '__main__':
    app.run(port=5001)