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
        Initialize instance of MDP class, set variables, load states and actions
        """
        self.actions_ = {}
        self.discount_factor = discount_factor
        self.grid = grid
        self.dim = len(grid)
        self.states = []
        self.Rmax = grid[terminal[1]][terminal[0]]
        self.terminal = terminal
        for y in range(self.dim):
            for x in range(self.dim - 1 , -1 , -1):
                self.states.append((x,y))

                actions = []
                if y > 0:                   # if y > 0 add action move up
                    actions.append(UP)

                if y < self.dim - 1:          # if y < dim add action move down
                    actions.append(DOWN)

                if x > 0:                   # if x > 0 add action move left
                    actions.append(LEFT)

                if x < self.dim - 1:          # if x < dim add action move right
                    actions.append(RIGHT)

                if (x,y) == self.terminal:
                    actions = []

                self.actions_[''.join(map(str, (x,y)))] = actions

    def actions(self, state):
        """
        Available actions for a given state (x,y)

        :param state        the current state represented as a tuple (x,y)

        :return actions     a list of actions
        """
        return self.actions_[''.join(map(str, state))]


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
    Value iteration algorithm returns a policy, utility values for each state
    """

    def __new__(self, mdp, maxError=2):
        """
        Create a new ValueIteration instance and run the algorithm returning the
        policy results

        :param mdp          a MDP with states S, actions A(s), transition model P(s'|s,a),
                            rewards R(s,a,s'), discount γ/gamma
        :param maxError     the maximum error/ε allowed in the utility of any state

        :return U           a policy, vector of utility values for each state
        """
        U = [[]]
        U_prime = [[0 for _ in range(mdp.dim)] for _ in range(mdp.dim)]
        self.mdp = mdp
        sigma_gamma = maxError * (1 - mdp.discount_factor) / mdp.discount_factor

        while True:
            self.U = U = U_prime
            maxChange = 0.0

            for state in mdp.states:
                for action in mdp.actions(state):
                    U_prime[state[1]][state[0]] = self.maxQValue(self, mdp, state, action, U)
                    maxChange = max(abs(U_prime[state[1]][state[0]] - U[state[1]][state[0]]), maxChange)

            if maxChange <= sigma_gamma:
                return U

    def maxQValue(self, mdp, state, action, U):
        """
        Maximum Q-value function to return the maximum value for the state given
        the actions and probabilities

        :param mdp          a MDP with states S, actions A(s), transition model P(s'|s,a),
                            rewards R(s,a,s'), discount γ/gamma
        :param state        the current state represented as a tuple (x,y)
        :param action       the action for the current state that leads to the next
        :param U            a policy, vector of utility values for each state

        :return value       a float, the maximum q-value
        """
        values = []
        for next_state,probability in mdp.transitions(state, action):
            values.append(probability * \
                          ((self.reward(self, state, action) + \
                            mdp.discount_factor * U[next_state[1]][next_state[0]])))
        return max(values)

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

        # get reward above, if action up and y > 0
        if action == UP and y > 0:
            reward = self.mdp.grid[y-1][x]

        # get reward below, if action down and y < dim
        elif action == DOWN and y < self.mdp.dim - 1:
            reward = self.mdp.grid[y+1][x]

        # get reward left, if action left and x > 0
        elif action == LEFT and x > 0:
            reward = self.mdp.grid[y][x-1]

        # get reward right, if action right and x < dim
        elif action == RIGHT and x < self.mdp.dim - 1:
            reward = self.mdp.grid[y][x+1]

        return reward

    
def displayPolicy(terminal, dim, policy):
    """
    Display a policy converting numeric values into one U, D, L, R actions

    :param terminal     the terminal state represented as a tuple (x,y)
    :param dim          the policy/grid dimensions
    :param policy       a policy, vector of utility values for each state
    """
    for y in range(dim):
        for x in range(dim):
            if (x,y) == terminal:
                policy[y][x] = 'G'
                continue

            values = {}
            if y > 0:                   # if y > 0 add action move up
                values[str(policy[y-1][x])] = "↑"
            if y < dim - 1:          # if y < dim add action move down
                values[str(policy[y+1][x])] = "↓"
            if x > 0:                   # if x > 0 add action move left
                values[str(policy[y][x-1])] = "←"
            if x < dim - 1:          # if x < dim add action move right
                values[str(policy[y][x+1])] = "→"
    
            policy[y][x] = list(dict(sorted(values.items(), reverse=True)).values())[0]
    
    for i in range(dim):
        print(policy[i])


def main():
    discountFactor = 0.99
    R = [-100, -3, 0, +3]
    terminal = (2,0) # x,y

    for r in R:
        world = [[r, -1 , 10, ], [-1, -1, -1], [-1, -1, -1]]
        dim = len(world)
        mdp = MDP(world, terminal, discountFactor)
        policy = ValueIteration(mdp)
        for i in range(dim):
            print(policy[i])
        displayPolicy(terminal, dim, policy)
        print()



if __name__ == '__main__':
    main()