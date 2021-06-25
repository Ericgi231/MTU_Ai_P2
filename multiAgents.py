# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        oldPowers = currentGameState.getCapsules()

        #stopping is bad, gotta go fast
        if action == "Stop":
            return -1000

        #we are always looking for the action that gives the best score or the best access to more score
        value = successorGameState.getScore()

        #if food was found with action, score increases by 10
        #we do not want moves to exceed a score increase of 10 unless better than eating a pellet

        #increase score based on min distance to a dot after action
        min = 9999
        for foodPos in newFood.asList():
            dist =+ manhattanDistance(foodPos, newPos)
            if dist < min:
                min = dist
        value += 9 / min

        #mod score based on distance to power up
        if (len(oldPowers) > 0):
            min = 9999
            for powerPos in oldPowers:
                dist = manhattanDistance(powerPos, newPos)
                if dist < min:
                    min = dist
            value += 100 / (min + 1)

        #mod score based on distance to ghost, based on if powered up
        for ghost in newGhostStates:
            #if ghost scared long enough to reach it, and is close, attack
            dist = manhattanDistance(ghost.getPosition(), newPos)
            if (ghost.scaredTimer > dist):
                if (dist <= 1):
                    value += 500
                else:
                    value += 100 / dist
            else:
                #if action would land on ghost, do not
                if (dist <= 1):
                    value -= 1000

        return value

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        bestAction = actions[0]
        bestValue = -99999
        for action in actions:
            next = gameState.generateSuccessor(0, action)
            value = self.minNode(next, 1)
            if value > bestValue:
                bestAction = action
                bestValue = value

        return bestAction

    def maxNode(self, gameState, level):
        if (level/gameState.getNumAgents() == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        
        index = level % gameState.getNumAgents()
        actions = gameState.getLegalActions(index)
        v = -99999

        for action in actions:
            next = gameState.generateSuccessor(index, action)
            v = max(v, self.minNode(next, level+1))

        return v

    def minNode(self, gameState, level):
        if (level/gameState.getNumAgents() == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        
        index = level % gameState.getNumAgents()
        actions = gameState.getLegalActions(index)
        v = 99999

        for action in actions:
            next = gameState.generateSuccessor(index, action)
            if(index == gameState.getNumAgents()-1):
                v = min(v, self.maxNode(next, level+1))
            else:
                v = min(v, self.minNode(next, level+1))

        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        bestAction = actions[0]
        bestValue = -99999
        a = -99999
        b = 99999
        for action in actions:
            next = gameState.generateSuccessor(0, action)
            val = self.minNode(next, 1, a, b)
            if val >= b:
                return bestAction
            a = max(a, val)
            if val > bestValue:
                bestAction = action
                bestValue = val
            

        return bestAction

    def maxNode(self, gameState, level, a, b):
        if (level/gameState.getNumAgents() == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        
        index = level % gameState.getNumAgents()
        actions = gameState.getLegalActions(index)
        v = -99999

        for action in actions:
            next = gameState.generateSuccessor(index, action)
            v = max(v, self.minNode(next, level+1, a, b))
            if v > b:
                return v
            a = max(a, v)
            
        return v

    def minNode(self, gameState, level, a, b):
        if (level/gameState.getNumAgents() == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        
        index = level % gameState.getNumAgents()
        actions = gameState.getLegalActions(index)
        v = 99999

        for action in actions:
            next = gameState.generateSuccessor(index, action)
            if(index == gameState.getNumAgents()-1):
                v = min(v, self.maxNode(next, level+1, a, b))
            else:
                v = min(v, self.minNode(next, level+1, a, b))
            if v < a:
                return v
            b = min(b, v)

        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        bestAction = actions[0]
        bestValue = -99999
        for action in actions:
            next = gameState.generateSuccessor(0, action)
            value = self.avgNode(next, 1)
            if value > bestValue:
                bestAction = action
                bestValue = value

        return bestAction

    def maxNode(self, gameState, level):
        if (level/gameState.getNumAgents() == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        
        index = level % gameState.getNumAgents()
        actions = gameState.getLegalActions(index)
        v = -99999

        for action in actions:
            next = gameState.generateSuccessor(index, action)
            v = max(v, self.avgNode(next, level+1))

        return v

    def avgNode(self, gameState, level):
        if (level/gameState.getNumAgents() == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        
        index = level % gameState.getNumAgents()
        actions = gameState.getLegalActions(index)
        vals = []

        for action in actions:
            next = gameState.generateSuccessor(index, action)
            if(index == gameState.getNumAgents()-1):
                vals.append(self.maxNode(next, level+1))
            else:
                vals.append(self.avgNode(next, level+1))

        return sum(vals) / float(len(vals))


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: e
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()

    #win loss data
    if currentGameState.isLose():
        return -99999
    elif currentGameState.isWin():
        return 99999

    #food data
    minFoodDistance = 99999
    foods = currentGameState.getFood().asList()
    for food in foods:
        minFoodDistance = min(minFoodDistance, manhattanDistance(food, pos))

    #power up data
    minPowerUpDistance = 99999
    powerUps = currentGameState.getCapsules()
    if powerUps:
        for powerUp in powerUps:
            minPowerUpDistance = min(minPowerUpDistance, manhattanDistance(powerUp, pos))
    else:
        minPowerUpDistance = 0

    #ghost data
    ghosts = currentGameState.getGhostStates()
    aGhosts, sGhosts = [], []
    for ghost in ghosts:
        if ghost.scaredTimer:
            sGhosts.append(ghost)
        else:
            aGhosts.append(ghost)

    aGhostMin, sGhostMin = 99999, 99999
    if aGhosts:
        for ghost in aGhosts:
            aGhostMin = min(aGhostMin, manhattanDistance(ghost.getPosition(), pos))

    if sGhosts:
        for ghost in sGhosts:
            sGhostMin = min(sGhostMin, manhattanDistance(ghost.getPosition(), pos))
    else:
        sGhostMin = 0

    #linear combination
    value = scoreEvaluationFunction(currentGameState)
    value -= 3    * (1./aGhostMin)      #lower = bad
    value -= 2    * sGhostMin           #lower = good
    value -= 0.05 * minPowerUpDistance  #lower = good
    value -= 100  * len(powerUps)       #lower = good
    value -= 1    * minFoodDistance     #lower = good
    value -= 4    * len(foods)          #lower = good

    return value

# Abbreviation
better = betterEvaluationFunction
