import numpy as np

def rotate(face, variation):
    match variation:
        case None:
            face = np.rot90(face, k=1, axes=(1,0))
        case "prime":
            face = np.rot90(face, k=-1, axes=(1,0))
        case "double":
            face = np.rot90(face, k=2, axes=(1,0))

    return face


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

    def __init__(self,currentstate=initialState.copy()):
        self.currentstate = currentstate

    def check(self):
        if (self.currentstate == self.initialState).all():
            print("Cube is solved!")
        else:
            print("Cube is still scrambled!")

    def U(self,variation=None):

        # create up/down flipped matrix to form the upper face as seen from the front
        upperFace = self.currentstate[2,0,:]
        for i in reversed(range(0,2)):
            upperFace = np.vstack((upperFace, self.currentstate[i,0,:]))


        upperFace = rotate(upperFace,variation)

        # unflip the matrix to reinsert into the state
        upperFace = np.flipud(upperFace)
        for i in reversed(range(0,3)):
            self.currentstate[i,0,:] = upperFace[i,:]

    def R(self, variation=None):
        rightFace = self.currentstate[0,:,2]
        for i in range (1,3):
            rightFace = np.column_stack((rightFace,self.currentstate[i,:,2]))

        rightFace = rotate(rightFace,variation)

        for i in range (0,3):
            self.currentstate[i,:,2] = rightFace[:,i]

    def move(self, direction):
        match direction:
            case "U":
                self.U()
            case "U'":
                self.U("prime")
            case "U2":
                self.U("double")
            case "R":
                self.R()
            case "R'":
                self.R("prime")
            case "R2":
                self.R("double")

rubikcube = cube()
rubikcube.move("U")
rubikcube.check()
print(rubikcube.currentstate)
#print("initial state: \n",rubikcube.initialState)
