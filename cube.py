import numpy as np

class cube:
    initialState = np.array([
                    [['A','B','C'],
                     ['D','E','F'],
                     ['G','H','I']],

                    [['J','K','L'],
                     ['M', 0 ,'N'],
                     ['O','P','Q']],

                    [['R','S','T'],
                     ['U','V','W'],
                     ['X','Y','Z']]
                    ])

    def __init__(self,currentstate=initialState):
        self.currentstate = currentstate
    def move(self, direction):
        match direction:
            case "R":
                rightFace = self.currentstate[0,:,2]
                for i in range (1,3):
                    rightFace = np.column_stack((rightFace,self.currentstate[i,:,2]))
                print(rightFace)
                print(np.rot90(rightFace, k=1, axes=(1,0)))

rubikcube = cube()
rubikcube.move("R")
