import pyrebase


config ={
    'apiKey': "AIzaSyCuATOltNI_Vxu_ucfzXPNmN2V1puvqABU",
    'authDomain': "appweb-orion-php.firebaseapp.com",
    'databaseURL': "https://appweb-orion-php-default-rtdb.firebaseio.com",
    'projectId': "appweb-orion-php",
    'storageBucket': "appweb-orion-php.appspot.com",
    'messagingSenderId': "365589111987",
    'appId': "1:365589111987:web:cc51e2470cbe43ec40fcc6"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

email = "ageu87@gmail.com"
password = "ageu123456789"

# user = auth.create_user_with_email_and_password(email, password)
# print(user)

user = auth.sign_in_with_email_and_password(email, password)
# print(user)

# info = auth.get_account_info(user['idToken'])
# print(info)

# auth.send_email_verification(user['idToken'])

# auth.send_password_reset_email(email)

