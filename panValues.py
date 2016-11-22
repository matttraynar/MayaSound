import sys 
import platform
import types
import maya.cmds as cmds
import vec3
import camera
from pydub import AudioSegment


import os,  inspect
# realpath() will make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

def reload_package(root_module):
  '''
  CODE FROM http://stackoverflow.com/questions/2918898/prevent-python-from-caching-the-imported-modules
  WRITTEN BY MATT ANDERSON

  Used to reload external modules I have written and am using in Maya because these modules
  are normally cached. This means any changes I make to these modules would not be tracked
  unless they are reloaded
  '''
  package_name = root_module.__name__

  # get a reference to each loaded module
  loaded_package_modules = dict([
      (key, value) for key, value in sys.modules.items() 
      if key.startswith(package_name) and isinstance(value, types.ModuleType)])

  # delete references to these loaded modules from sys.modules
  for key in loaded_package_modules:
      del sys.modules[key]

  # load each of the modules again; 
  # make old modules share state with new modules
  for key in loaded_package_modules:
      print('loading %s' % key)
      newmodule = __import__(key)
      oldmodule = loaded_package_modules[key]
      oldmodule.__dict__.clear()
      oldmodule.__dict__.update(newmodule.__dict__)
    
  '''
  MATT ANDERSON CODE END
  '''

print("------ reloading packages -----")
reload_package(vec3)
reload_package(camera)
reload_package(AudioSegment)
print("------- reload finished -------\n")

def fpsFor(unit):
  return {
    "game":15.0,
    "film":24.0,
    "pal":25.0,
    "ntsc":30.0,
    "show":48.0,
    "palf":50.0,
    "ntscf":60.0
  }.get(unit,24.0)

def calculatePan(camName, objName):
  #Get the camera data from maya
  mayaCamPos = cmds.camera(camName,q=True,p=True)
  mayaCamUp = cmds.camera(camName,q=True,wup=True)
  mayaCamLook = cmds.camera(camName,q=True,wci=True)

  #Get the cube data
  mayaObjPos = cmds.xform(objName,q=True,t=True)

  #Convert the maya camera data to my vec3 type
  cameraPos = vec3.vec3(mayaCamPos[0],mayaCamPos[1],mayaCamPos[2])
  cameraUp = vec3.vec3(mayaCamUp[0],mayaCamUp[1],mayaCamUp[2])
  cameraLook = vec3.vec3(mayaCamLook[0] - cameraPos.x, mayaCamLook[1] - cameraPos.y, mayaCamLook[2] - cameraPos.z)
  cameraLook = vec3.normalize(cameraLook)
  worldUp = vec3.vec3(0,1,0)


  if(cameraUp == worldUp):
    cameraLR = vec3.normalize(vec3.cross(cameraLook,cameraUp))
  else:
    cameraLR = vec3.normalize(vec3.cross(worldUp,cameraUp))

  #Store this vec3 data in a camera class
  cam = camera.camera(cameraPos,cameraUp,cameraLR,cameraLook)
  #Convert the cube data
  objPosition = vec3.vec3(mayaObjPos[0],mayaObjPos[1],mayaObjPos[2])

  #Calculate the distance vector between the camera and the object
  distVector = vec3.normalize(objPosition - cam.pos)
  
  #Project the distance onto the camera's left & right vector
  projectOntoLR = vec3.dot(distVector,cam.lr)

  return projectOntoLR

def panSound():
  cmds.select("pCube1")
  firstKey = cmds.findKeyframe(timeSlider=True, which='first')
  lastKey = cmds.findKeyframe(timeSlider=True, which='last')

  unit = cmds.currentUnit(q=True,t=True)

  fps = fpsFor(unit)
  lengthOfFrame = 1000.0/fps
  
  if(platform.system() == "Windows"):
    soundClip = AudioSegment.from_mp3("E:/mattt/Documents/maya/scripts/Walking.mp3")
  elif(platform.system() == "Linux"):
    soundClip = AudioSegment.from_mp3("/home/i7626944/Documents/Innovations/MayaSound/Walking.mp3")
  

  #soundClip = AudioSegment.from_mp3("E:/mattt/Documents/maya/scripts/A3.mp3")

  newClip = AudioSegment.empty()
  oldSplit = 0
  currentSplit = lengthOfFrame
  lastVolume = 0

  tmpClip = AudioSegment.empty()
  tmpClip2 = AudioSegment.empty()

  if (len(soundClip) < (lastKey*lengthOfFrame)):
    print("sound > time")
      
    for frame in range (int(1),int(lastKey + 1)):
      cmds.currentTime(frame,edit=True)
      panValue = calculatePan("cameraShape1","pCube1")

      dist = getDistance("cameraShape1","pCube1")

      if (currentSplit >= len(soundClip)):
          tmpClip = soundClip[oldSplit:len(soundClip)].pan(panValue)
          volume = calculateVolumeChange(dist,soundClip,tmpClip)
      

          tmpClip2 = tmpClip + volume
        
          newClip += tmpClip2
          tmpClip2 = AudioSegment.empty()

          currentSplit = len(soundClip) - oldSplit
          oldSplit = 0        

      tmpClip += soundClip[oldSplit:currentSplit].pan(panValue)
      volume = calculateVolumeChange(dist,soundClip,tmpClip)

      tmpClip2 = tmpClip + volume
      newClip += tmpClip2

      lastVolume = volume
      tmpClip = AudioSegment.empty()
      tmpClip2 = AudioSegment.empty()
      oldSplit = currentSplit
      currentSplit += lengthOfFrame
      
  else:
    print("time > sound")
    
    for frame in range (1,int(lastKey + 1)):
      cmds.currentTime(frame,edit=True)
      panValue = calculatePan("cameraShape1","pCube1")

      dist = getDistance("cameraShape1","pCube1")

      tmpClip += soundClip[oldSplit:currentSplit].pan(panValue)

      volume = calculateVolumeChange(dist,soundClip,tmpClip)

      tmpClip2 = tmpClip + volume

      newClip += tmpClip2

      tmpClip = AudioSegment.empty()
      tmpClip2 = AudioSegment.empty()
      oldSplit = currentSplit
      currentSplit += lengthOfFrame

  if(platform.system() == "Windows"):
    newClip.export("E:/mattt/Documents/maya/scripts/WalkWithPan.wav",format="wav")
  elif(platform.system() == "Linux"):
    newClip.export("/home/i7626944/Documents/Innovations/MayaSound/pannedWalk.wav",format="wav")

  print("Sound file exported")

def getDistance(camName, objName):
  mayaCamPos = cmds.camera(camName,q=True,p=True)
  mayaObjPos = cmds.xform(objName,q=True,t=True)

  camPosition = vec3.vec3(mayaCamPos[0],mayaCamPos[1],mayaCamPos[2])
  objPosition = vec3.vec3(mayaObjPos[0],mayaObjPos[1],mayaObjPos[2])

  distance = vec3.dist(camPosition, objPosition)

  return distance

def calculateVolumeChange(distance,soundClip,adjustClip):
  
  loudness = soundClip.max_dBFS
  adLoudness = soundClip.max_dBFS

  if(distance < 1):
    distance = 1
    
  newLoudness = pow((10/distance),2) * loudness

  if(loudness < 0):
    loudnessChange = newLoudness - loudness
    newLoudness = loudness - loudnessChange

  returnVolume = newLoudness - loudness

  if(returnVolume > 7000):
    returnVolume = 5500

  testClip = adjustClip + returnVolume

  if(testClip.max_dBFS > adLoudness):
    returnVolume = 0

  return returnVolume


#panSound()



