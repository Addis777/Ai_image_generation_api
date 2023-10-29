import json
from Adiz_api_modules.adiz_key_manager import APIKeyManager
from Adiz_api_modules.adiz_db import MySQLDatabase , UserDatabase
from Adiz_api_modules.adiz_signin_manager import LoginManager, ApiTokenManager , JWTManager
from Adiz_api_modules.adiz_image_generator import ImageGenerator
from Adiz_api_modules.adiz_Oauth2Provider import OAuth2Provider


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'Adiz_test'
}
GCLIENT_ID ="your GOOGLE client id"
GCLIENT_SECRET = "your GOOGLE client secret"

MCLIENT_ID ="your MICROSOFT client id"
MCLIENT_SECRET = "your MICROSOFT client secret"

ACLIENT_ID ="your APPLE client id"
ACLIENT_SECRET = "your APPLE client secret"

REDIRECT_URI = ""

dat = MySQLDatabase(**db_config)
dat.initialize_database()
api_key = '12457'
token_secret = "mytoken_sectret"
keyman = APIKeyManager(api_key)
image_man = ImageGenerator()
login_man = LoginManager(dat,token_secret)
jwt_man = JWTManager(token_secret)
form_data = {}

def Adiz_api(environ, start_response):
    request_method = environ['REQUEST_METHOD']
    headers = [('Content-Type', 'application/json'),
               ('Access-Control-Allow-Origin','*'),
               ('Access-Control-Allow-Methods', 'POST'),
               ('Access-Control-Allow-Headers','Content-Type, Authorization')
               ]
    if request_method =='POST':
        content_length = int(environ.get('CONTENT_LENGTH',0))
        if content_length > 0:
            posts = environ['wsgi.input'].read(content_length).decode('utf-8')
            post_params = posts.split('&')
            for param in post_params:
                key, value = param.split('=')
                form_data[key] = value
            if not keyman.validate_key(form_data['api_key']):
                status = '200 OK'
                response_data = {'error':'Invalid API Key!'}
                json_response = json.dumps(response_data)
                start_response(status, headers)
                return [json_response.encode()]
      
    else:
        status = '200 OK'
        response_data = {'message':'Method not Allowed!'}
        json_response = json.dumps(response_data)
        start_response(status, headers)
        return [json_response.encode()]
    
    path = environ.get('PATH_INFO', '').rstrip('/')
    if environ.get('PATH_INFO', '') == '/':
        status = '200 OK'
        print ("myname : %s"%form_data['myname'])
        response_data = {'maname':f"hello {form_data['myname']}!"}
    elif path == '/v1/signin':
        response_data = signin_handler()
        status = '200 OK'
    elif path == '/v1/signout':
        response_data = signout_handler()
        status = '200 OK'
    elif path == '/v1/generate-image':
        response_data = generate_image_handler()
        status = '200 OK'
    elif path == '/v1/edit-image':
        response_data = edit_image_handler()
        status = '200 OK'
    elif path == '/v1/referral-link':
        response_data = referral_link_handler()
        status = '200 OK'
    elif path == '/v1/credit':
        response_data = credit_handler()
        status = '200 OK'
    elif path == '/v1/doc':
        response_data = doc_handler()
        status = '200 OK'
    else:
        status = '404 Not Found'
        response_data = {'message': 'Endpoint not found'}

    # Serialize response_data to JSON
    json_response = json.dumps(response_data)

    start_response(status, headers )
    return [json_response.encode()]

# Define handler functions for each endpoint
def signin_handler():
    sign_type = form_data['sign_type']
    oauth2 = ""
    if sign_type == "code":
        if form_data['sign_to'] == 'google':
            oauth2 = OAuth2(GCLIENT_ID, GCLIENT_SECRET, REDIRECT_URI)
        elif form_data['sign_to'] == 'microsoft':
            oauth2 = GoogleOAuth(MCLIENT_ID, MCLIENT_SECRET, REDIRECT_URI)
        elif form_data['sign_to'] == 'apple':
            oauth2 = GoogleOAuth(ACLIENT_ID, ACLIENT_SECRET, REDIRECT_URI)
        else:
            return {"error": "can't sign up into %s"%form_data['sign_to']}
        auth_url = oauth2.get_authentication_url()
        return {"url": auth_url}
    
    elif sign_type == "signin":
        code = form_data['code']
        access_token, id_token = oauth2.exchange_code_for_tokens(authorization_code)
        user_info = oauth2.get_user_info(access_token)
        userdb = UserDatabase(dat)
        user_id = usdab.create_user(user_info['name'],user_info['email'],profile_pic=user_info['profile_picture'],ref=form_data['ref'])
        return login_man.login(user_id)    

def signout_handler():
    try:
        login_man.logout(form_data['token'])
        return {'message': 'Signed out successfully'}
    except:
        return {'error': 'unable to sign out'}
    
def generate_image_handler():
    try:
        prompt = form_data['prompt']
        size = form_data['size']
        num_of_images = form_data['numb']
    except:
        return {'error': 'Something went wrong!'}
    if prompt and size and num_of_images:
        return image_man.generate(prompt,size,num_of_images)

def edit_image_handler():
    try:
        mask_img = form_data['mask_image']
        img = form_data['image']
        prompt = form_data['prompt']
        size = form_data['size']
        num_of_images = form_data['numb']
    except:
        return {'error': 'Something went wrong!'}
    if prompt and size and num_of_images:
        return image_man.generate(prompt,img,mask_img,size,num_of_images)
    
def referral_link_handler():
    try:
        user_data = jwt_man.decode(form_date['token'])
        query = 'SELECT referral_code FROM `referrals` WHERE `user_id` = %s;'
        data = (user_data['user_id'],)
        self.db.execute_query(query, data)
        return self.db.cursor.fetchall()
    except:
        return {'error': 'unable to fetch referral code!'}
    
def credit_handler():
    try:
        user_data = jwt_man.decode(form_date['token'])
        query = 'SELECT free_credits, earned_credits FROM `credits` WHERE `user_id` = %s;'
        data = (user_data['user_id'],)
        self.db.execute_query(query, data)
        return self.db.cursor.fetchall()
    except:
        return {'error': 'unable to fetch credits info!'}
    
def doc_handler():
    try:
        user_data = jwt_man.decode(form_date['token'])
        query = 'SELECT * FROM `api_docs`'
        self.db.execute_query(query, data)
        return self.db.cursor.fetchall()
    except:
        return {'error': 'unable to fetch api documentation!'}
    



if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    httpd = make_server('localhost', 90, Adiz_api)
    print('Listening on port 90...')
    httpd.serve_forever()
