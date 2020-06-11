import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from PIL import Image
import urllib.request
from tqdm import tqdm
import shutil
import operator
from collections import Counter

def ObtainAlbumData():
	# Get the username from terminal
	username = sys.argv[1]
	scope = 'user-library-read'

	# Erase cache and prompt for user permission
	try:
		token = util.prompt_for_user_token(username, scope) # add scope
	except (AttributeError, JSONDecodeError):
		os.remove(f".cache-{username}")
		token = util.prompt_for_user_token(username, scope) # add scope
	
	if token:
		sp = spotipy.Spotify(auth=token)  #Authorize Spotipy
		Data=[]
		i=0
		fp=open("AlbumData.txt","w")
		for x in range(4): 
			results = sp.current_user_saved_albums(50,i)	#Get first 50 albums
			for item in results['items']:	
				i+=1
				albums = item['album']		#Get Albums
				artists=albums['artists']	#Get Artist
				images=albums['images']		#Get Image Data
				url=images[0]['url']		#Get Image URL
				towrite=(str(i) + '. ' + albums['name'] + ' - ' + artists[0]['name'] + ' - ' +  url +'\n')
				fp.write(towrite)
				print(i,'. ',albums['name'],' - ',artists[0]['name'],url)	#Print Data
				Date=albums['release_date'].replace('-','')
				Data.append({"Album":albums['name'],"Artist":artists[0]['name'],"Date":Date,"Image":url})
		fp.close()
	else:
		print("Can't get token for", username)
	return Data
#################################################################################################################

def DLArtwork(Data):
	i=0
	print()
	print('Downloading Album Artwork:')
	for item in tqdm(range(len(Data))):
		dljpg(Data[i]['Image'],'im'+str(i))
		Data[i]['Image']='Wallpaper/Artwork/im'+str(i)+'.jpg'
		i+=1
	
	print()
	return Data

def dljpg(url,filename):
	fullpath='Wallpaper/Artwork/'+filename+'.jpg'
	urllib.request.urlretrieve(url, fullpath)

def sortArtist(Data):
	Data.sort(key=operator.itemgetter('Date'))
	Data.sort(key=operator.itemgetter('Artist'))
	count=Counter(item['Artist'] for item in Data)
	for i in range(len(Data)-1):
		Data[i].update({'#A':count[Data[i]['Artist']]})
		print(Data[i])	
	return Data	

def DomColour(Data):
	i=0;
	print('Obtaining Dominant Colour:')
	for item in tqdm(range(len(Data))):
		img=Image.open(Data[i]['Image'])
		img=img.resize((1,1))
		colour=img.getpixel((0,0))
		Data[i].update({'Dom':colour})
		i+=1
	return Data

def Wallpaper(Data):
	Width=1536
	Height=864
	amount=Data[0]['#A']
	W=Width/amount
	Wallpaper=Image.new('RGB',(Width,Height))
	

def main():
	Data=ObtainAlbumData()
	Data=sortArtist(Data)
	Data=DLArtwork(Data)
	Data=DomColour(Data)
	for item in Data:
		print(item)
main()
