from cmd import Cmd
import os
import sys

class ImageEnhancement(Cmd):
    intro = '''====Image enhancement, designed by "Searching Center, Energysh"====
    Type help or ? to list commands.
    '''
    def do_adjust(self, argv):
        '''input 3 parameter: filepath adjust_name video_status
    filepath,
    adjust name(snow_scene, forest_scene, asian, white, black... ),
    video status:(Pause, Resume)'''

        parameters = argv.split(' ')

        if parameters and parameters[0] != "exit" and len(parameters) == 3:
            print("Run adjust...")

    def do_exit(self, arg):
        'Stop run'
        print('Stop running')
        # self.close()
        return True

if __name__ == '__main__':
    ImageEnhancement().cmdloop()