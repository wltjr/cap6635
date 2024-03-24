from itertools import count

# direction constants
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class ValueIteration():
    """
    Value iteration algorithm returns a utility function
    """

    def __init__(self, mdp, maxError=2):
        """
        :param mdp          a MDP with states S, actions A(s), transition model P(s'|s,a),
                            rewards R(s,a,s'), discount γ/gamma
        :param maxError     the maximum error/ε allowed in the utility of any state

        :return U           a policy, vector of utility values for each state
        """
        U = []
        U_prime = []
        maxChange = 0.01
        S,A,P,R,delta = mdp

        self.STATES = S
        self.dim = len(S)

        while True:
            U = U_prime

            for s in S:
                U_prime = max(sum(A[s]), self.qValue(mdp, s, a, U))
                change = abs(U_prime[s] - U[s])
                if change > maxChange:
                    maxChange = change
            if maxChange <= maxError * (1 - delta) / delta:
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
            reward = self.STATES[x][y-1]

        # move down, if action down and y < dim
        elif action == DOWN and y < self.dim:
            reward = self.STATES[x][y+1]

        # move left, if action left and x > 0
        elif action == LEFT and x > 0:
            reward = self.STATES[x-1][y]

        # move right, if action right and x < dim
        elif action == RIGHT and x < self.dim:
            reward = self.STATES[x+1][y]

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
    world = [[r, -1 , 10, ], [-1, -1, -1], [-1, -1, -1]]
    actions = (0, 1, 2, 3)

    for r in R:
        world[0][0] = r
#        STATES,A,P,R,delta = mdp
        mdp = (world, actions,  discountFactor)



if __name__ == '__main__':
    main()