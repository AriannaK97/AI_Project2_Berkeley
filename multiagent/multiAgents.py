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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        FoodList = newFood.asList()
        newGhostPositions = successorGameState.getGhostPositions()  # getGhostPositions() function in file pacman.py
        foodDist = []
        points = 0          #collecting points that show weather a move is better than another,
                            # the more the points the better the move


        #calculating all food distances from newPos
        for food in FoodList:
            foodDist.append(manhattanDistance(newPos, food))

        for i in foodDist:
            if i <= 4:
                points += 1
            elif i <= 15 and i > 4 :
                 points += 0.2
            else:
                points += 0.15

        for ghost in newGhostPositions:
            if ghost == newPos:
                points = 2 - points
            if manhattanDistance(newPos, ghost) <= 3.5:
                points = 1 - points

        return successorGameState.getScore() + points




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
        """
        "*** YOUR CODE HERE ***"


        def MiniMaxDecision(self, gameState, agent, depth):

            if agent == gameState.getNumAgents()-1:
                agent = self.index
                depth += 1
            else:
                agent += 1

            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return [Directions.STOP, self.evaluationFunction(gameState)]

            if agent == self.index:
                return maxValue(self, gameState, agent, depth)
            else:
                return minValue(self, gameState, agent, depth)


        def maxValue(self, gameState, agent, depth):
           # v = "", float ("-inf")
            v = []
            if gameState.isLose() or gameState.isWin():
                return [Directions.STOP, self.evaluationFunction(gameState)]

            for action in gameState.getLegalActions(agent):
                newValue = MiniMaxDecision(self, gameState.generateSuccessor(agent,action),agent,depth)
                if not v:
                    v.append(action)
                    v.append(newValue[1])

                else:
                    newV = max(v[1], newValue[1])

                    if newV is newValue[1]:
                        v[0] = action
                        v[1] = newV
               # print "max = ", v, "\n"




            return v


        def minValue(self, gameState, agent, depth):
            #v = "", float ("inf")
            v = []
            if gameState.isLose() or gameState.isWin():
                return [Directions.STOP, self.evaluationFunction(gameState)]

            for action in gameState.getLegalActions(agent):
                newValue = MiniMaxDecision(self, gameState.generateSuccessor(agent,action),agent,depth)
                if not v:
                    v.append(action)
                    v.append(newValue[1])

                else:
                    newV = min(v[1], newValue[1])

                    if newV is newValue[1]:
                        v[0] = action
                        v[1] = newV
                    #print "min = ", v, "\n"
                    # if not v:
                    #    v.append(action)
                    #    v.append(newValue)

                    # else:

            return v

        return MiniMaxDecision(self, gameState, self.index - 1, 0)[0]


    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

