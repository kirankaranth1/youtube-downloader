import pafy
import urllib
import sys
import time
import os
 

def reporthook(count, block_size, total_size):
   global start_time
   if count == 0:
       start_time = time.time()
       return
   duration = time.time() - start_time
   progress_size = float(count * block_size)
   speed = int(progress_size / (1024 * duration))
   percent = int(count * block_size * 100 / total_size)
   sys.stdout.write("\r...%d%%, %f MB, %d KB/s, %d seconds passed." %(percent, float(progress_size) / (1024.0 * 1024.0), speed, duration))
   sys.stdout.flush()

def vdetails(pobject):
   print("\nVideo Title:\n" + str(pobject.title)+"\n")
   print("Available download options: \n")
   opt=pobject.allstreams
   count=1
   for o in opt:
      print("Option "+ str(count)+": "+str(o))
      count=count+1
   

def down(pobject,choice):
   
   if (choice == "best"):
      Durl=pobject.getbest().url
      Dstream=pobject.getbest()
   else:
      Durl=pobject.allstreams[int(choice)-1].url
      Dstream=pobject.allstreams[int(choice)-1]
   filename=str(pobject.title)+"."+str(Dstream).split('@')[0].split(':')[1]
   print("Downloading "+filename)
   urllib.urlretrieve(str(Durl), filename,reporthook)
   print("\nFile downloaded at "+str(os.getcwd())+"/"+filename)

def pldetails(pl):
   print("Playlist details:\n")
   print("Playlist title: "+str(pl['title']))
   print("Videos in this playlist: \n")
   for i in range(1,len(pl['items'])):
      print("Video "+str(i)+":"+str(pl['items'][i]['pafy'].title))


def downpl(pl,c):
   if c=="all":
      c=range(1,len(pl['items']))
   for i in c:
      down(pl['items'][i]['pafy'],"best")      


def schedule():
   print("Enter the IDs of videos in playlist you want to download: ")
   print("or enter 'all' to download all videos in playlist: ")
   print("EXAMPLE: Type 1,4,5,7 to download videos 1,4,5 & 7 of playlist in that order.")
   choice=raw_input()
   if choice!='all':
       c=choice.split(',')
       c = map(int, c)
       return c
   else:
       return choice


Yurl=raw_input("Enter URL of youtube video or playlist: ")

if((Yurl.find("list"))>=0)or((Yurl.find("playlist"))>=0):
  pl=True
  print("Playlist detected")
  playlist = pafy.get_playlist(Yurl)
  pldetails(playlist)
  c=schedule()
  print(c)
  downpl(playlist,c)
  print("Done. All videos downloaded!")
  
else:
  pl=False
  pobj=pafy.new(Yurl)
  vdetails(pobj)
  choice=raw_input("Enter download option number(or just enter 'best' for best quality download): " )
  down(pobj,choice)
  


