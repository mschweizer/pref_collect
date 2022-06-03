from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from rest_framework import viewsets, generics
from rest_framework.parsers import JSONParser

from .models import Preference
from .serializers import PreferenceSerializer


@csrf_exempt
def query_list(request):
    """
    List all queries, or create a new snippet.
    """
    if request.method == 'GET':
        preference_queries = Preference.objects.all()
        serializer = PreferenceSerializer(preference_queries, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PreferenceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def query_detail(request, query_id):
    """
    Retrieve, update or delete a preference_query.
    """
    try:
        preference_query = Preference.objects.get(pk=query_id)

        if request.method == 'GET':
            serializer = PreferenceSerializer(preference_query)
            return JsonResponse(serializer.data)

    except Preference.DoesNotExist:
        if request.method == 'GET':
            return HttpResponse(status=404)
        else:
            preference_query = Preference(uuid=query_id)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PreferenceSerializer(preference_query, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        preference_query.delete()
        return HttpResponse(status=204)


class QueryListView(ListView):

    model = Preference
    paginated_by = 100
    ordering = 'created_timestamp'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def index(request):
    
    return render(request, 'preferences/index.html')


def next_query(request):
    top_query = Preference.objects.filter(label__isnull=True).order_by('priority').first()
    if top_query is not None:
        return redirect('query', query_id=top_query.uuid)
    else:
        return redirect('index')


def query(request, query_id):

    query = get_object_or_404(Preference, uuid=query_id)
    if request.method == 'POST' and (label := request.POST['action']) is not None:
        if label == 'Left':
            query.label = 1
        elif label =='Right':
            query.label = 0
        elif label =='Indifferent':
            query.label = .5
        elif label == 'Skip':
            query.label = -1
        query.full_clean()
        query.save()
        return redirect('next')

    context = {
        'query': query,
        'video_url_left': query.video_file_path_left,
        'video_url_right': query.video_file_path_right
    }
    return render(request, 'preferences/query.html', context)
