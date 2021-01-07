import json

class rw:
    # def write(self, to, by):
    #     dataJson = json.dumps(self.__dict__)
    #     resultJson = "{\"" + self.__class__.__name__ + "\": " + dataJson + "}"

    #     print(self.__dict__)

    #     with open(to, by) as f:
    #         f.write(resultJson)

    def getData(self):
        dataJson = json.dumps(self.__dict__)
        resultJson = "{\"" + self.__class__.__name__ + "\": " + dataJson + "}"
        return resultJson
        