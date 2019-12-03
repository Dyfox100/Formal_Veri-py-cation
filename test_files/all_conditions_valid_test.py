def main():
    i = 5
    x = -27
    j = 0
    initialx = x
    #FV_invariant_j==0,initialx==x_x==initialx+j
    while j<i:
        x = x + 1
        j = j + 1
    #END_FV

    #FV_command_j==4,x==21_j==125

    j = 1 + j
    j = (x - 1 + j) * j

    #testing comments
    #END_FV

    x = 4
    y = 3
    j = 5
    #FV_conditional_True_x==4 + j
    if (x!=4):
        x = 4
        x = x + j
    else:
        x = x + j
    #END_FV

    x = 5
    initialx = x
    j = 1
    i = 4
    #FV_invariant_j==1,initialx==x_x==initialx * j
    while j<i:
        x = x + initialx
        j = j + 1
    #END_FV
