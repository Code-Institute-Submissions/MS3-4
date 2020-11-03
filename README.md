# MS3 - [Recipe for Disaster](http://louis-g-ms3.herokuapp.com/)

Recipe for disaster is a Flask and  Mongo-DB web application that allows users to find and share their love of cooking! It has the capacity to grow indefinitely with food enthusiasts being able to add their own personal and favourite recipes to the site and stored within the Mongo-DB. 
But Recipe for Disaster is not just for those that already appreciate home-cooked food, this application allows users to discover their passion with features such as finding a truly random recipe, and searching by single ingredients.
 
## UX
 
This web application is for lovers of home-cooked food that wish to try new meals and want to share they're much-loved recipes with others online. With my application Users can come together as a community to share their passion and explore to find things for any occasion or purpose. Recipe for disaster is the best way to achieve these goals due to it's usablility, speed and design.
 
	- As a user I want to be able to see recipes created by other users.

	- As a user I want to be able to search by keyword to find a recipe

	- As a user I want to be able to filter by category to find a recipe
			
	- As a user I want to add my own recipe to be viewed by others

	- As a user I want to be able to sign up and log into the application.

	- As a user I want to be a try a recipe I've not had before.

Full wireframes can be found [here](https://github.com/louisgreenhall/MS3/blob/main/Wireframes/Wireframes%20PDF.pdf)


## Features

	• View Recipe: This feature allows users to read recipes stored on the database, displayed on a dedicated page, with everything a user needs to make the same meal themselves
	• Search Recipes: from anywhere in the site a user can search for a keyword of a name of a recipe such as "Sweet" for "Sweet and sour chicken". 
	• Search Recipes by category: A page in the application is dedicated to all the categories of all the recipes stored in the database, this makes it easy for users to filter their search results by a particular category of food, such as "burgers" for Cheese-Stuffed Burgers
	• Search by ingredients: within the search bar located at the top of the page users can narrow their choices down by picking a single ingredient such as "pasta" which returns all ingredients with pasta mentioned in their ingredients list, name or description.
	• Add recipe: Users can log in and then add their own or their favourite recipes to the site and then see them displayed in the same style as the others in our collection.
	• Edit recipe: allows users to change details of a recipe on the application. 
	• Delete recipe: as a function on every recipe there is the option to delete it from the database, for whatever reason. This will remove it from database and if one of it's categories had only that recipe in it's group, it will remove the redundant category as well, keeping the site clean and user expectations met.
	• Register: From the log in page users can provide a prefered username, password and email address to allow them to sign in and add recipes to the site
	• Sign in: Once a username and password have been created, users are then able to come back at any time and log back in to add to their collection and

 
### Existing Features

	- Viewing a recipe - allows users to see a recipe in full (Name, Description, Image, Ingredients, Steps) They can achieve this by clicking on any recipe card, searching for a recipe or clicking the random recipe button.

	- Searching a recipe - allows users to search for a recipe by providing a keyword to the searchbar, after searching they will be taken to a result page showing all and any recipes that match their parameters

	- Signing up / Logging in - allows users to provide their details and create an account and then sign in. Users can do this by providing a prefered username for themselves, a password and their email address in order to then gain the benefit to add their own recipe to the site

	- Adding a recipe - Once signed in users can access the drop down box under their username, filling in all the necessary fields and providing a url to aan image of their choice will then allow them to send the recipe to the databse and they'll be able to see it displayed alongside the others.

	- Editing a recipe - Users can alter the details of a recipe from the recipe page by clicking the edit recipe button where they'll be able to submit changes to the fields they select and then be taken back to the recipe page they made changes to.

	- Deleting a recipe - Users can delete recipes from the site by viewing their chosen recipe and clicking the delete button, this will remove the recipe itself, and remove the recipe from all categories; users will not see this again unless it is added back.

### Features Left to Implement

	- Youtube API linked to recipe pages, would allow users to see search results in the page for their recipe title - for users that prefer to watch a recipe rather than read one

	- Set up an "add to cart" link that will add all ingredients mentioned for a recipe to a shopping cart for a supermarket so that users planning to make a recipe in the future can know they have everything they need

	- Promote own brand of kitchenware, within each recipe promote key utensils that would likely be necessary such as a pasta maker for a pasta dish or a rice cooker for a meal with rice.

	- Add comment/review functionality to recipe page so community member can leave feedback and reviews promoting recipes they enjoyed or disliked

	- Link authors to recipes they've created so that they can view them seperately

## Technologies Used

- [Materialize Framework](https://materializecss.com/)
    - I used **Materialize** to provide responsiveness and structure to my website.

- [Mongo-DB](https://www.mongodb.com/)
	- I used Mongo-DB to host the data collected and retrieved for each recipe seen on the site

- [Bcrypt](https://pypi.org/project/bcrypt/)
	- I used Bcrypt to provide encryption to passwords stored on in the database

- [Heroku](https://www.heroku.com/)
	- I used Heroku to deploy and host my live-site

- [Pymongo](https://pypi.org/project/pymongo/)
	- I used Pymongo to communicate with mongo-DB from my Python files

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
	- I used Flask interact between my .py files and .html


## Testing

### User Stories testing

	- As a user I want to be able to see recipes created by other users.
		Open application
		From home page, click on recipe within upper carousel to be taken to its page
		Verified I was able to see recipe
	
	- As a user I want to be able to search by keyword to find a recipe
		Open application
		Chose keyword "beef" and entered into search bar in navigation at top of page
		Pressed enter
		Was taken to results page with recipes that contained beef in title, ingredients and description
		Clicked on a result
		Verified I was able to see recipe
	
	- As a user I want to be able to filter by category to find a recipe
		Open application
		Clicked on Categories link in navigation at top of page
		Was taken to page displaying all recipe categories
		Chose category "Chinese"
		Was taken to a resulting page displaying all recipes that were chinese dishes
		Clicked on a result
		Verified I was able to see recipe

	- As a user I want to add my own recipe to be viewed by others
		Open application
		Clicked on login/sign up link at top of page
		Was taken to a sign up form
		Completed form with valid information
		Used above created user details to log in
		Clicked on username dropdown window and selected "add recipe"
		Taken to create recipe page
		Completed form with valid information, including a valid image URL
		Pressed submit button
		Verified I was able to see my recipe, copied URL to clipboard
		Logged out using dropdown on top navigation bar
		Pasted URL into address bar
		Verified I was able to see my recipe while logged out

	- As a user I want to be able to sign up and log into the application.
		Open application
		Clicked on login/sign up link at top of page
		Was taken to a sign up form
		Clicked Login tab
		Completed form with invalid information
		Verified I was unable to login to application
		Clicked Sign Up tab
		Completed form with valid information
		Verified I was able to create a user
		Reloaded Login Page
		Clicked Login tab
		Completed form with valid information
		Verified I was able to login to application

	- As a user I want to be a try a recipe I've not had before.
		Open application
		Clicked button "Random Recipe" on home page
		Verified I was able to see a recipe I had not specified
		Refreshed page
		Verified new recipe was shown


### Responsive Testing
	-	I tested the application on a variety of screen sizes (mobile, tablet, desktop, large desktop screen > 1920px) to ensure that all content could be viewed on each size. 
	- Several adjustments were made to the homepage carousels to ensure that content would fit the screen appropriately (full width on mobile, multiple columns on larger screen sizes)
	- Reusable components (includes) were used to ensure that the styling would be as consistent as possible around the site, across different sized screens.
	- One issue identified is that when actively resizing the screen (using developer tools), the carousel width/height are recalculated dynamically and this can cause some visual issues. Refreshing the page on the same size resolves this issue.

### Other Testing

	- While testing, I realised that a lot of content (including static content - css, images, js files) were being heavily cached, requiring a restart of the application each time. To get around this, I followed [this guide](https://stackoverflow.com/questions/34066804/disabling-caching-in-flask) to disable static content caching in Flask.

## Deployment

Following the documentation in the course for deploying to Heroku, and also the following guide [Getting Started With Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python#define-a-procfile) allowed me to relatively easily deploy the application to Heroku:

	- I was required to set up an alternative git remote using `git remote -a heroku louis-g-ms3` so that I was able to push changes to Heroku
	- I was required to set up some config (environment) variables that could be used to get the port used by the application/connection strings etc
	- I was required to create a Procfile in the root of my project with the following `web: python runserver.py 0.0.0.0:5000`
	- Once I had the Heroku CLI installed, I had to create a master branch in GIT and use `git push heroko master` to try deploying the application
	- This flagged up a number of errors that required fixing, including missing dependencies from the requirements.txt file, specifically dnspython and flask-mongoengine, as well as the missing config variables above (it couldn't connect to the port after 30 seconds)

	- To connect to the application locally, it is necessary to open the project in Visual Studio Code, ensure you have all of the requirements installed (you can use `pip install -r requirements.txt`), and once run, you need to open the MS3_Application folder, and use VS Code's in-built debugger to open __init__.py as a Flask application



## Credits

### Content
- A number of the recipes used in this site were were obtained from [BBC Good Food](https://www.bbcgoodfood.com/)

### Media
- The photos and some of the content used in this site were obtained from [BBC Good Food](https://www.bbcgoodfood.com/)

### Acknowledgements

- I would like to thank my mentor Felipe Souza Alarcon for the help and advice he has given me throughout the course of this project.