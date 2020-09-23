from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import pandas as pd
import json
# film poster
# https://image.tmdb.org/t/p/w500/kqjL17yufvn9OVLyXYpvtyrFfak.jpg
# personal details
# https://api.themoviedb.org/3/person/776?api_key=5492165c61b1a21c06eb3a3b578a6339&language=en-US
class MOVIE:
    def __init__(self,id,moviePoster,adult,budget,originalTitle,overView,releaseDate,Language,voteAverage,voteCount,actorList):
        self.id=id
        self.moviePoster=moviePoster
        self.adult=adult
        self.budget=budget
        self.originalTitle=originalTitle
        self.overView=overView
        self.releaseDate=releaseDate
        self.Language=Language
        self.voteAverage=voteAverage
        self.voteCount=voteCount
        self.actorList=actorList
    def printData(self):
        print(self.moviePoster)

class Actors:
    def __init__(self,actorId,actorName,actorProfilePhoto,actorCharacter,actorBirthday,actorBiography,actorDepartment):
        self.actorId=actorId
        self.actorName=actorName
        self.actorProfilePhoto=actorProfilePhoto
        self.actorCharacter=actorCharacter
        self.actorBirthday=actorBirthday
        self.actorBiography=actorBiography
        self.actorDepartment=actorDepartment

def home(request):
    data=pd.read_csv('templates\\Dataset\\main_data.csv')
    movie_name=data['movie_title']
    movie_list=list()
    for a in movie_name:
        movie_list.append(a)
    #print(movie_name)
    json_list = json.dumps(movie_list)
    return render(request,'MainPage/index.html',{'movie_list':json_list,'from_home':True})

def search(request):
    movie=request.POST['movie']
    movieList=recommendMovie(movie)
    print(movieList)
    movieDetailList=getDetails(movieList)
    # print(movieDetailList)
    data=pd.read_csv('templates\\Dataset\\main_data.csv')
    movie_name=data['movie_title']
    movie_list=list()
    for a in movie_name:
        movie_list.append(a)
    #print(movie_name)
    json_list = json.dumps(movie_list)
    mainMovieList=list()
    mainMovieList=(getDetailsOfMainMovie(movie))
    print(mainMovieList)
    return render(request,'MainPage/index.html',{'movie_list':json_list,'from_home':False,'from_search':True,'mainMovieList':mainMovieList,'movieDetailList':movieDetailList})

def searching(request,movieName):
    movie=movieName.lower()
    movieList=recommendMovie(movie)
    print(movieList)
    movieDetailList=getDetails(movieList)
    # print(movieDetailList)
    data=pd.read_csv('templates\\Dataset\\main_data.csv')
    movie_name=data['movie_title']
    movie_list=list()
    for a in movie_name:
        movie_list.append(a)
    #print(movie_name)
    json_list = json.dumps(movie_list)
    mainMovieList=list()
    mainMovieList=(getDetailsOfMainMovie(movie))
    print(mainMovieList)
    return render(request,'MainPage/index.html',{'movie_list':json_list,'from_home':False,'from_search':True,'mainMovieList':mainMovieList,'movieDetailList':movieDetailList})


def takeSecond(elem):
    return elem[1]

def recommendMovie(movieName):
    data=pd.read_csv('templates\\Dataset\\main_data.csv')
    movie_name=data['movie_title']

    from sklearn.feature_extraction.text import CountVectorizer
    cv=CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    count_matri_to_array=count_matrix.toarray()
    from sklearn.metrics.pairwise import cosine_similarity
    similarity = cosine_similarity(count_matrix)
    index_of_movie=data.loc[data['movie_title']==movieName].index[0]
    lst = list(enumerate(similarity[index_of_movie]))
    movieList=list()
    genreList=list()
    for i in sorted(lst,key=takeSecond,reverse=True)[0:11]:
        if i[0]!=index_of_movie:
            movieList.append(data.iloc[i[0]]['movie_title'])
    return movieList



def getDetails(movieList):
    from tmdbv3api import TMDb
    import json
    import requests
    tmdb = TMDb()
    tmdb.api_key = '5492165c61b1a21c06eb3a3b578a6339'
    from tmdbv3api import Movie
    tmdb_movie = Movie()
    movieDetailList=list()
    i=1
    for movie in movieList:
        ##################################################################
        ######################  GETTING DETAILS OF MOVIE #################
        ##################################################################
        print(movie)
        result = tmdb_movie.search(movie)
        movie_id = result[0].id
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
        data_json = response.json()
        moviePoster="https://image.tmdb.org/t/p/w500"+data_json['poster_path']
        adult=data_json['adult']
        budget=data_json['budget']
        originalTitle=data_json['original_title']
        overView=data_json['overview']
        releaseDate=data_json['release_date']
        Language=data_json['spoken_languages'][0]['name']
        voteAverage=data_json['vote_average']
        voteCount=data_json['vote_count']
        response = requests.get('https://api.themoviedb.org/3/movie/{}/credits?api_key={}'.format(movie_id,tmdb.api_key))
        data_json=response.json()
        actorList=list()
        x=MOVIE(i,moviePoster,adult,budget,originalTitle,overView,releaseDate,Language,voteAverage,voteCount,actorList)
        movieDetailList.append(x)
        i=i+1
    return movieDetailList


def getDetailsOfMainMovie(movie):
    from tmdbv3api import TMDb
    import json
    import requests
    tmdb = TMDb()
    tmdb.api_key = '5492165c61b1a21c06eb3a3b578a6339'
    from tmdbv3api import Movie
    tmdb_movie = Movie()
    movieDetailList=list()

    ##################################################################
    ######################  GETTING DETAILS OF MOVIE #################
    ##################################################################
    print(movie)
    result = tmdb_movie.search(movie)
    movie_id = result[0].id
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
    data_json = response.json()
    moviePoster="https://image.tmdb.org/t/p/w500"+data_json['poster_path']
    adult=data_json['adult']
    budget=data_json['budget']
    originalTitle=data_json['original_title']
    overView=data_json['overview']
    releaseDate=data_json['release_date']
    Language=data_json['spoken_languages'][0]['name']
    voteAverage=data_json['vote_average']
    voteCount=data_json['vote_count']
    response = requests.get('https://api.themoviedb.org/3/movie/{}/credits?api_key={}'.format(movie_id,tmdb.api_key))
    data_json=response.json()
    try:
        actor1Id=data_json['cast'][0]['id']
        actor1Name=data_json['cast'][0]['name']
        if(data_json['cast'][0]['profile_path']==None):
            actor1ProfilePhoto="templates\\mainPage\\images\\blank_man.jpg"
        else:
            actor1ProfilePhoto="https://image.tmdb.org/t/p/w500"+data_json['cast'][0]['profile_path']
        actor1Character=data_json['cast'][0]['character']

        actor2Id=data_json['cast'][1]['id']
        actor2Name=data_json['cast'][1]['name']
        if(data_json['cast'][1]['profile_path']==None):
            actor2ProfilePhoto="templates\\mainPage\\images\\blank_man.jpg"
        else:
            actor2ProfilePhoto="https://image.tmdb.org/t/p/w500"+data_json['cast'][1]['profile_path']
        actor2Character=data_json['cast'][1]['character']

        actor3Id=data_json['cast'][2]['id']
        actor3Name=data_json['cast'][3]['name']
        if(data_json['cast'][2]['profile_path']==None):
            actor3ProfilePhoto="templates\\mainPage\\images\\blank_man.jpg"
        else:
            actor3ProfilePhoto="https://image.tmdb.org/t/p/w500"+data_json['cast'][2]['profile_path']
        actor3Character=data_json['cast'][2]['character']

        actor4Id=data_json['cast'][3]['id']
        actor4Name=data_json['cast'][3]['name']
        if(data_json['cast'][3]['profile_path']==None):
            actor4ProfilePhoto="templates\\mainPage\\images\\blank_man.jpg"
        else:
            actor4ProfilePhoto="https://image.tmdb.org/t/p/w500"+data_json['cast'][3]['profile_path']
        actor4Character=data_json['cast'][3]['character']

        actor5Id=data_json['cast'][4]['id']
        actor5Name=data_json['cast'][4]['name']
        if(data_json['cast'][4]['profile_path']==None):
            actor5ProfilePhoto="templates\\mainPage\\images\\blank_man.jpg"
        else:
            actor5ProfilePhoto="https://image.tmdb.org/t/p/w500"+data_json['cast'][4]['profile_path']
        actor5Character=data_json['cast'][4]['character']

        actor6Id=data_json['cast'][5]['id']
        actor6Name=data_json['cast'][5]['name']
        if(data_json['cast'][5]['profile_path']==None):
            actor6ProfilePhoto="templates\\mainPage\\images\\blank_man.jpg"
        else:
            actor6ProfilePhoto="https://image.tmdb.org/t/p/w500"+data_json['cast'][5]['profile_path']
        actor6Character=data_json['cast'][5]['character']

        actor7Id=data_json['cast'][6]['id']
        actor7Name=data_json['cast'][6]['name']
        if(data_json['cast'][6]['profile_path']==None):
            actor7ProfilePhoto="templates\\mainPage\\images\\blank_man.jpg"
        else:
            actor7ProfilePhoto="https://image.tmdb.org/t/p/w500"+data_json['cast'][6]['profile_path']
        actor7Character=data_json['cast'][6]['character']

        actor8Id=data_json['cast'][7]['id']
        actor8Name=data_json['cast'][7]['name']
        if(data_json['cast'][7]['profile_path']==None):
            actor8ProfilePhoto="templates\\mainPage\\images\\blank_man.jpg"
        else:
            actor8ProfilePhoto="https://image.tmdb.org/t/p/w500"+data_json['cast'][7]['profile_path']
        actor8Character=data_json['cast'][7]['character']

        response = requests.get('https://api.themoviedb.org/3/person/{}?api_key={}&language=en-US'.format(str(actor1Id),tmdb.api_key))
        data_json=response.json()
        actor1Birthday=data_json['birthday']
        actor1Department=data_json['known_for_department']
        actor1Biography=data_json['biography']

        response = requests.get('https://api.themoviedb.org/3/person/{}?api_key={}&language=en-US'.format(str(actor1Id),tmdb.api_key))
        data_json=response.json()
        actor1Birthday=data_json['birthday']
        actor1Department=data_json['known_for_department']
        actor1Biography=data_json['biography']

        response = requests.get('https://api.themoviedb.org/3/person/{}?api_key={}&language=en-US'.format(str(actor2Id),tmdb.api_key))
        data_json=response.json()
        actor2Birthday=data_json['birthday']
        actor2Department=data_json['known_for_department']
        actor2Biography=data_json['biography']

        response = requests.get('https://api.themoviedb.org/3/person/{}?api_key={}&language=en-US'.format(str(actor3Id),tmdb.api_key))
        data_json=response.json()
        actor3Birthday=data_json['birthday']
        actor3Department=data_json['known_for_department']
        actor3Biography=data_json['biography']

        response = requests.get('https://api.themoviedb.org/3/person/{}?api_key={}&language=en-US'.format(str(actor4Id),tmdb.api_key))
        data_json=response.json()
        actor4Birthday=data_json['birthday']
        actor4Department=data_json['known_for_department']
        actor4Biography=data_json['biography']

        response = requests.get('https://api.themoviedb.org/3/person/{}?api_key={}&language=en-US'.format(str(actor5Id),tmdb.api_key))
        data_json=response.json()
        actor5Birthday=data_json['birthday']
        actor5Department=data_json['known_for_department']
        actor5Biography=data_json['biography']

        response = requests.get('https://api.themoviedb.org/3/person/{}?api_key={}&language=en-US'.format(str(actor6Id),tmdb.api_key))
        data_json=response.json()
        actor6Birthday=data_json['birthday']
        actor6Department=data_json['known_for_department']
        actor6Biography=data_json['biography']

        response = requests.get('https://api.themoviedb.org/3/person/{}?api_key={}&language=en-US'.format(str(actor7Id),tmdb.api_key))
        data_json=response.json()
        actor7Birthday=data_json['birthday']
        actor7Department=data_json['known_for_department']
        actor7Biography=data_json['biography']

        response = requests.get('https://api.themoviedb.org/3/person/{}?api_key={}&language=en-US'.format(str(actor8Id),tmdb.api_key))
        data_json=response.json()
        actor8Birthday=data_json['birthday']
        actor8Department=data_json['known_for_department']
        actor8Biography=data_json['biography']

        a1=Actors(actor1Id,actor1Name,actor1ProfilePhoto,actor1Character,actor1Birthday,actor1Biography,actor1Department)
        a2=Actors(actor2Id,actor2Name,actor2ProfilePhoto,actor2Character,actor2Birthday,actor2Biography,actor2Department)
        a3=Actors(actor3Id,actor3Name,actor3ProfilePhoto,actor3Character,actor3Birthday,actor3Biography,actor3Department)
        a4=Actors(actor4Id,actor4Name,actor4ProfilePhoto,actor4Character,actor4Birthday,actor4Biography,actor4Department)
        a5=Actors(actor5Id,actor5Name,actor5ProfilePhoto,actor5Character,actor5Birthday,actor5Biography,actor5Department)
        a6=Actors(actor6Id,actor6Name,actor6ProfilePhoto,actor6Character,actor6Birthday,actor6Biography,actor6Department)
        a7=Actors(actor7Id,actor7Name,actor7ProfilePhoto,actor7Character,actor7Birthday,actor7Biography,actor7Department)
        a8=Actors(actor8Id,actor8Name,actor8ProfilePhoto,actor8Character,actor8Birthday,actor8Biography,actor8Department)

        actorList=list()
        actorList.append(a1)
        actorList.append(a2)
        actorList.append(a3)
        actorList.append(a4)
        actorList.append(a5)
        actorList.append(a6)
        actorList.append(a7)
        actorList.append(a8)

        x=MOVIE(0,moviePoster,adult,budget,originalTitle,overView,releaseDate,Language,voteAverage,voteCount,actorList)
        movieDetailList.append(x)
    except:
        print("an error occured")
    return movieDetailList
