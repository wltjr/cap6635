

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