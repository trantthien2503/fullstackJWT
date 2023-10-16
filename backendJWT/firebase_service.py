import firebase_admin
from firebase_admin import credentials, db, firestore

import json

with open('flask-jwt-firebase-adminsdk-39lmg-cf6f910c00.json', 'r') as json_file:
    appsettings = json.load(json_file)

certificate = credentials.Certificate(appsettings)

firebaseApp = firebase_admin.initialize_app(
    certificate, {"databaseURL": appsettings['databaseURL']})

db = firestore.client()
class FirestoreCollection():
    def __init__(self, collection_name):
        self.collection = db.collection(collection_name)

    def get_all_data(self):
        try:
            collections = self.collection.get()
            collections_dict = []
            
            for doc in collections:
                collections_dict.append(doc.to_dict())
            
             # Thêm thông báo thành công
            response = {
            'data': collections_dict,
            'message': 'Lấy dữ liệu thành công'
            }
            return response
        except Exception as e:
            return {'message': f'Lỗi không xác định: {e}'} 

    def add_data(self, data):
        try:
            # Lấy id và thêm vào data
            doc_ref = self.collection.document()
            id = doc_ref.id
            data['id'] = id
            
            doc_ref.set(data)

            doc = doc_ref.get()
            doc_data = doc.to_dict()

            # Thêm thông báo thành công
            response = {
            'data': doc_data,
            'message': 'Thêm dữ liệu thành công'
            }

            return response

        except Exception as e:
            return {'message': f'Lỗi không xác định: {e}'}

    def add_multiple_data(self, data):
        try:
            for item in data:
                self.add_data(item)

            return {
                "data": True,
                "message": "Thêm nhiều dữ liệu thành công"
            }
        except Exception as e:
                return {'message': f'Lỗi không xác định: {e}'}

    def update_data(self, doc_id, updates):
        # Cập nhật dữ liệu trong collection
        try:    
            doc = self.collection.document(doc_id)

            doc.update(updates)

            response = {
            'data': True,
            'message': 'Cập nhật dữ liệu thành công'
            }
            return response

        except ValueError as e:
            return {'message': str(e)}

        except Exception as e:
            return {'message': f'Lỗi không xác định: {e}'}

    def delete_data(self, doc_id):
        try:
            # Kiểm tra đầu vào
            if not doc_id:
                raise ValueError("Vui lòng cung cấp id cần xóa")
            # Tạo query theo id    
            doc_ref = self.collection.document(doc_id)
            # Xóa document
            doc_ref.delete()
            response = {
            'data': True,
            'message': 'Xóa dữ liệu thành công'
            }
            return response
        except ValueError as err:
            return {'message': str(err)}
        except Exception as err:
            return {'message': f'Lỗi không xác định: {err}'}

    def search_data(self, field, value):
        # Hàm tìm kiếm dữ liệu theo trường và giá trị
        try:
             # Tạo query
            query = self.collection.order_by(field)
            # Truy vấn theo giá trị 
            query = query.where(field, '==', value)
            results = query.get()
            if not results:
              return []
            data = [doc.to_dict() for doc in results]

            response = {
            'data': data,
            'message': 'Tìm kiếm thành công'
            }
            return response
        except ValueError as err:
            return {'message': str(err)}

        except Exception as err:
            return {'message': f'Lỗi không xác định: {err}'}


    def registerUser(self, data):
        # Chỉ check trường hợp email đã tồn tại
        try:
            # Validate data
            email = data['email']
            search = self.search_data('email',email)
            if search:
                return {
                    "data": False,
                    'message': 'Email đã được đăng ký'  
                }
            doc_ref = self.collection.document(email).set(data)

            doc_ref = self.collection.document(email)
            doc = doc_ref.get()

            response = {
                "user": doc.to_dict(),
                "message": "Đăng ký thành công"
            }
            return response
        except Exception as err:
            return {'message': f'Lỗi: {err}'}
        

    def loginUser(self, data):

        try:
        
            # Validate data
            email = data['email']
            password = data['password']

            # Query document
            query = self.collection.where('email', '==', email).where('password', '==', password)
            doc = query.get() 
            
            if not doc:
                return {'message': 'Email hoặc mật khẩu không chính xác'}

            # Get user data
            user = doc[0].to_dict()

            response = {
            "user": user,  
            'message': 'Đăng nhập thành công'
            }

            return response

        except Exception as err:
            return {'message': f'Lỗi: {err}'}