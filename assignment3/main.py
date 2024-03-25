from itertools import count

# direction constants
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class MDP():
    """
    Markov decision process class
    """

    def __init__(self, grid, terminal, discount_factor):
        """

        """
        self.discount_factor = discount_factor
        self.grid = grid
        self.dim = len(grid)
        self.states = []
        self.Rmax = grid[terminal[1]][terminal[0]]
        self.terminal = terminal
        for y in range(self.dim):
            for x in range(self.dim - 1 , -1 , -1):
                self.states.append((x,y))

    def actions(self, state):
        """
        Available actions for a given state (x,y)

        :param state        the current state represented as a tuple (x,y)

        :return actions     a list of actions
        """
        x, y = state
        actions = []

        if state == self.terminal:
            return actions

        if y > 0:                   # if y > 0 add action move up
            actions.append(UP)

        if y < self.dim - 1:          # if y < dim add action move down
            actions.append(DOWN)

        if x > 0:                   # if y > 0 add action move left
            actions.append(LEFT)

        if x < self.dim - 1:          # if x < dim add action move right
            actions.append(RIGHT)

        return actions

    def transitions(self, state, action):
        """
        Get a list of the next states and their corresponding probabilities

        :param state            the current state represented as a tuple (x,y)
        :param action           the action to be taken at the current state

        :return transitions     a list of next states and their probabilities
        """
        x, y = state
        actions = self.actions(state)
        inverse = 0.1
        # probability based on available actions
        selected = 1 - (len(actions) * inverse)
        transitions = []

        for a in actions:
            probability = inverse
            if a == action:
                probability = selected
            if action == UP:
                next_state = (x, y - 1)
            elif action == DOWN:
                next_state = (x, y + 1)
            elif action == LEFT:
                next_state = (x - 1, y)
            elif action == RIGHT:
                next_state = (x + 1, y)
            transitions.append((next_state, probability))

        return transitions


class ValueIteration():
    """
    Value iteration algorithm returns a utility function
    """

    def __new__(self, mdp, maxError=2):
        """
        :param mdp          a MDP with states S, actions A(s), transition model P(s'|s,a),
                            rewards R(s,a,s'), discount γ/gamma
        :param maxError     the maximum error/ε allowed in the utility of any state

        :return U           a policy, vector of utility values for each state
        """
        U = [[]]
        U_prime = mdp.grid
        self.mdp = mdp

        while True:
            self.U = U = U_prime
            maxChange = 0

            for state in mdp.states:
                for action in mdp.actions(state):
                    value = 0.0
                    for next_state,probability in mdp.transitions(state, action):
                        value += probability * \
                                ((self.reward(self, state, action) + \
                                 mdp.discount_factor * U[next_state[1]][next_state[0]]))

                    U_prime[state[1]][state[0]] = value
                    # U_prime[state[1]][state[0]] = max(sum(mdp.actions(state)), self.qValue(mdp, state, action, U))
                    maxChange = max(abs(U_prime[state[1]][state[0]] - U[state[1]][state[0]]), maxChange)
            if maxChange <= maxError * (1 - mdp.discount_factor) / mdp.discount_factor:
                return U

    def qValue(self,mdp, state, action, U):

        # sum(P(state_prime|state, action)(self.reward(state, action) + self.gamma * U[state_prime]))

        return

    def reward(self, state, action):
        """
        reward utility function produces a reward for moving from current state to
        the next based on the action.

        :param state        the current state represented as a tuple (x,y)
        :param action       the action for the current state that leads to the next

        :return reward      the reward for the action leading to the next state
        """
        reward = 0
        x, y = state

        # move up, if action up and y > 0
        if action == UP and y > 0:
            reward = self.U[x][y-1]

        # move down, if action down and y < dim
        elif action == DOWN and y < self.mdp.dim - 1:
            reward = self.U[x][y+1]

        # move left, if action left and x > 0
        elif action == LEFT and x > 0:
            reward = self.U[x-1][y]

        # move right, if action right and x < dim
        elif action == RIGHT and x < self.mdp.dim - 1:
            reward = self.U[x+1][y]

        return reward

    def utility(self, state, action):
        """
        reward utility function produces a reward for moving from current state to
        the next based on the action.

        :param state        the current state represented as a tuple (x,y)
        :param action       the action for the current state that leads to the next

        :return reward      the reward for the action leading to the next state
        """
        utility = 0

        for i in count(): 
            utility += self.gamma ** i * self.reward(state, action)

        return utility

def main():
    discountFactor = 0.99
    R = [-100, -3, 0, +3]
    r = R[0]
    world = [[r, -1 , 10, ], [-1, -1, -1], [-1, -1, -1]]
    terminal = (2,0) # x,y

    for r in R:
        world[0][0] = r
        mdp = MDP(world, terminal, discountFactor)
        print(ValueIteration(mdp))



if __name__ == '__main__':
    main()