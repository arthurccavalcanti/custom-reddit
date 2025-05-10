

'''
Receives a list of tuples, such as
[(subreddit1, dict_parameters1), (subreddit2, dict_parameters2), ...],
and returns another list of tuples which contain the subreddit name,
the number of posts and the wanted flairs for each subreddit item.
Ex. [('worldnews', 10, 'all'), ('askscience', 2, ['news', 'sports']), ...]
'''

def get_API_params(params=None):

    api_params = []
    
    for list_item in params:


        subreddit = list_item[0]
        num_posts = list_item[1]['num_posts']

        if list_item[1]['flairs']['filter']:
            flairs = (list_item[1]['flairs']['wanted_flairs'])
        else:
            flairs = 'all'

        tuple = (subreddit, num_posts, flairs)

        api_params.append(tuple)

    return api_params

# ----------------------------------------
if __name__ == "__main__":
    get_API_params()