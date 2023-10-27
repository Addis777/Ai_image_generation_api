import pymysql
import html
import re
import random
import bcrypt
import os
import uuid
import requests
from Adiz_api_modules.adiz_api_log import ApiLogger

class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.logger = ApiLogger('api_log.log')

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
            )
            
            self.cursor = self.connection.cursor()
        except:
            self.logger.log_error("unable to connect to the database")
            return {"error":"unable to connect to the database!"}
        
        self.logger.log_info("Successfully connected to the database")
        return self.connection
 
    def disconnect(self):
        try:
            self.cursor.close()
            self.connection.close()
            self.logger.log_info("Closed the database connection")
        except:
            self.logger.log_error("unable to close the database connection")
            return {"error":"unable to close the database connection"}
            

    def initialize_database(self):
        # Connect without specifying a database
        self.connect()
        try:
            # Create the 'Adiz-db' database if it doesn't exist
            create_db_query = f"CREATE DATABASE IF NOT EXISTS `{self.database}`;"
            self.cursor.execute(create_db_query)

            # Use the 'Adiz-db' database
            use_db_query = f"USE `{self.database}`;"
            self.cursor.execute(use_db_query)

            # Create tables if they don't exist (you can add more tables here)
            create_users_table_query = '''
            CREATE TABLE IF NOT EXISTS `users` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `username` VARCHAR(255) NOT NULL,
                `email` VARCHAR(255) NOT NULL,
                `profile_pic` VARCHAR(255),
                `time_zone` varchar (255),
                `created_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE (`email`)
            );
            '''
            self.cursor.execute(create_users_table_query)

            create_user_interests_table_query = '''
            CREATE TABLE IF NOT EXISTS `user_interest` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id` INT NOT NULL,
                `interest` VARCHAR(255) NOT NULL,                
                `created_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
            );
            '''
            self.cursor.execute(create_user_interests_table_query)

            create_user_consent_table_query = '''
            CREATE TABLE IF NOT EXISTS `user_consent` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id` INT NOT NULL,
                `policy_name` VARCHAR(255) NOT NULL,
                `agreed` BOOLEAN NOT NULL,
                `agreement_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
            );
            '''
            self.cursor.execute(create_user_consent_table_query)

            # Create API Metadata Table
            create_api_metadata_table_query = '''
            CREATE TABLE IF NOT EXISTS `api_docs` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `endpoint` VARCHAR(255) NOT NULL,
                `description` VARCHAR(4096), -- Updated to VARCHAR
                `input_format` VARCHAR(4096), -- Updated to VARCHAR
                `output_format` VARCHAR(4096), -- Updated to VARCHAR
                `version` VARCHAR(10) NOT NULL,
                `created_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
             );
            '''
            self.cursor.execute(create_api_metadata_table_query)

            # Create Tokens Table
            create_tokens_table_query = '''
            CREATE TABLE IF NOT EXISTS `api_tokens` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id` INT,
                `token` VARCHAR(4096) NOT NULL, -- Updated to VARCHAR
                `expiration_timestamp` TIMESTAMP,
                `created_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
            );
            '''
            self.cursor.execute(create_tokens_table_query)


            create_user_interests_table_query = '''
            CREATE TABLE IF NOT EXISTS `referrals` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id` INT NOT NULL,
                `referral_code` varchar(255) NOT NULL,
                `no_of_referrals` INT NOT NULL DEFAULT 0,
                `created_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
            );
            '''
            self.cursor.execute(create_user_interests_table_query)

            create_user_interests_table_query = '''
            CREATE TABLE IF NOT EXISTS `credits` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `user_id` INT NOT NULL,
                `free_credits` INT(255) NOT NULL,
                `earned_credits` INT(255) DEFAULT 0,
                `forever_free`  BOOLEAN NOT NULL DEFAULT 0,
                `created_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `updated_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
            );
            '''
            self.cursor.execute(create_user_interests_table_query)

            # Commit the changes
            self.connection.commit()
            self.logger.log_info(f'Successfully initialized the database {self.database}')
        except:
            self.logger.log_error(f'unable to initialize the database {self.database}')
            return {'error': 'unable to initialize the database!'}

        finally:
            # Disconnect after creating the database and tables
            self.disconnect()            

class UserDatabase:
    def __init__(self,dbcon):
        self.dbcon = dbcon
        self.database = dbcon.database
        self.uconsent = UserConsent(dbcon)
        self.ppol = 'Privacy'
        self.cpol =  'Cookie'
        self.logger = ApiLogger('api_log.log')
        
    def create_user(self, username, email, profile_pic='',ref=''):
        freecredit = 100
        self.dbcon.connect()     
        use_db_query = f"USE `{self.database}`;"
        self.dbcon.cursor.execute(use_db_query)
        
        if not self.is_valid_email(email):
            self.logger.log_error(f"Couldn't SignIn the user {username} due to invalid email")
            return {'error':"Invalid email!"}
        try:
            query = f"INSERT INTO `users` (username, email ) VALUES ('{username}','{email}')"
            self.dbcon.cursor.execute(query)
            user_id = self.dbcon.cursor.lastrowid
            self.dbcon.connection.commit()
            self.logger.log_info(f"Successfully Signed Up the user In with user id : {user_id}")
            if ref:
                self.__manage_ref(ref)
                
            if profile_pic:
                self.__save_pic(profile_pic,user_id)
            self.uconsent.create_user_consent(user_id,self.ppol,True)
            self.uconsent.create_user_consent(user_id,self.cpol,True)
            refcode = self.__generate_random()
            refquery = f"INSERT INTO `referrals`(user_id, referral_code) VALUES ('{user_id}','{refcode}')"
            self.dbcon.cursor.execute(refquery)
            self.dbcon.connection.commit()
            credquery = f"INSERT INTO `credits` (user_id, free_credits) VALUES ('{user_id}','{freecredit}')"
            self.dbcon.cursor.execute(credquery)
            self.dbcon.connection.commit()
            return user_id
        except:
           self.dbcon.connection.rollback()
           self.logger.log_error(f"Unable to Signup the user.")
           return {'error':'Unable to Signup the user.'}
          

    
    def is_valid_email(self, email):
        # Implement email validation logic here
        # Example: Use a regular expression to validate email format
        return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None)

    

    def get_user(self, u_id):
        query = "SELECT * FROM users WHERE id = %s"
        data = (u_id,)
        self.dbcon.connect()
        use_db_query = f"USE `{self.database}`;"
        self.dbcon.cursor.execute(use_db_query)
        self.dbcon.cursor.execute(query, data)
        user_data = self.dbcon.cursor.fetchone()
        return user_data
    
    def __generate_random(self):
        self.dbcon.connect()
        use_db_query = f"USE `{self.database}`;"
        self.dbcon.cursor.execute(use_db_query)
        while True:
            random_number = int(random.randint(11111, 999999999999))
            print("%s \n"%random_number)
            try:
                query = "SELECT count(*) FROM referrals WHERE referral_code = '%s'"%random_number
                self.dbcon.cursor.execute(query)
                count = self.dbcon.cursor.fetchone()[0]
                if count == 0:
                    print("count : %s"%count)
                    return random_number
            except Exception as ex:
                self.logger.log_error(ex)
                print(ex)
                return
            
            
    def __save_pic(self,image_url,user_id):
        
        try:
            # Create the folder if it doesn't exist
            folder_path = "profile_pictures"
            os.makedirs(folder_path, exist_ok=True)
            ext = image_url.rsplit('.')[1]
            # Generate a unique filename
            self.dbcon.connect()
            use_db_query = f"USE `{self.database}`;"
            self.dbcon.cursor.execute(use_db_query)
            unique_filename = str(uuid.uuid4()) +'.'+ ext
            # Check if the unique filename already exists in the folder
            while os.path.exists(os.path.join(folder_path, unique_filename)):
                unique_filename = str(uuid.uuid4()) + '.' + ext 

            # Download the image from the URL
            response = requests.get(image_url)
            if response.status_code == 200:
                # Save the image to the folder with the unique filename
                file_path = os.path.join(folder_path, unique_filename)
                with open(file_path, 'wb') as file:
                    file.write(response.content)

                # Replace 'your_table_name' and 'your_column_name' with your actual table and column names
                insert_query = "UPDATE `users` SET  profile_pic = '%s' WHERE id = %d"%(unique_filename,user_id)
                self.dbcon.cursor.execute(insert_query)
                self.dbcon.connection.commit()
               

                return unique_filename
            else:
                self.dbcon.connection.rollback()
                print("Failed to download image. Status code:", response.status_code)
                return None

        except Exception as e:
            print("Error:", e)
            return None
        
    def __manage_ref(self,ref_code):
        query = f"UPDATE referrals SET no_of_referrals = no_of_referrals + 1 WHERE referral_code = {ref_code}"
        refcred = 100
        try:
            self.dbcon.cursor.execute(query)
            self.dbcon.connection.commit()
            self.logger.log_info(f"Successfuly updated number of referals for referal code : {ref_code}.")
        except:
            self.logger.log_error(f"Couldn't update number of referals for referral code : {ref_code}.")
            self.dbcon.connection.rollback()
            pass
        selcredquery = f"SELECT user_id FROM `referrals` WHERE referral_code = {ref_code}"
        

        try:
            self.dbcon.cursor.execute(selcredquery)
            u_id = self.dbcon.cursor.fetchone()[0]
            print("user_id : %s \n"%u_id)
            upcredquery = f"UPDATE `credits` SET earned_credits = earned_credits + {refcred} WHERE user_id = {u_id} "
            self.dbcon.cursor.execute(upcredquery)
            self.dbcon.connection.commit()
        except Exception as ex:
            self.dbcon.connection.rollback()
            self.logger.log_error('Database error occured : %s'%ex)
            


    
class ApiTokensTable:
    def __init__(self, db):
        self.db = db
        self.database = db.database

    def create_api_token(self, user_id, token, expiration_timestamp):
        query = '''
            INSERT INTO `api_tokens` (user_id, token, expiration_timestamp)
            VALUES (%s, %s, %s);
        '''
        data = (user_id, token, expiration_timestamp)
        self.db.execute_query(query, data)

    def get_api_tokens_by_user_id(self, user_id):
        query = 'SELECT * FROM `api_tokens` WHERE `user_id` = %s;'
        data = (user_id,)
        self.db.execute_query(query, data)
        return self.db.cursor.fetchall()

    
class PromptsTable:
    def __init__(self, db):
        self.db = db
        self.database = db.database

    def create_prompt(self, user_id, prompt_text):
        query = '''
            INSERT INTO `prompts` (user_id, prompt_text)
            VALUES (%s, %s);
        '''
        data = (user_id, prompt_text)
        self.db.execute_query(query, data)

    def get_prompts_by_user_id(self, user_id):
        query = 'SELECT * FROM `prompts` WHERE `user_id` = %s;'
        data = (user_id,)
        self.db.execute_query(query, data)
        return self.db.cursor.fetchall()

    
class UserInterestTable:
    def __init__(self, db):
        self.db = db
        self.database = db.database

    def create_user_interest(self, user_id, interest):
        query = '''
            INSERT INTO `user_interest` (user_id, interest)
            VALUES (%s, %s);
        '''
        data = (user_id, interest)
        self.db.execute_query(query, data)

    def get_interests_by_user_id(self, user_id):
        query = 'SELECT * FROM `user_interest` WHERE `user_id` = %s;'
        data = (user_id,)
        self.db.execute_query(query, data)
        return self.db.cursor.fetchall()

    
class UserConsent:
    def __init__(self, db):
        self.db = db
        self.database = db.database
        self.logger = ApiLogger('api_log.log')


    def create_user_consent(self, user_id, policy_name, agreed):
        self.db.connect()
        use_db_query = f"USE `{self.database}`;"
        try:

            self.db.cursor.execute(use_db_query)
            query = '''
                INSERT INTO `user_consent` (user_id, policy_name, agreed)
                VALUES (%s, %s, %s);
            '''
            data = (user_id, policy_name, agreed)
            self.db.cursor.execute(query, data)
            self.db.connection.commit()
        except:
            self.logger.log_error(f'unable to add consent ( {policy_name} policy ) for user with id : {user_id}')
        self.db.disconnect()
        self.logger.log_info(f'successfully added consent ( {policy_name} policy ) for user with id : {user_id}')

    def get_user_consents_by_user_id(self, user_id):
        query = 'SELECT * FROM `user_consent` WHERE `user_id` = %s;'
        data = (user_id,)
        self.db.cursor.execute(query, data)
        return self.db.cursor.fetchall()



