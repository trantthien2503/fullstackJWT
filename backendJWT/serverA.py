from flask import Flask, jsonify, request
import secrets
import requests
import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_cors import CORS

from firebase_service import FirestoreCollection

app = Flask(__name__)
CORS(app, support_credentials=True)

secret_key = secrets.token_urlsafe(32)  # Tạo khóa bí mật ngẫu nhiên
app.config['JWT_SECRET_KEY'] = secret_key  # Khóa bí mật cho JWT
jwt = JWTManager(app)
# Địa chỉ của ServerB
SERVERB_URL = 'http://127.0.0.1:5001'  # Thay đổi theo địa chỉ thật của ServerB

# Tạo access token và refresh token khi xác thực thành công
@app.route('/login', methods=['POST'])
def login():
    username = request.get_json().get('username')
    password = request.get_json().get('password')
    # Xác thực username và password (giả sử bạn có hệ thống xác thực riêng)
    if username == 'admin' and password == 'password':
        # Thiết lập payload cho access token
        access_token_payload = {'username': username, 'role': 'admin'}
        # Thiết lập payload cho refresh token
        refresh_token_payload = {'username': username}
        access_token_expires = datetime.timedelta(minutes=15)  # Thời gian hết hạn: 15 phút
        access_token = create_access_token(identity=username, additional_claims=access_token_payload, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(identity=username, additional_claims=refresh_token_payload)
        token = {
            "username": username,
            "password": password,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        fire = FirestoreCollection("tokens")
        fire.add_data(token)
        return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200
    
    return jsonify({'message': 'Invalid username or password'}), 401

# Tuyến đường /protected
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Protected endpoint. Hello, {current_user}!'}), 200


# Tuyến đường /actors
@app.route('/actors', methods=['GET'])
@jwt_required()
def get_actors():
    # Gọi API từ ServerB để lấy danh sách diễn viên
    response = requests.get(f'{SERVERB_URL}/bactors')
    actors = response.json()

    # Trả về kết quả cho clientA
    return jsonify(actors), 200

# Tuyến đường /films
@app.route('/films', methods=['GET'])
@jwt_required()
def get_films():
    # Gọi API từ ServerB để lấy danh sách phim
    response = requests.get(f'{SERVERB_URL}/bfilms')
    films = response.json()

    # Trả về kết quả cho clientA
    return jsonify(films), 200
if __name__ == '__main__':
    app.run(port=5000)