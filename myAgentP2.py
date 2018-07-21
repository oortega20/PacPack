# myAgentP2.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
# This file was based on the starter code for student bots, and refined
# This file was based on the starter code for student bots, and refined
# by Mesut (Xiaocheng) Yang


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import nearestPoint

#########
# Agent #
#########


class myAgentP2(CaptureAgent):
  """
  YOUR DESCRIPTION HERE
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    # Make sure you do not delete the following line.
    # If you would like to use Manhattan distances instead
    # of maze distances in order to save on initialization
    # Make sure you do not delete the following line.
    # If you would like to use Manhattan distances instead
    # of maze distances in order to save on initialization
    # time, please take a look at:
    # CaptureAgent.registerInitialState in captureAgents.py.
    CaptureAgent.registerInitialState(self, gameState)
    self.start = gameState.getAgentPosition(self.index)

    otherAgentActions = self.receivedInitialBroadcast
    teammateIndices = [index for index in self.getTeam(gameState) if index != self.index]
    assert len(teammateIndices) == 1
    teammateIndex = teammateIndices[0]
    otherAgentPositions = getFuturePositions(gameState, otherAgentActions, teammateIndex)

    # You can process the broadcast here!
    #iterat through other agent positions -- if he picks up food, you dont need to go to those spaces
    friend= []
    foodPos = gameState.getFood()
    for i in otherAgentPositions:
        if i in foodPos:
            friend.append(i)
    #friend is an array showing which food pellets the other agent eats

    myFood = []
    for i in foodPos:
        if i not in friend:
            myFood.append(i)
    #myFood is the food pellets im going to go after
    # You can process the broadcast here!

  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    return random.choice(actions)



def getFuturePositions(gameState, plannedActions, agentIndex):
  """
  Returns list of future positions given by a list of actions for a
  specific agent starting form gameState

  NOTE: this does not take into account other agent's movements
  (such as ghosts) that might impact the *actual* positions visited
  by such agent
  """
  if plannedActions is None:
    return None

  planPositions = [gameState.getAgentPosition(agentIndex)]
  for action in plannedActions:
    if action in gameState.getLegalActions(agentIndex):
      gameState = gameState.generateSuccessor(agentIndex, action)
      planPositions.append(gameState.getAgentPosition(agentIndex))
    else:
      print("Action list contained illegal actions")
      break
  return planPositions


  def getFeatures(self, gamestate, action):
      features = util.Counter()
      successorGameState = gameState.generateSuccessor(self.index, action)
      newPos = successorGameState.getAgentPosition(self.index)
      newFood = successorGameState.getFood() #figure this out later
      oldFood = gameState.getFood()
      ghostIndices = self.getOpponents(successorGameState)

      numRepeats = sum([1 for x in self.observationHistory[-20:] if x.getAgentPosition(self.index) == newPos])
      foodPositions = myFood
      foodDistances = [self.getMazeDistance(newPos, foodPosition) for foodPosition in foodPositions]
      closestFood = min( foodDistances ) + 1.0

      ghostPositions = [successorGameState.getAgentPosition(ghostIndex) for ghostIndex in ghostIndices]
      ghostDistances = [self.getMazeDistance(newPos, ghostPosition) for ghostPosition in ghostPositions]
      ghostDistances.append( 1000 )
      closestGhost = min( ghostDistances ) + 1.0

      teammateIndices = [index for index in self.getTeam(gameState) if index != self.index]
      assert len(teammateIndices) == 1, "Teammate indices: {}".format(self.getTeam(gameState))
      teammateIndex = teammateIndices[0]
      teammatePos = successorGameState.getAgentPosition(teammateIndex)
      teammateDistance = self.getMazeDistance(newPos, teammatePos) + 1.0

      pacmanDeath = successorGameState.data.num_deaths

      features['successorScore'] = self.getScore(successorGameState)

      features['closestFood'] = closestFood
      features['closestGhost'] = closestGhost
      features['numRepeats'] = numRepeats
      features['teammateDistance'] = teammateDistance
      
      return features
