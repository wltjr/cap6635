import copy

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
        # memoize state actions
        for y in range(self.dim):
            for x in range(self.dim - 1 , -1 , -1):
                self.states.append((x,y))

                actions = []
                if (x,y) != self.terminal:
                    actions.append((UP, y > 0))
                    actions.append((DOWN, y < self.dim - 1))
                    actions.append((LEFT, x > 0))
                    actions.append((RIGHT, x < self.dim - 1))

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
        probability = 1
        inverse = 0.1
        transitions = []

        for a,valid in actions:
            if valid:
                if a == UP and action != DOWN:
                    probability -= inverse
                    transitions.append(((x, y - 1), inverse))
                elif a == DOWN and action != UP:
                    probability -= inverse
                    transitions.append(((x, y + 1), inverse))
                elif a == LEFT and action != RIGHT:
                    probability -= inverse
                    transitions.append(((x - 1, y), inverse))
                elif a == RIGHT and action != LEFT:
                    probability -= inverse
                    transitions.append(((x + 1, y), inverse))
        transitions.append((state, probability))

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
        U_prime = [[0 for _ in range(mdp.dim)] for _ in range(mdp.dim)]
        self.mdp = mdp
        sigma_gamma = maxError * (1 - mdp.discount_factor) / mdp.discount_factor

        while True:
            U = copy.deepcopy(U_prime)
            maxChange = 0.0

            for state in mdp.states:
                U_prime[state[1]][state[0]] = round(self.maxQValue(self, mdp, state, U), 4)
                maxChange = max(abs(U_prime[state[1]][state[0]] - U[state[1]][state[0]]), maxChange)

            if maxChange <= sigma_gamma:
                return U

    def maxQValue(self, mdp, state, U):
        """
        Maximum Q-value function to return the maximum value for the state given
        the actions and probabilities

        :param mdp          a MDP with states S, actions A(s), transition model P(s'|s,a),
                            rewards R(s,a,s'), discount γ/gamma
        :param state        the current state represented as a tuple (x,y)
        :param U            a policy, vector of utility values for each state

        :return value       a float, the maximum q-value
        """
        values = []
        for action,_ in mdp.actions(state):
            value = 0.0
            for next_state,probability in mdp.transitions(state, action):
                value += probability * \
                         ((mdp.grid[state[1]][state[0]] + \
                          mdp.discount_factor * U[next_state[1]][next_state[0]]))
            values.append(value)

        if len(values) == 0:
            return U[state[1]][state[0]]
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
    display = [[0 for _ in range(dim)] for _ in range(dim)]
    for y in range(dim):
        for x in range(dim):
            if (x,y) == terminal:
                display[y][x] = 'G'
                continue

            values = []
            if y > 0:                   # if y > 0 add action move up
                values.append((policy[y-1][x], "↑"))
            if y < dim - 1:          # if y < dim add action move down
                values.append((policy[y+1][x], "↓"))
            if x > 0:                   # if x > 0 add action move left
                values.append((policy[y][x-1], "←"))
            if x < dim - 1:          # if x < dim add action move right
                values.append((policy[y][x+1], "→"))

            display[y][x] = sorted(values, key=lambda x: x[0], reverse=True)[0][1]

    for i in range(dim):
        print(display[i])


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