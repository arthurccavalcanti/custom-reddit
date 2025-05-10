# README DO PROGRAMA

## Project Structure

```
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
```
------

### Program flow:

> input_parameters -> main -> request_handler -> processor -> handlers -> storage -> HTML & logger

If any errors, use logger.

------

READMES of projects
- short description
- gif of it running
- how to run
- tech used
- quick rundown of development problems
- wishlist of future features
- include tests
- do commit history
- have your main projects with a master branch, a dev branch and a in progress feature branch
