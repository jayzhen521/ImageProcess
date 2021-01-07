import json
import sys
import os
sys.path.append(os.path.split(os.path.abspath(__file__))[0] + "/../processor")

d={"snow_scene": [{"unsharpenmask": {"ksize": 5, "sigma": 0, "weight": 0.0}},{"adapthisteq": {"clipLimit": 0.01, "tilesRow": 8, "tilesColumn": 8}},{"vibrance": {"intensity": 0.0}},{"adjustbright": {"delta": 0.0}}]}
print(json.dumps(d,ensure_ascii=False,indent=4))  #字典转成json,字典转换成字符串 加上ensure_ascii=False以后，可以识别中文， indent=4是间隔4个空格显示

import framecontrol

frameControl = framecontrol.framecontrol()

# for attr in dir(frameControl):
#     print(attr)

myClassDict = frameControl.__dict__

print(myClassDict)

myClassJson = json.dumps(myClassDict)

print(myClassJson)

# write
with open("write_test.txt", "w") as f:
    f.write(myClassJson)