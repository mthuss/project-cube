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

    def R(self, variation=None):
        rightFace = self.currentstate[0,:,2]
        for i in range (1,3):
            rightFace = np.column_stack((rightFace,self.currentstate[i,:,2]))

        match variation:
            case None:
                rightFace = np.rot90(rightFace, k=1, axes=(1,0))
            case "prime":
                rightFace = np.rot90(rightFace, k=-1, axes=(1,0))
            case "double":
                rightFace = np.rot90(rightFace, k=2, axes=(1,0))

        for i in range (0,3):
            self.currentstate[i,:,2] = rightFace[:,i]

    def move(self, direction):
        match direction:
            case "R":
                self.R()
            case "R'":
                self.R("prime")
            case "R2":
                self.R("double")

rubikcube = cube()
rubikcube.move("R'")
print(rubikcube.currentstate)
