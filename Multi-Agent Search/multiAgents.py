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

        value = successorGameState.getScore()

        ghostdist = manhattanDistance(newPos, newGhostStates[0].getPosition())
        capdist = [manhattanDistance(newPos,x) for x in successorGameState.getCapsules() ]
        fooddist = [manhattanDistance(newPos, x) for x in newFood.asList()]       #get a list here and use min in the below if condition

        if ghostdist > 0:                                                           #using reciprocal as suggested and performing a hit
            value -= 10 / (ghostdist)                                               #and trial beginning from 1.

        if len(fooddist) > 0:
            value += 10 / min(fooddist)

        #if len(capdist) > 0:                                                       #producing negative score
        #    value += 10 / min(capdist)

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
    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0                                                          # As given in the assignment, pacman is always 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def isTerminal(self, state, depth, agent):
        if state.isWin() or state.isLose() or self.depth == depth or state.getLegalActions(agent) == 0:
            return True
        return False

    def isPacman(self, state, agent):
        return agent % state.getNumAgents() == 0                                # As given in the assignment, pacman is always 0

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
        def minimax(state, depth, agent):
            #print 'agents start'
            #print agent
            #print 'agents count'
            #print state.getNumAgents()
            #print 'agents end'
            if agent == state.getNumAgents():
                return minimax(state, depth + 1, 0)

            if self.isTerminal(state, depth, agent):
                return self.evaluationFunction(state)

            suc = (minimax(state.generateSuccessor(agent, action), depth, agent + 1) for action in state.getLegalActions(agent))

            if self.isPacman(state, agent):
                return max(suc)                                                     #using inbuilt max and min functions rather than doing it
            else:                                                                   #explicitly like done in the assignment
                return min(suc)

        #return max([minimax(gameState.generateSuccessor(0, action), 0, 1) for action in gameState.getLegalActions(0)]) #not working. PLease fing the reason
        return max(gameState.getLegalActions(0),key = lambda x: minimax(gameState.generateSuccessor(0, x), 0, 1)) #reference https://www.programiz.com/python-programming/methods/built-in/max

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = float("-inf")
        beta = float("inf")

        def max_value(gameState, depth, alpha, beta):
          actions = gameState.getLegalActions(0)
          if not actions or depth < 0:
            return (self.evaluationFunction(gameState), None)
          else:
            v = float("-inf")
            best_action = None
            for action in actions:
              temp = min_value(1, gameState.generateSuccessor(0, action), depth, alpha, beta)[0] #increment agent to min
              if v < temp:
                v = temp
                best_action = action
              if v > beta:
                return (v, best_action)
              alpha = max(alpha, v)
            return (v, best_action)

        def min_value(agentIndex, gameState, depth, alpha, beta):
          actions = gameState.getLegalActions(agentIndex)
          if not actions or depth < 0:
            return (self.evaluationFunction(gameState), None)
          next_agent = (agentIndex + 1) % gameState.getNumAgents()
          v = float("inf")
          best_action = None
          for action in actions:
            temp = next_value(next_agent, gameState.generateSuccessor(agentIndex, action), depth, alpha, beta)[0]
            if v > temp:
              v = temp
              best_action = action
            if v < alpha:
              return (v, best_action)
            beta = min(beta, v)
          return (v, best_action)

        def next_value(agentIndex, gameState, depth, alpha, beta):
          if agentIndex == 0:
            return max_value(gameState, depth - 1, alpha, beta)
          else:
            return min_value(agentIndex, gameState, depth, alpha, beta)

        return next_value(self.index, gameState, self.depth, alpha, beta)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0                                                           # As given in the assignment, pacman is always 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def isTerminal(self, state, depth, agent):
        if state.isWin() or state.isLose() or self.depth == depth or state.getLegalActions(agent) == 0:
            return True
        return False

    def isPacman(self, state, agent):
        return agent % state.getNumAgents() == 0                                 # As given in the assignment, pacman is always 0


    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(state, depth, agent):
            if agent == state.getNumAgents():
                return expectimax(state, depth + 1, 0)

            if self.isTerminal(state, depth, agent):
                return self.evaluationFunction(state)

            suc = [expectimax(state.generateSuccessor(agent, action), depth, agent + 1) for action in state.getLegalActions(agent)]
                                                                                #use similar logic to minimax but as list as we need length to take average
            if self.isPacman(state, agent):
                return max(suc)                                                     #using inbuilt max and min functions rather than doing it
            else:                                                                   #explicitly like done in the assignment
                return sum(suc)/len(suc)                                            #Average needs to be used instead of minimum (here there is no probablity given)
                                                                                    #ASK: why is sum(suc) passing the test
        #x= gameState.getLegalActions(0)
        return max(gameState.getLegalActions(0),key = lambda x: expectimax(gameState.generateSuccessor(0, x), 0, 1))

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()                               #Use currentgame state as its and current evaluation function. unlike reflex.
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"

    value = currentGameState.getScore()
    capdist = [manhattanDistance(newPos,x) for x in currentGameState.getCapsules() ]
    fooddist = [manhattanDistance(newPos, x) for x in newFood.asList()]         #get a list here and use min in the below if condition

    gvalue = 0
    for ghost in newGhostStates:
        ghostdist = manhattanDistance(newPos, newGhostStates[0].getPosition())
        if ghostdist > 0:
            if ghost.scaredTimer > 0:                                           # Adding scared timer here for oppotunistic chance -> if ghost is scared
                gvalue += 100 / ghostdist
            else:
                gvalue -= 10 / ghostdist
    value += gvalue

    if len(fooddist) > 0:
        value += 10 / min(fooddist)

    #if len(capdist) > 0:                                                       #producing negative score and giving 5/6. Clarify with TA the reason after debugging yourself.
    #    value += 10 / min(capdist)

    return value

# Abbreviation
better = betterEvaluationFunction
