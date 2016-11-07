import vec3

class camera:
  def __init__(self, pos, up, lr, look):
    self.pos = vec3.vec3(pos[0],pos[1],pos[2])
    self.up = vec3.vec3(up[0],up[1],up[2])
    self.lr = vec3.vec3(lr[0],lr[1],lr[2])
    self.look = vec3.vec3(look[0],look[1],look[2])
  
  def __getitem__(self, key):
    if(key == 0 or key == "pos"):
      return self.pos
    elif(key == 1 or key == "up"):
      return self.up
    elif(key == 2 or key == "lr"):
      return self.lr
    elif(key == 3 or key == "look"):
      return self.look
    else:
      raise Exception("Invalid get for camera")

  def __setitem__(self, key, value):
    if(key == 0 or key == "pos"):
      self.pos = value
    elif(key == 1 or key == "up"):
      self.up = value
    elif(key == 2 or key == "lr"):
      self.lr = value
    elif(key == 3 or key == "look"):
      self.look = value
    else:
      raise Exception("Invalid get for camera")

  def __str__(self):
    return "Position = " + str(self.pos) + "\nUp = " + str(self.up) + "\nLeft -> Right = " + str(self.lr)+ "\nLook = " + str(self.look)
