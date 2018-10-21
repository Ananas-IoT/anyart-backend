from django.http import HttpResponse
from .fireconf import firebase


def home(request):
    db = firebase.database()
    data = {"name": "Anna Manko Ivanivna"}
    db.child("users").push(data)
    return HttpResponse("This is homepage.")