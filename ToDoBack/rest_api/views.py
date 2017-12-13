from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from controlers.model import Model

from datetime import date

mod = Model()


@api_view(['POST', "GET"])
def sign_up(request):

    if request.method == 'GET':
        data = {"displayName": "asdfUk",
                "email": "asdfuk@com.com",
                "password": "Git_Good25",
                "repeatPassword": "Git_Good25"}

    elif request.method == 'POST':
        data = request.data

    """Process of signing up"""

    result = mod.sign_up(data["displayName"], data["email"], data["password"], data["repeatPassword"])
    return Response(result)


@api_view(['POST', "GET"])
def sign_in(request):

    if request.method == 'GET':
        data = {"email": "asdfuk@com.com",
                "password": "Git_Good25"}

    elif request.method == 'POST':
        data = request.data

    """Process of signing in"""

    result = mod.sign_in(data["email"], data["password"])
    return Response(result)


@api_view(['POST', "GET"])
def create_project(request):

    if request.method == 'GET':
        data = {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpvaG4gZG9lIiwiaWQiOjF9.SWi5pYoCM6I0DBsCTXS6POZlWR4sOMI7GovWBDedvCk",
                "username": "john doe",
                "name": "newShit25",
                "color": "FFBF7F"}

    elif request.method == 'POST':
        data = request.data

    """Process of signing in"""

    result = mod.create_project(data)
    return Response(result)


@api_view(['POST', "GET"])
def change_project(request):

    if request.method == 'GET':
        data = {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpvaG4gZG9lIiwiaWQiOjF9.SWi5pYoCM6I0DBsCTXS6POZlWR4sOMI7GovWBDedvCk",
                "username": "john doe",
                "id": 1,
                "name": "newShit3",
                "color": "FFBF7R"}

    elif request.method == 'POST':
        data = request.data

    """Process of signing in"""

    print(data)

    result = mod.change_project(data)
    return Response(result)


@api_view(['POST', "GET"])
def delete_project(request):

    if request.method == 'GET':
        data = {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpvaG4gZG9lIiwiaWQiOjF9.SWi5pYoCM6I0DBsCTXS6POZlWR4sOMI7GovWBDedvCk",
                "username": "john doe",
                "id": 2}

    elif request.method == 'POST':
        data = request.data

    """Process of signing in"""
    result = mod.delete_project(data)
    return Response(result)


@api_view(['POST', "GET"])
def get_projects(request):

    if request.method == 'GET':
        data = {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpvaG4gZG9lIiwiaWQiOjF9.SWi5pYoCM6I0DBsCTXS6POZlWR4sOMI7GovWBDedvCk",
                "username": "john doe"}

    elif request.method == 'POST':
        data = request.data

    """Process of signing in"""

    result = mod.get_projects(data)
    return Response(result)


@api_view(['POST', "GET"])
def create_task(request):

    if request.method == 'GET':
        data = {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpvaG4gZG9lIiwiaWQiOjF9.SWi5pYoCM6I0DBsCTXS6POZlWR4sOMI7GovWBDedvCk",
                "username": "john doe",
                "project": 1,
                "name": "Guerrillas",
                "state": "Done",
                "priority": 1,
                "due_date": date(day=13, year=2017, month=12)}

    elif request.method == 'POST':
        data = request.data

    """Process of signing in"""

    result = mod.create_task(data)
    return Response(result)


@api_view(['POST', "GET"])
def get_tasks_for_today(request):

    if request.method == 'GET':
        data = {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpvaG4gZG9lIiwiaWQiOjF9.SWi5pYoCM6I0DBsCTXS6POZlWR4sOMI7GovWBDedvCk",
                "username": "john doe"}

    elif request.method == 'POST':
        data = request.data

    """Process of signing in"""

    result = mod.get_tasks_for_today(data)

    return Response(result)


@api_view(['POST', "GET"])
def get_tasks_for_7_days(request):

    if request.method == 'GET':
        data = {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpvaG4gZG9lIiwiaWQiOjF9.SWi5pYoCM6I0DBsCTXS6POZlWR4sOMI7GovWBDedvCk",
                "username": "john doe"}

    elif request.method == 'POST':
        data = request.data

    """Process of signing in"""

    result = mod.get_tasks_for_7_days(data)
    return Response(result)


@api_view(['POST', "GET"])
def get_tasks_for_project(request):

    if request.method == 'GET':
        data = {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpvaG4gZG9lIiwiaWQiOjF9.SWi5pYoCM6I0DBsCTXS6POZlWR4sOMI7GovWBDedvCk",
                "username": "john doe",
                "project": 4}

    elif request.method == 'POST':
        data = request.data

    """Process of signing in"""

    result = mod.get_tasks_for_project(data)
    return Response(result)


@api_view(['POST', "GET"])
def get_done_tasks(request):

    if request.method == 'GET':
        data = {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpvaG4gZG9lIiwiaWQiOjF9.SWi5pYoCM6I0DBsCTXS6POZlWR4sOMI7GovWBDedvCk",
                "username": "john doe"}

    elif request.method == 'POST':
        data = request.data

    """Process of signing in"""

    result = mod.get_done_tasks(data)
    return Response(result)


@api_view(['POST', "GET"])
def change_task(request):

    if request.method == 'GET':
        data = {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpvaG4gZG9lIiwiaWQiOjF9.SWi5pYoCM6I0DBsCTXS6POZlWR4sOMI7GovWBDedvCk",
                "username": "john doe",
                "project": 4,
                "id": 8,
                "name": "newShit89",
                "state": "Done",
                "priority": "1"}

    elif request.method == 'POST':
        data = request.data

    """Process of signing in"""

    result = mod.change_task(data)
    return Response(result)


@api_view(['POST', "GET"])
def delete_task(request):

    if request.method == 'GET':
        data = {"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpvaG4gZG9lIiwiaWQiOjF9.SWi5pYoCM6I0DBsCTXS6POZlWR4sOMI7GovWBDedvCk",
                "username": "john doe",
                "id": 9}

    elif request.method == 'POST':
        data = request.data

    """Process of signing in"""

    result = mod.delete_task(data)
    return Response(result)
