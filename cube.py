import numpy as np
import random
import re
import hashlib

SCRAMBLE_STEPS = 2
MAX_STEPS = 20
NUM_SOLUTIONS = 6

# list of all possible moves
movement_chart = ("U","D","R","L","F","B", 
                  "U'","D'","R'","L'","F'","B'",
                  "U2","D2","R2","L2","F2","B2")

def rotate(face, variation):
    match variation:
        case None:
            face = np.rot90(face, k=1, axes=(1,0))
        case "prime":
            face = np.rot90(face, k=-1, axes=(1,0))
        case "double":
            face = np.rot90(face, k=2, axes=(1,0))

    return face

# gets a scrambling sequence and returns the inverse sequence
def getSolutionfromScramble(move_list):
    movement_list = list(reversed(move_list))
    for i in range(0,len(movement_list)):
        if chr(39) in movement_list[i]:
            movement_list[i] = movement_list[i].replace("'","")

        else:
            if "2" not in movement_list[i]:
                movement_list[i] = movement_list[i] + "'"

    return movement_list

# this is what the cube looks like when solved
# (as seen from the front)
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
        self.scrambledState = None
        self.testedSolutions = set()
        self.solutions = list()

    def scramble(self):
        move_list = self.getCombination(SCRAMBLE_STEPS)
        for movement in move_list:
            self.move(movement)

        self.scrambledState = self.currentstate.copy()
        return move_list

    def check(self):
        if (self.currentstate == solvedState).all():
            print("Solution found!")
            return True
        else:
            return False

    def getCombination(self, size):
        move_list = []
        move_list.append(random.choice(movement_chart))
        i = 1
        while i < size:
            while True:
                movement = random.choice(movement_chart)
                # prevent redundant full face turns
                if "2" in movement and movement != move_list[-1]:
                    break
                if "2" not in movement and movement != move_list[-1]:
                    if ("'" in movement and movement.replace("'","") != move_list[-1]) or ("'" not in movement and (movement + "'") != move_list[-1]):
                        break
#                   convert consecutive X moves into one X2 move
#                    if movement == move_list[-1]:
#                        movement = move_list.pop().replace("'","") + "2"
#                        print(f"Turned {move_list[-1]} at position {i} into {movement}")
#                        i -= 1

            move_list.append(movement)
            i+=1

        return tuple(move_list)

    def solve(self):
        iterations = 0
        repeated = 0 # counts how many times a repeated combination has been tested consecutively
        size = 1
        
        # it's safe to assume that you most likely can't find a 
        # solution that takes less steps than it takes to scramble the cube.
        # (can technically happen, especially with X2's being counted
        # as a single move, but still rather unlikely)
        # uncomment this if you want a faster but unfair bruteforcer
        # (also, might actually make it slower in some cases)
        #size = SCRAMBLE_STEPS

        while True:
            # reset currentstate to the original scrambled state for a new attempt
            self.currentstate = self.scrambledState.copy()

            # get new combination and compute its hash
            combination = self.getCombination(size)
            combination_hash = hashlib.md5(repr(combination).encode()).hexdigest()

            # check if received combination hasn't been tested yet
            # there might just be something wrong with this here function...
            if combination_hash not in self.testedSolutions:
                repeated = 0 # resets counter
                iterations += 1

                # add combination's hash to set of tested combinations
                self.testedSolutions.add(combination_hash)
                #print("Testing ", combination)
                #print(combination_hash)

                # test combination
                for movement in combination:
                    self.move(movement)

                # check if tested combination actually solved the cube
                if self.check():
                    self.solutions.append(combination)
                    if len(self.solutions) == NUM_SOLUTIONS:
                        return iterations
            else:
                repeated += 1
                # increase size of combination arrays if no new
                # combinations have been found for a certain number of iterations
                # (18*size: made-up heuristic number)
                if size <= MAX_STEPS and repeated >= 18*size:
                    size += 1

    #----------------#
    # CUBE MOVEMENTS #
    #----------------#

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
rubikcube.testedSolutions.add(hashlib.md5(repr(tuple(solution_steps)).encode()).hexdigest())

print("Now solving...")
iterations = rubikcube.solve()

print("Number of iterations: ", iterations)
print("Scrambled cube (as seen from the front): \n", rubikcube.scrambledState)
print("\nScrambling steps: ", scramble_steps)
if len(solution_steps) <= MAX_STEPS:
    print("\nTrivial solution: ", solution_steps)

if len(rubikcube.solutions) == 0:
    print("\nNo solutions found!")
else: 
    print("\nSolutions: ")
    for sol in rubikcube.solutions:
        print(sol)

