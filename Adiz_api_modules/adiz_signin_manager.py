import jwt
from datetime import datetime, timedelta

class JWTManager:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def generate_token(self, user_id, expires_on):
        payload = {
            'user_id': user_id,
            'exp': expires_on  # Token expiration time (adjust as needed)
        }
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token has expired
        except jwt.InvalidTokenError:
            return None  # Invalid token

class ApiTokenManager:
    def __init__(self, db):
        self.db = db
        self.database = db.database
        self.db.connect()     
        use_db_query = f"USE `{self.database}`;"
        self.db.cursor.execute(use_db_query)

    def create_api_token(self, user_id, token, expiration_timestamp):
        query = '''
            INSERT INTO `api_tokens` (user_id, token, expiration_timestamp)
            VALUES (%s, %s, %s);
        '''
        data = (user_id, token, expiration_timestamp)
        self.db.cursor.execute(query, data)
        self.db.connection.commit()

    def get_api_token(self, user_id):
        query = 'SELECT token,expiration_timestamp FROM `api_tokens` WHERE `user_id` = %s;'
        data = (user_id,)
        self.db.cursor.execute(query, data)
        return self.db.cursor.fetchone()
    
    
    def update_api_token(self, user_id, token , expires):
        query = "UPDATE `api_tokens` SET token = '%s' ,expiration_timestamp = '%s'  WHERE `user_id` = %s;"%(token,expires,user_id)
        print(query)
        self.db.cursor.execute(query)
        self.db.connection.commit()
        
    def delete_token(self,token):
        delete_query = "DELETE FROM `api_tokens` WHERE token = %"%token
        try:
            self.db.cursor.execute(delete_query)
            self.db.connection.commit()
        except:
            return {'error':'unable to logout!'}
        


    def has_token(self,user_id):
        tok = self.get_api_token(user_id)
        if tok:
            return True
        else:
            return False
        
    def token_expired(self, user_id):
        if self.has_token(user_id):
            token_ex = self.get_api_token(user_id)[1]
            if token_ex.timestamp() <= int(datetime.utcnow().timestamp()):
                return True
            else:
                return False
    
        



class LoginManager:
    def __init__(self,dbcon,token_secret):
        self.dbcon = dbcon
        self.database = dbcon.database
        self.jwtman = JWTManager(token_secret)
        self.tokenrec = ApiTokenManager(self.dbcon)
        
    def login(self,user_id):
        self.dbcon.connect()     
        use_db_query = f"USE `{self.database}`;"
        self.dbcon.cursor.execute(use_db_query)
        token_expire = datetime.utcnow() + timedelta(minutes=1)
        if self.tokenrec.has_token(user_id):
            ex_token =  self.tokenrec.get_api_token(user_id)[0]
            ex_t =  self.tokenrec.get_api_token(user_id)[1]
            print("ex_expire: %s \nnow: %s"%(ex_t,datetime.utcnow()))
            if self.tokenrec.token_expired(user_id):
                the_token = self.jwtman.generate_token(user_id,token_expire)
                self.tokenrec.update_api_token(user_id,the_token,token_expire)
            else:
                return ex_token
        else:
            the_token = self.jwtman.generate_token(user_id,token_expire)
            self.tokenrec.create_api_token(user_id,the_token,token_expire)

        return the_token
            
        
    def logout(self,token):
        self.tokenrec.delete_token(token)
        
        
        
