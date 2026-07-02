# This is function is for the place file to calculate the number of likes and dislikes
def calculate_vote(vote):
    like = 0
    dislike = 0
    for all_row in vote:
        if all_row.vote is True:
            like = like+1
        elif all_row.vote is False:
            dislike = dislike+1

    # print(like, dislike)
    # This will be returned as tuples
    return like, dislike
