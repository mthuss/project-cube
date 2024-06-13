import numpy as np
import random
import re

SCRAMBLE_STEPS = 10

movement_chart = ["U","D","R","L","F","B", 
                  "U'","D'","R'","L'","F'","B'",
                  "U2","D2","R2","L2","F2","B2"]


def rotate(face, variation):
    match variation:
        case None:
            face = np.rot90(face, k=1, axes=(1,0))
        case "prime":
            face = np.rot90(face, k=-1, axes=(1,0))
        case "double":
            face = np.rot90(face, k=2, axes=(1,0))

    return face

def getSolutionfromScramble(move_list):
    movement_list = list(reversed(move_list))
    for i in range(0,len(movement_list)):
        if chr(39) in movement_list[i]:
            movement_list[i] = movement_list[i].replace("'","")

        else:
            if "2" not in movement_list[i]:
                movement_list[i] = movement_list[i] + "'"

    return movement_list


class cube:
    initialState = np.array([
                    # front layer
                    [['A','B','C'],
                     ['D','E','F'],
                     ['G','H','I']],

                    # middle layer
                    [['J','K','L'],
                     ['M', 0 ,'N'],
                     ['O','P','Q']],
                    
                    # back layer
                    [['R','S','T'],
                     ['U','V','W'],
                     ['X','Y','Z']]
                    ])

    def __init__(self,currentstate=initialState.copy()):
        self.currentstate = currentstate

    def scramble(self):
        move_list = []
        for i in range(0,SCRAMBLE_STEPS):
            movement = random.choice(movement_chart)
            self.move(movement)
            move_list.append(movement)

        return move_list


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

    def D(self, variation=None):
        bottomFace = self.currentstate[0,2,:]
        for i in range(1,3):
            bottomFace = np.vstack((bottomFace, self.currentstate[i,2,:]))

        bottomFace = rotate(bottomFace, variation)

        for i in range(0,3):
            self.currentstate[i,2,:] = bottomFace[i,:]

    def R(self, variation=None):
        rightFace = self.currentstate[0,:,2]
        for i in range (1,3):
            rightFace = np.column_stack((rightFace,self.currentstate[i,:,2]))

        rightFace = rotate(rightFace,variation)

        for i in range (0,3):
            self.currentstate[i,:,2] = rightFace[:,i]

    def L(self, variation=None):
        leftFace = self.currentstate[0,:,0]
        for i in range(1,3):
            leftFace = np.column_stack((leftFace, self.currentstate[i,:,0]))

        leftFace = rotate(leftFace, variation)

        for i in range(0,3):
            self.currentstate[i,:,0] = leftFace[:,i]

    def F(self, variation=None):
        self.currentstate[0] = rotate(self.currentstate[0], variation)

    def B(self, variation=None):
        match variation:
            case None:
                self.currentstate[2] = np.rot90(self.currentstate[2], k=-1, axes=(1,0))
            case "prime":
                self.currentstate[2] = np.rot90(self.currentstate[2], k=1, axes=(1,0))
            case "double":
                self.currentstate[2] = np.rot90(self.currentstate[2], k=2, axes=(1,0))

    def move(self, direction):
        match direction:
            case "U":
                self.U()
            case "U'":
                self.U("prime")
            case "U2":
                self.U("double")
            case "D":
                self.D()
            case "D'":
                self.D("prime")
            case "D2":
                self.D("double")
            case "R":
                self.R()
            case "R'":
                self.R("prime")
            case "R2":
                self.R("double")
            case "L":
                self.L()
            case "L'":
                self.L("prime")
            case "L2":
                self.L("double")
            case "F":
                self.F()
            case "F'":
                self.F("prime")
            case "F2":
                self.F("double")
            case "B":
                self.B()
            case "B'":
                self.B("prime")
            case "B2":
                self.B("double")


rubikcube = cube()
scramble_steps = rubikcube.scramble()
solution_steps = getSolutionfromScramble(scramble_steps)
print("Scrambled cube (as seen from the front): \n", rubikcube.currentstate)
print("\nScrambling steps: ", scramble_steps)
print("\nSteps for unscrambling: ", solution_steps)

print("\nNow solving...")
for i in solution_steps:
    rubikcube.move(i)

rubikcube.check()
#print("initial state: \n",rubikcube.initialState)
