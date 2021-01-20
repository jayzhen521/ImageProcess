from adapthisteq import adapthisteq
from adjustbright import adjustbright
from autocontrasteq import autocontrasteq
from BrightnessContrast import BrightnessContrast
from guidefilter import guidefilter
from unsharpenmask import unsharpenmask
from vibrance import vibrance
from HSVAdjuster import HSVAdjuster
from AutoBrightnessContrast import AutoBrightnessContrast

class AdjusterFactory():

    # defaultAdjustersNames = ["vibrance", "BrightnessContrast", "unsharpenmask"]

    defaultAdjustersNames = ["AutoBrightnessContrast", "unsharpenmask"]
    
    # defaultAdjustersNames = ["HSVAdjuster", "BrightnessContrast", "unsharpenmask"]


    @staticmethod
    def createAdjuster(adjusterName, inDict = []):
        adjuster = None
        if adjusterName == "adapthisteq":
            adjuster = adapthisteq()
        elif adjusterName == "adjustbright":
            adjuster = adjustbright()
        elif adjusterName == "autocontrasteq":
            adjuster = autocontrasteq()
        elif adjusterName == "BrightnessContrast":
            adjuster = BrightnessContrast()
        elif adjusterName == "guidefilter":
            adjuster = guidefilter()
        elif adjusterName == "unsharpenmask":
            adjuster = unsharpenmask()
        elif adjusterName == "vibrance":
            adjuster = vibrance()
        elif adjusterName == "AutoBrightnessContrast":
            adjuster = AutoBrightnessContrast()
        elif adjusterName == "HSVAdjuster":
            adjuster = HSVAdjuster()

        if adjuster and inDict:
            adjuster.__dict__ = inDict

        return adjuster
        
