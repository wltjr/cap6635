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
        optimal = False

        for a,valid in actions:
            if valid:
                if a == action:
                    optimal = True
                if a == UP and action != UP and action != DOWN:
                    probability -= inverse
                    transitions.append(((x, y - 1), inverse))
                elif a == DOWN and action != DOWN and action != UP:
                    probability -= inverse
                    transitions.append(((x, y + 1), inverse))
                elif a == LEFT and action != LEFT and action != RIGHT:
                    probability -= inverse
                    transitions.append(((x - 1, y), inverse))
                elif a == RIGHT and action != RIGHT and action != LEFT:
                    probability -= inverse
                    transitions.append(((x + 1, y), inverse))

        if optimal:
            probability -= inverse
            if action == UP:
                transitions.append(((x, y - 1), probability))
            elif action == DOWN:
                transitions.append(((x, y + 1), probability))
            elif action == LEFT:
                transitions.append(((x - 1, y), probability))
            elif action == RIGHT:
                transitions.append(((x + 1, y), probability))
            transitions.append((state, inverse))
        else:
            transitions.append((state, probability))

        return transitions


class ValueIteration():
    """
    Value iteration algorithm returns a policy, utility values for each state
    """

    def __new__(self, mdp, maxError=0.0001):
        """
        Create a new ValueIteration instance and run the algorithm returning the
        policy results

        :param mdp          a MDP with states S, actions A(s), transition model P(s'|s,a),
                            rewards R(s,a,s'), discount γ/gamma
        :param maxError     the maximum error/ε allowed in the utility of any state

        :return U           a policy, vector of utility values for each state
        """
        U_prime = [[ (0,"") for _ in range(mdp.dim)] for _ in range(mdp.dim)]
        self.mdp = mdp
        sigma_gamma = maxError * (1 - mdp.discount_factor) / mdp.discount_factor

        while True:
            U = copy.deepcopy(U_prime)
            maxChange = 0.0

            for state in mdp.states:
                U_prime[state[1]][state[0]] = self.maxQValue(self, mdp, state, U)
                maxChange = max(abs(U_prime[state[1]][state[0]][0] - U[state[1]][state[0]][0]), maxChange)

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
                         ((mdp.grid[next_state[1]][next_state[0]] + \
                          mdp.discount_factor * U[next_state[1]][next_state[0]][0]))

            values.append((value,action))

        if len(values) == 0:
            return U[state[1]][state[0]]
        return max(values, key=lambda value: value[0])


def getArrow(action):
    """
    Converts numeric direction values to arrow characters or G for goal/terminal

    :param action       the action to be converted to arrow character

    :return arrow       a arrow character or G for goal/terminal state
    """
    if action == UP:
        return ("↑")
    elif action == DOWN:
        return ("↓")
    elif action == LEFT:
        return ("←")
    elif action == RIGHT:
        return ("→")
    else:
        return "G"

def main():
    discountFactor = 0.99
    R = [-100, -3, 0, +3]
    terminal = (2,0) # x,y

    for r in R:
        world = [[r, -1 , 10, ], [-1, -1, -1], [-1, -1, -1]]
        dim = len(world)
        line = 64
        r_str = " R = " + str(r) + " "
        dashes = "-" * int(line/2 - len(r_str)/2)
        print(dashes + r_str + dashes)
        print("  Reward table:           Numeric policy:          Arrow Policy:")
        mdp = MDP(world, terminal, discountFactor)
        policy = ValueIteration(mdp)
        policy[terminal[1]][terminal[0]] = (world[terminal[1]][terminal[0]], 'G')
        for y in range(dim):
            for x in range(dim):
                print("%4d  " % (world[y][x]), end='')
            print("    ", end='')
            for x in range(dim):
                print("%6.2f  " % (policy[y][x][0]), end='')
            for x in range(dim):
                print("%6s" % (getArrow(policy[y][x][1])), end='')
            print()
        print("-" * line + "\n")



if __name__ == '__main__':
    main()