import json
import os
from helper_functions import get_API_params
from request_handler import request_handler
from processor import processor
from storage import reddit_local_storage
from dotenv import load_dotenv
from cleaunp import cleanup
from html_generator import generate_htmls

# ----------------------------------------------------
# ENTRY POINT, STARTS PROGRAMS, CALLS OTHER FUNCTIONS.

'''
TO DO: add less_comments parameter to program's logic.
       add amount of days for cleanup to program's logic.
       update requirement.txt
'''


# Assigns contents of json to a variable.
with open('input_parameters_teste.json', 'r') as json_file:
    input_parameters = json.load(json_file)

# Separates parameters of requests into tuples and stores them in a list.
params = list(input_parameters.items())

# Gets parameters necessary to make API requests.
api_params = get_API_params(params)

# Gets responses from Reddit.
responses = request_handler(api_params)

# Extracts reponses' data.
processed_posts = processor(responses, params)

# Saves data to local folder.
load_dotenv()
output_folder = os.getenv('OUTPUT_PATH')
reddit_local_storage(processed_posts, output_folder)

# Deles data older than 14 days.
cleanup(14, output_folder)

generate_htmls(output_folder)