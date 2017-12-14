"""Functions to get responces to responde to user request"""


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from controlers.controler import Controler

from datetime import date

mod = Controler()


@api_view(['POST'])
def sign_up(request):
    data = request.data

    result = mod.sign_up(data["displayName"], data["email"], data["password"], data["repeatPassword"])
    return Response(result)


@api_view(['POST'])
def sign_in(request):
    data = request.data

    result = mod.sign_in(data["email"], data["password"])
    return Response(result)


@api_view(['POST'])
def create_project(request):
    data = request.data

    result = mod.create_project(data)
    return Response(result)


@api_view(['POST'])
def change_project(request):
    data = request.data

    result = mod.change_project(data)
    return Response(result)


@api_view(['POST'])
def delete_project(request):
    data = request.data

    result = mod.delete_project(data)
    return Response(result)


@api_view(['POST'])
def get_projects(request):
    data = request.data

    result = mod.get_projects(data)
    return Response(result)


@api_view(['POST'])
def create_task(request):
    data = request.data

    result = mod.create_task(data)
    return Response(result)


@api_view(['POST'])
def get_tasks_for_today(request):
    data = request.data

    result = mod.get_tasks_for_today(data)
    return Response(result)


@api_view(['POST'])
def get_tasks_for_7_days(request):
    data = request.data

    result = mod.get_tasks_for_7_days(data)
    return Response(result)


@api_view(['POST'])
def get_tasks_for_project(request):
    data = request.data

    result = mod.get_tasks_for_project(data)
    return Response(result)


@api_view(['POST'])
def get_done_tasks(request):
    data = request.data

    result = mod.get_done_tasks(data)
    return Response(result)


@api_view(['POST'])
def change_task(request):
    data = request.data

    result = mod.change_task(data)
    return Response(result)


@api_view(['POST'])
def delete_task(request):
    data = request.data

    result = mod.delete_task(data)
    return Response(result)
