README DO PROGRAMA

Project Structure

api_processor/
	main.py
	input_parameters.json
	request_handler.py
	processing/
		processor.py
		handlers/
			video_handler.py
			img_handler.py
			comment_handler.py
	storage/
		storage.py
		cleanup.py
	logger.py
	html/
		html_generator.py
		templates/
			base.html
	helper_functions.py
	requirements.txt
	README.md
	.env

-------------------------------------------------------

Program flow:

input_parameters -> main -> request_handler -> processor -> handlers -> storage -> HTML & logger

If any errors, use logger.
