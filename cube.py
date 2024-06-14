import numpy as np
import random
import re
import hashlib

SCRAMBLE_STEPS = 5
MAX_STEPS = 10

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

solvedState = np.array([
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

class cube:

    def __init__(self,currentstate=solvedState.copy()):
        self.currentstate = currentstate
        self.previousMovement = -1
        self.scrambledState = None
        self.testedSolutions = set()

    def scramble(self):
        move_list = self.getCombination(SCRAMBLE_STEPS)
        for movement in move_list:
            self.move(movement)

        self.scrambledState = self.currentstate.copy()
        return move_list

    def check(self):
        if (self.currentstate == solvedState).all():
            print("Cube is solved!")
            return True
        else:
            print("Cube is still scrambled!")
            return False

    def getCombination(self, size):
        move_list = []
        i = 0
        while i < size:
            while True:
                movement = random.choice(movement_chart)
                # prevent redundant full turns
                if "2" in movement and movement != self.previousMovement:
                    break
                if "2" not in movement and movement != self.previousMovement:
#                    if movement == self.previousMovement:
#                        movement = move_list.pop().replace("'","") + "2"
#                        print(f"Turned {self.previousMovement} at position {i} into {movement}")
#                        i -= 1
#                        if movement == move_list[-1]:
                    if ("'" in movement and movement.replace("'","") != self.previousMovement) or ("'" not in movement and (movement + "'") != self.previousMovement):
#                        print(f"{self.previousMovement} was undone by {movement} at position {len(move_list)}")
                        break

            self.previousMovement = movement
            move_list.append(movement)
            i+=1

        return tuple(move_list)

    def solve(self):
        iterations = 0
        repeated = 0 # counts how many times a repeated combination has been tested consecutively
        size = 1
        
        # size = SCRAMBLE_STEPS
        while True:
            # reset currentstate to the original scrambled state for a new attempt
            self.currentstate = self.scrambledState.copy()

            # get new combination and compute its hash
            #combination = self.getCombination(MAX_STEPS)
            combination = self.getCombination(size)
            combination_hash = hashlib.md5(repr(combination).encode()).hexdigest()

            # check if received combination has already been tested
            if combination_hash not in self.testedSolutions:
                repeated = 0 # resets counter
                iterations += 1

                # add combination's hash to set of tested combinations
                self.testedSolutions.add(combination_hash)
                print("Testing ", combination)
                print(combination_hash)

                # test combination
                for movement in combination:
                    self.move(movement)

                # tested combination actually solved the cube
                if self.check():
                    print("Solution: ", combination)
                    print("Iterations: ", iterations)
                    return
            else:
                repeated += 1
                if repeated >= 18*size:
                    size += 1

                print("Repeated: ", repeated)





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
#rubikcube.testedSolutions.add(hash(tuple(solution_steps)))
iterations = rubikcube.solve()
print("Number of iterations: ", iterations)
print("Scrambled cube (as seen from the front): \n", rubikcube.scrambledState)
print("\nScrambling steps: ", scramble_steps)
print("\nSteps for unscrambling: ", solution_steps)
print("\n\nLength: ", len(solution_steps))

print("\nNow solving...")
#for i in solution_steps:
#    rubikcube.move(i)

#print("initial state: \n",rubikcube.initialState)
