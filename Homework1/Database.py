        
from pymongo import MongoClient 


mongo_client = MongoClient("mongo")
db = mongo_client["cse312"]
user_collection = db["users"] 
user_collection_id = db["user_id"]
image_collection_id = db["image_id"]
chat_collection = db["chat"]
live_chat_collection = db["livechat"]
information_collection = db["information"]
user_token_collection = db["tokens"]


def get_new_id():
        id_object = user_collection_id.find_one({})
        if id_object:
                next_id = int(id_object['last_id']) + 1
                user_collection_id.update_one({},{'$set': {'last_id': next_id}})
                return next_id
        else:
                user_collection_id.insert_one({'last_id': 1})
                return 1

def get_new_image_id():
        id_object = image_collection_id.find_one({})
        if id_object:
                next_id = int(id_object['last_id']) + 1
                image_collection_id.update_one({},{'$set': {'last_id': next_id}})
                return next_id
        else:
                image_collection_id.insert_one({'last_id': 1})
                return 1

def create(body):
        user = user_collection.insert_one(body)

def all_users():
        users_list = user_collection.find({}, {"_id": 0})
        return list(users_list)

def get_user(id):
        user = user_collection.find({"id": id}, {"_id": 0})
        return list(user)

def update_user(id, body):
        user_collection.update_one({"id": id},{'$set': {'email': body['email'], 'username': body['username']}})

def delete_user(id):
        user_collection.delete_one({"id": id})

def check_database(id):
        user = get_user(id)
        if not len(user):
                return True
        else:
                return False

def save_upload(image, comment):
        chat = chat_collection.insert_one({'message': comment.decode(), "image_file": image})

def get_chat():
        chat_list = chat_collection.find({}, {"_id": 0})
        return list(chat_list)

def save_live_chat(username, message):
        live_chat_collection.insert_one({"username": username, "comment": message["comment"]})

def get_live_chat():
        chat_list = live_chat_collection.find({}, {"_id": 0})
        return list(chat_list)

def store_information(username, password):
        information_collection.insert_one({username.decode(): password})

def get_information_by_username(username):
        user = information_collection.find({},{username.decode():1,"_id": 0})
        user = list(user)
        for i in user:
                if i:
                        return i
        return 0

def store_token(username, token):
        user = list(user_token_collection.find({},{username:1,"_id":0}))
        if user:
                user_token_collection.update_one({},{'$set':{username: token.decode()}})
        else:        
                user_token_collection.insert_one({username: token.decode()})

def get_token_by_username(username):
        user = user_token_collection.find({},{username:1,"_id":0})
        return list(user)