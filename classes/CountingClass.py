import datetime

class Chickount:
    def __init__(self,uname,part, idRef, image, count, timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ):
        self.uname = uname
        self.part = part
        self.idRef = idRef
        self.image = image
        self.timestamp = timestamp
        self.count = count

    def __str__(self):

        return f"idRef: {self.idRef}, image: {self.image}, timestamp: {self.timestamp}, count: {self.count}"
    
    def __repr__(self):

        return f"idRef: {self.idRef}, image: {self.image}, timestamp: {self.timestamp}, count: {self.count}"
    
    def to_dict(self):
        return {
            "uname" : self.uname,
            "part" : self.part,
            "idRef": self.idRef,
            "image": self.image,
            "timestamp": self.timestamp,
            "count": self.count
        }