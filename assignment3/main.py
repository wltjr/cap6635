

class ValueIteration():
    """
    Value iteration algorithm returns a utility function
    """

    def __init__(self, mdp, maxError=2):
        """
        :param mdp          a MDP with states S, actions A(s), transition model P(s'|s,a),
                            rewards R(s,a,s'), discount δ/delta
        :param maxError     the maximum error allowed in the utility of any state

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

    def qValue(self,mdp, s, a, U):

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
        if action == 0 and y > 0:
            reward = self.STATES[x][y-1]

        # move down, if action down and y < dim
        elif action == 1 and y < self.dim:
            reward = self.STATES[x][y+1]

        # move left, if action left and x > 0
        elif action == 2 and x > 0:
            reward = self.STATES[x-1][y]

        # move right, if action right and x < dim
        elif action == 3 and x < self.dim:
            reward = self.STATES[x+1][y]

        return reward

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