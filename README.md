# PROJECT BUDGET README
Project budget allows a user to create, edit, view and delete projects and to add and delete budgets linked to those projects.

## Purpose
The purpose of this site is to allow a user to log in, create budgets for projects that you might have that require some savings and edit those budgets. The user can only see their data when they are logged in.  

## Features
### Existing Features

1. Register page
2. Login page for existing users
3. Projects page where existing projects can be viewed, edited or deleted. New projects can be added too.
4. Budgets page where existing budgets per project can be viewed or deleted. New budgets can be added too.

### Future Additions
- Add pages that allow the user to input actual spend which link to the budget items
- Add dashboard page that shows the user how many budgets they have per project, the values they have remaining after their actual spends and when the actual spends occurred over time.

## Technologies used
- CSS https://devdocs.io/css/   
- HTML https://devdocs.io/html/
- Font Awesome https://fontawesome.com/v4.7.0/   
- Materialize https://materializecss.com/
- Flask https://flask.palletsprojects.com/en/1.1.x/
- MongoDB https://docs.mongodb.com/
- jQuery https://api.jquery.com/

## Testing
### Registration
- Test that when submitting the registration form on the registration page, a new user is added to the MongoDB database. Navigated to the Register menu item, filled in the form and clicked submit. Opened MongoDB and verified that a new user was added to the Users collection. Did this on a mobile as well as a laptop.
- From the Login page, clicked the Register link at the bottom left hand side of the page to check that the user is redirected to the Register page.

### Login
- Test that a registered user can log in successfully. Used an existing user's details to log in to the web app by clicking on the Login menu item, typing in the username and password and clicking the submit button. When the Welcome flash message appeared I could confirm that it worked.
- From the Register page, clicked the Login link at the bottom left hand side of the page to check that the user is redirected to the Login page.

### Home Page
- When the user is logged in, there is a current bug where the Login and Register links are still visibile to the user. These should not be there as the user has already logged in successfully.

### Projects
- Test adding a new project by clicking on the projects menu item, after being logged in. Clicked the add button and filled in the form. The flash message saying that it was successful and the new project box confirmed that it worked. Checked the MongoDB database in the Projects collection to make sure the new project had been added and it had.
- Test that the correct information for a budget is being pulled through to the website from the DB by comparing side by side. 
- Test deleting a project by clicking on the bin icon. Checked the MongoDB database to make sure that project had been removed.
- Test editing a project's details by clicking on the edit icon. The project form comes up with the fields pre-populated with the information from the DB. I amended some of the fields and clicked the Edit button. When viewing that project on the Projects page, the details have changed. Checked in the MongoDB database and the changes had also been made there. When clicking the cancel button, no changes are made to the DB.

### Budgets
- Test adding a budget to a project by clicking on the Budgets menu item, then clicking the Add Budget button next to one of the projects that was created. Tested submitting the new budget without adding a budget item, and received an error message asking for the item name to be filled in. This is the correct outcome as at least one budget item must be added to a budget for it to be submitted.  Tested that the character limit on the Budget Item field is imposed when typing less than 5 characters, an error message appears when trying to submit with less than 5 characters.  Tested that the amount field only accepts numbers and is required before submitting. 
- Test that the correct information for a budget is being pulled through to the website from the DB by comparing side by side. 
- Test deleting a budget from a project by clicking on the bin icon. Checked the MongoDB database to make sure that budget had been removed.

## Python code 
- Tested pep8 compliance for python code by running pycodestyle on app.py, corrected any warnings and errors.  

## Deployment
Create a new Heroku account.
Create a New App in Heroku with the name project-budget-x in region Europe.
Select Python as the Framework.
Link to GitHub repo nic-was/project-budget.
Add config vars in the settings tab for the project (IP, MONGO_DB, Mongo_URI, PORT, SECRET_KEY, KEY)
In the Deploy tab, choose GitHub as the Deployment method.
Enable Auto deploy to Heroku through github updates.
 
### Acknowledgements
- Thank you Glen, Cheryl and Neville for helping with a lot of user testing.

