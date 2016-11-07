import math

class vec3:
  def __init__(self, x = 0.0, y = 0.0, z = 0.0):
    self.x = float(x)
    self.y = float(y)
    self.z = float(z)

  def __add__(self, value):
    return newPoint(self[0] + value[0], self[1] + value[1], self[2] + value[2])
  
  def __sub__(self, value):
    return newPoint(self[0] - value[0], self[1] - value[1], self[2] - value[2])

  def __iadd__(self, value):
    self.x = value[0] + self.x
    self.y = value[1] + self.y
    self.z = value[2] + self.z
    return self

  def __isub__(self, value):
    self.x = value[0] - self.x
    self.y = value[1] - self.y
    self.z = value[2] - self.z
    return self

  def __div__(self, value):
    return newPoint(self.x/value, self.y/value, self.z/value)

  def __mul__(self, value):
    return newPoint(self.x*value[0], self.y*value[1], self.z*value[2])

  def __idiv__(self, value):
    self[0] = self[0]/value
    self[1] = self[1]/value
    self[2] = self[2]/value
    return self

  def __imul__(self, value):
    self[0] = self[0]*value
    self[1] = self[1]*value
    self[2] = self[2]*value
    return self

  def __getitem__(self, key):
    if(key == 0):
      return self.x
    elif(key == 1):
      return self.y
    elif(key == 2):
      return self.z
    else:
      raise Exception("Invalid coordinate to vector")

  def __setitem__(self, key, value):
    if(key == 0):
      self.x = value
    elif(key == 1):
      self.y = value
    elif(key == 2):
      self.z = value
    else:
      raise Exception("Invalid coordinate to vector")
      
  def __str__(self):
    return "(" +str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

  def __eq__(self, value):
    if isinstance(value, vec3):
      return (self.x == value.x) and (self.y == value.y) and (self.z == value.z)

newPoint = vec3

def distSqr(p1, p2):
  return((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

def dist(p1, p2):
  return math.sqrt(distSqr(p1,p2))

def length(vec):
  return math.sqrt(vec.x**2 + vec.y**2 + vec.z**2)

def normalize(vec):
  if(vec.x == 0.0 and vec.y == 0.0 and vec.z == 0.0):
    return vec3(0,0,0)
  return vec/length(vec)

def dot(a, b):
  return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def project(a, b):
  return b * dot(a,b) / length(b)**2

def cross(a, b):
  return vec3((a[1]*b[2] - a[2]*b[1]), (a[2]*b[0] - a[0]*b[2]), (a[0]*b[1] - a[1]*b[0]))