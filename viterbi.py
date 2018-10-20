import numpy as np

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):
    """Run the Viterbi algorithm.

    N - number of tokens (length of sentence)
    L - number of labels

    As an input, you are given:
    - Emission scores, as an NxL array
    - Transition scores (Yp -> Yc), as an LxL array
    - Start transition scores (S -> Y), as an Lx1 array
    - End transition scores (Y -> E), as an Lx1 array

    You have to return a tuple (s,y), where:
    - s is the score of the best sequence
    - y is the size N array/seq of integers representing the best sequence.
    """
    L = start_scores.shape[0]
    assert end_scores.shape[0] == L
    assert trans_scores.shape[0] == L
    assert trans_scores.shape[1] == L
    assert emission_scores.shape[1] == L
    N = emission_scores.shape[0]

    def append(scores,old,L, N, last, dp, score):
        for i in range(L):
            score1=scores[N-1][i]+last[i]
            if score<score1:
                old=i
                score=score1
        res = [old]    
        for i in range(N-1,0,-1):
            res.append(dp[i][old])
            old=dp[i][old]
        res=res[::-1]
        return res

    dp_arr = np.zeros(emission_scores.shape, dtype=int)
    scores_arr = np.zeros(emission_scores.shape)
    import sys
    prev = 0
    score = -sys.maxint - 1
    scores_arr -= sys.maxint
    ap=[]
    apif=[]
    for i in range(L):
        dp_arr[0][i] = 0
        scores_arr[0][i] = emission_scores[0][i]+start_scores[i]
    for i in range(N-1):
        for j in range(L):
            for k in range(L):
                score1=emission_scores[i+1][j]+scores_arr[i][k]+trans_scores[k][j]
                ap.append(score1)
                if scores_arr[i+1][j]<score1:
                    dp_arr[i+1][j] = k
                    apif.append(score1)
                    scores_arr[i+1][j]=score1                    
    for i in range(L):
        score1=scores_arr[N-1][i]+end_scores[i]
        if score<score1:
            prev=i
            apif.append(score1)
            score=score1

    out = append(scores_arr,prev,L,N,end_scores,dp_arr,score)
    # res = [prev]    
    # for i in range(N):
    #     prev=dp_arr[i][prev]
    #     out.append(dp_arr[i][prev])
    #     
    return (score, out)