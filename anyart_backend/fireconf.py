import pyrebase

config = {
    "apiKey": "AIzaSyBQyAhqhl06fqpET264Nxhz8xb0ANRJvC4",
    "authDomain": "anyart-1efb8.firebaseapp.com",
    "databaseURL": "https://anyart-1efb8.firebaseio.com",
    "projectId": "anyart-1efb8",
    "storageBucket": "anyart-1efb8.appspot.com",
    "messagingSenderId": "812160347547"
}

firebase = pyrebase.initialize_app(config)