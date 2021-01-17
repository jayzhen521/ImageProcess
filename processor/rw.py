import json
import cv2

class rw:
    # def write(self, to, by):
    #     dataJson = json.dumps(self.__dict__)
    #     resultJson = "{\"" + self.__class__.__name__ + "\": " + dataJson + "}"

    #     print(self.__dict__)

    #     with open(to, by) as f:
    #         f.write(resultJson)

    def getData(self):
        return {self.__class__.__name__: self.__dict__}

    def __str__(self):
        return self.__class__.__name__

    def getAdjustFunc(self):
        pass

class Serializer():

    @staticmethod
    def obj2Dict(obj):
        d = {}
        d['__class__'] = obj.__class__.__name__
        d['__module__'] = obj.__module__
        d.update(obj.__dict__)
        return d

    @staticmethod
    def dict2Obj(d):
        if '__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            class_ = getattr(module, class_name)
            args = dict((key.encode('ascii'), value) for key, value in d.items())
            instance = class_(**args)
        else:
            instance = d
        return instance


        