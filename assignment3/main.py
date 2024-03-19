

def Q_Value(mdp, s, a, U):

    return 


def ValueIteration(mdp, maxError=2):
    """
    Value iteration algorithm returns a utility function

    :param mdp          a MDP with states S, actions A(s), transition model P(s'|s,a),
                        rewards R(s,a,s'), discount δ/delta
    :param maxError     the maximum error allowed in the utility of any state

    :return U           a policy, vector of utility values for each state
    """

    U = []
    U_prime = []
    maxChange = 0.01
    S,A,P,R,delta = mdp

    while True:
        U = U_prime

        for s in S:
            U_prime = max(sum(A[s]), Q_Value(mdp, s, a, U))
            change = abs(U_prime[s] - U[s])
            if change > maxChange:
                maxChange = change
        if maxChange <= maxError * (1 - delta) / delta:
            return U


def main():
    world = [[r, -1 , 10, ], [-1, -1, -1], [-1, -1, -1]]
    R = [-100, -3, 0, +3]
    discount = 0.99

    for r in R:
        world[0][0] = r



if __name__ == '__main__':
    main()