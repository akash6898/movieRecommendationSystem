from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import pandas as pd
import json
def home(request):
    data=pd.read_csv('C:\\Users\\shash\Desktop\\Data_Science\\dataScience\\movie recommendation\\code\\main_data.csv')
    movie_name=data['movie_title']
    movie_list=list()
    for a in movie_name:
        movie_list.append(a)
    #print(movie_name)
    json_list = json.dumps(movie_list)
    return render(request,'MainPage/index.html',{'movie_list':json_list})
def search(request):
    movie=request.POST['movie']
    return HttpResponse(movie)
