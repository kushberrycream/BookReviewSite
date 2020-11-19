# BookClub - Book Review Website - Third Milestone Project
**Stream Three Project: Data Centric Development - Code Institute**
## Introduction
This is my third project showcasing the knowledge I have gained in Python3, Databases such as MongoDB and Frameworks like Flask. I believe I have 
created a user friendly website 
I have built a simple CRUD application that a user is able to interact with and perform all the basic create, read, update and delete functions.
Users can create accounts, add books, review books, edit account info, upload user images, delete books etc! 

When setting up my workspace i had accidentally commited my enviromental variables, due to this I changed my enviroment variables to keep the my site secure.

## Demo

Click the image below to view my Live Portfolio.
<a href="https://bookclub-ms3.herokuapp.com/">
  <img alt="am i responsive" src="https://github.com/kushberrycream/BookReviewSite/blob/master/static/images/bookclub-prev.png?raw=true">
</a>

## Contents
- [Introduction](#bookclub---book-review-website-|-third-milestone-project)
- [Demo](#demo)
- [UX](#ux)
    * [Strategy](#strategy)
    * [Scope](#scope)
    * [Structure](#structure)
    * [Skeleton](#skeleton)
    * [Surface](#surface)
- [Technologies Used](#technologies-used)
- [Features](#features)
    * [Existing Features](#existing-features)
    * [Features Left to Implement](#features-left-to-implement)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)
    * [Content](#content)
    * [Media](#media)
    * [Acknowledgments](#acknowledgments)

## UX  
### Strategy
I wanted users of my book review website to be able to view book information and book reviews. I also wanted users to be able to upload their own books 
if it is not provided already, edit any information they believe to be incorrect and delete any information they have provided! I am also providing book 
recommendations via the reviews posted in the hope to get users to use my amazon affiliate link, which a link is also provided with every book.

### Scope
| User   | User Stories |
|:------:| ------ |
| Book Lovers | As A book lover I want to be able to see a vast amount of books, what people have to say about those books, also to be able to leave my own reviews on those books and be able to link to somewhere to purchase any book that I might be intrested in. I would also want the ability to add a book that may not be already available to me on the website.
| The once in a while reader | As a once in a while reader I want to find books that are recommended by other users, I want to see what they have to say about the book and how they rate it, I want to see a description of the book and also a link to buy any book I have an interest in.
| Book Clubs | As a book club I want to find books that might be of interest to my club. I want to see what other users recommend and also a summary of the book. I may even be interested in a purchase link.

### Structure
The Navbar is used throughout the site, if no user is logged in a log in button is available but once logged in this changes to the username of the user which is also a dropdown 
with a link to the account page and also a log out button. The Footer is used throughout also except from the homepage, the footer is minimal and only displays links to social media but also displays
the regular copywrite message. 

The homepage will be a full height landing page with a sign up form, for users with a login a login button is available in multiple places. 
Once signed in the Sign-up form will not display leaving two CTA's one to open your account page or the other to view all books, along with a sample of the most recently added books.

The account page will be the users dashboard to view, edit and delete any posts they have made. They can also upload profile information and a profile photo which will be displayed against any posts they make.

The All Reviews page displays every review on the site, it is sortable by username, date, book and ratings, the page is purely just to view all the reviews on the site but you can link to a specific books page.
Only 10 reviews are displayed per page and then it will paginate.

The Recommendations page only displays top reviews and wether or not the book is recommended by the sites users. A user will then be able to link to the books page or directly link to my amazon link.

The All books page displays every book on the site with the ability to search the database, 48 books are displayed per page and when each book is hovered ther most recent review is displayed and the rating.

The Add books page is a form that allows a logged in user to post a book they cannot find on the website. It will be a basic form which every field will be required to post the form.

From the majority of the pages a user is able to link to a books specfic page. Once they are there they can view all the information stored for that book such as the desciption, stats and reviews from users.
Buy book, Edit book, Review book and Delete book buttons are available on all of the books pages but if the user is not logged in then these buttons will be disabled.
If the user is the administrator or if the user posted the book then the delete book button is available otherwise this is disabled to all other users.

The Review page is a simple form with 2 inputs. The first is the review itself, the second is the star rating. Again only someone logged in can leave a review, but if a user has already left a review then they are redirected
towards there account where they can edit the original post. The Edit Review page is virtually a duplicate of the Add review page but the user can update the original post.

The delete page is the same if you are deleting your account, a book or a review. Depending on what delete button is pressed depends what information is displayed and what collection a user will be deleting information from.

### Skeleton
[Homepage / Landing Page](https://github.com/kushberrycream/BookReviewSite/blob/master/static/images/wireframes/Homepage%20_%20Landing%20Page.png?raw=true) 

[All Reviews](https://github.com/kushberrycream/BookReviewSite/blob/master/static/images/wireframes/All%20Reviews.png?raw=true)

[Recommendations](https://github.com/kushberrycream/BookReviewSite/blob/master/static/images/wireframes/Recommendations.png?raw=true)

[All Books](https://github.com/kushberrycream/BookReviewSite/blob/master/static/images/wireframes/All%20Books.png?raw=true)

[Book Details](https://github.com/kushberrycream/BookReviewSite/blob/master/static/images/wireframes/Book%20Details.png?raw=true)

[Add Book](https://github.com/kushberrycream/BookReviewSite/blob/master/static/images/wireframes/Add%20Book.png?raw=true)

[Add Review](https://github.com/kushberrycream/BookReviewSite/blob/master/static/images/wireframes/Add%20Review.png?raw=true)

[Account / User Page](https://github.com/kushberrycream/BookReviewSite/blob/master/static/images/wireframes/Account%20_%20User%20Page.png?raw=true)
### Surface
The site has a full page background throughout but on everypage except the homepage it is displayed behind a container with a white background this gives it a clean and simple design, it also avoids any issues with contrast between background and fonts, it also makes it look alot cleaner on smaller devices as full page backgrounds do not display correct on iOS devices. The font throughout is roboto as this is very clean and readable. The Navbar and Footer are both the same shade of grey and have the same colour font. All book Thumbnails are displayed the same on everypage to bring a uniformity to my website. All the Pages follow a similar layout also keeping my application looking clean and simple.

<p align="right">
  <a href="#bookclub---book-review-website---third-milestone-project">Back to Top :arrow_heading_up:</a> 
</p>

## Technologies Used

Here is a list of all the technologies used throughout the project!

- [Balsamiq Mockups 3](https://balsamiq.com/)
    - I have used Balsamiq to create my wireframes.
- [Python3](https://www.python.org/download/releases/3.0/)
    - I have used Python3 to create my server-side application.
- [HTML5](https://www.w3.org/html/)
    - I use HTML to create the basic structure of my book review website.
- [CSS3](https://www.w3.org/Style/CSS/Overview.en.html)
    - CSS gives my site its look and style.
- [JQuery](https://www.jquery.com/)
    - JQuery is used to initialize a few components and generally improve user experience.
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
    - I have utilised the flask micro-framework to speed up the overall process. I have also used multiple modules
    such as flask-pymongo, flask-paginate, session and many more.
- [MDBootstrap](https://mdbootstrap.com/)
    - I have used MDBootstrap as my CSS Framework as I like the combination of bootstrap and material design components.
- [MongoDB](https://www.mongodb.com/)
    - I have chosen to use MongoDB as my database as this is what I feel most comfortable using.
- [Font Awesome](https://fontawesome.com/)
    - Font Awesome was used for all of my icons.
- [Toastr](https://github.com/wiltonsr/Flask-Toastr/)
    - Using the Flask-Toastr module I was able to implement CodeSeven's Toastr js libary to provide non-blocking notifications.

<p align="right">
  <a href="#bookclub---book-review-website---third-milestone-project">Back to Top :arrow_heading_up:</a> 
</p>

## Features
The main features of my site are the ability to view a vast array of books and post reviews on each of these books, Post more books,
link to buy books, edit reviews and also see the recommendations.
### Existing Features
- [x] Users can sign up via the homepage signup form. Once signed in they will be able to leave reviews, view their profile,
 edit their profile and post more books.
- [x] If a user already has an account they are able to login via the login modal which is available through the Call to Action 
on the Navbar and the sign up form.
- [x] A user can only leave one review per book, if they try to add another a toastr notifcation will let the user know they will have to edit the original review.
- [x] A user can post a book via the Add book page, this will add the book to the database and send the user to the page that has just been created, here they can add a review
or edit if they have made an error.
- [x] A search bar is available so users can search for a book instead of crawling through hundreds of pages.

### Features Left To Implement
- [ ] Due to using an existing dataset I was limited to the data I had been provided as such I have not got information such as 
genre or category. In the future I plan to use my own data which does provide all the information I want.
- [ ] In the Future I plan to have Friends / Followers where you are able to view other users profiles, books people are reviewing and what they like.
Also providing a means to message or comment on each others pages.
- [ ] At the moment the Add book form is unmoderated so if a user uploads incorrect data, rude data etc then it will just be uploaded. In the future I plan to moderate 
all posts so I can keep my database clean.
- [ ] The search bar needs to be more exact as at the moment it works but it doesnt always give you what you expect.
- [ ] A Contact page is missing incase any users feel the need to get in touch or have any suggestions etc. This will need to be implement and will not be an issue but is not essential at this time.

<p align="right">
  <a href="#bookclub---book-review-website---third-milestone-project">Back to Top :arrow_heading_up:</a> 
</p>

## Testing

I have done all my testing manually and throughout production of my website. Whenever I have made a change to something I have tested any possible ways in which it could fail such as when I created my all reviews page and I was testing by adding reviews from different users I found a user without a profile image would break the page as it could not display the profile image for that user. 

All the python code is linted and debugged by gitpod so I have not had to worry about syntax or format as this has let me know throughout when I have not been using the correct syntax or I have input my code incorrectly. I have also been using Flask which uses Jinja2 as its template engine which lets me know of any bugs within my code also giving me a pointer to which part of my code is failing. All the HTML and CSS pass validation with [W3 Validators](https://validator.w3.org) but HTML does throw up errors due to the fact I am using jinja2 templating and it does not recognise this but other than the expected errors everything else passes. 

My site is responsive on multiple media devices and viewports. I used googles DevTools to test all the different viewport resolutions, I also did this on Opera and firefox.
I generally had no issues with this as I mainly used MDBootstraps preset classes to help create a flexbox layout keeping everything nice and centered, in a clear order and very responsive. I was able to keep my custom CSS to a minimum due to the way in which I used the framework I was able to keep my code nice and clean. All the pages respond correctly and every link acts in the expected way. I've had no console errors within my code and again act as expected.

During development I noticed that when a user without a profile photo posts a review they review actually breaks a few pages such as all reviews and the specific book page. The pages are looking for a profile photo to display for these reviews but cannot find one and throws an error. To fix this I decided to force users to upload a photo, I plan to automatically have a placeholder image uploaded to the database when a user creates an account but this was a quick and easy fix for now. 

Another bug is with the top ratings sortation, My database already has average ratings and my users input there own ratings which calculates a user average ratings whcih is where the issue occcurs. When a user selects top ratings they are given the collection of books in order of top rating first but because I have two ratings fields to sort through it places all the user ratings first from 5 down to 1 and then the average rating from 5 - 1. I am not sure how to fix this right now and it doesnt cause too much of an issue at this time so I have chosen to leave for the time being and when I can think of a solution I will implement.

Here are a few of the manual processes i've done to test my code:

1. NavBar:
    1. Throughout development I checked all links would respond correctly. By clicking links I was able to confirm this.
    2. Next I went into Devtools and turned on mobile emulation to confirm the Toggler button appears, I would click to confirm the button worked correctly.
    3. Once the links were displayed I clicked each to confirm the navbar opened the page and closed the navbar as intended.
    4. I also checked all available viewports within devtools to makes sure it displayed correctly.
    5. Social links were also checked to makes sure they opened a new tab and of course the correct page.
    6. All tests came were a success and I cannot recall any issues throughout development.

2. Footer:
    1. My footers navigation works as intended when clicked.
    2. Once the Quick Links had been selected I tested to see if they opened the correct pages in new tabs.
    3. I tested each viewport size to see if it resonsed as expected.
    4. All tests were successful and no errors except with styling occured.

3. Responsivness:
    1. I went to Devtools on chrome and chose various viewports, checked to see any display issues.
    2. If issues were discovered I would use Unicorn Revealer to see any hard to find padding / margin issues.
    3. If data did not display properly I added relevant media queries or edited javascript or content until it was correct.
    4. I then chose the responsive option on the viewports and checked as many resolutions as possible.
    5. I repeated the processes for any errors in what was displayed.
    6. I also checked the responsiveness on my personal iPhone and work Android as Devtools I find is not always 100% correct.
    7. If any errors did occur I corrected them accordingly.

4. Pagination
    1. On all reviews and all books pages I first go to the top pagination links and select a page.
    2. The selected page appears and the url string has something link "?page=2" added to the end.
    3. I then press the next links and the url string changes to the relevant page I am on.
    4. This is then repeated on the bottom buttons as they all respond as expected.

5. Login modal
    1. I first select the login button from the nav-bar or from the homescreen. 
    2. A modal appears with a small login form.
    3. Once filled in and submitted I am redirected to the account page I have logged into.
    4. If I input incorrect data I am redirected back to the homescreen with an error to tell me what went wrong.

6. Photo Upload Modal.
    1. Once logged in I navigate to the upload photo button.
    2. When selected the Photo upload modal is displayed with a file upload input.
    3. Once the browse button is selected I can then choose, Jpg, Png, Gif or Tiff images only.
    4. The selected image is then uploaded to the database and shown on the account page.
    5. Users can still select other file types which can cause my site to work unexpectedly.
    6. I plan to fix this in the coming future by not displaying files if they are not the correct file extension.

7. Register form
    1. To test this form I filled out every input and submitted.
    2. Once submitted it brought me to an account page as expected.
    3. Next I tested the validation by inputting known incorrect data.
    4. I first tried an existing username and was given an error message
    5. Next I tried an email without an @ and also ones without .com or .co.uk and again was given an error message as expected.
    6. lastly I tried a non matching password in which again I was given the expected error message.
    7. When testing the matching passwords validator was not working but this was easily fixed as my syntax was incorrect, although the website still worked with no issues from this problem.

8. Add Book Form.
    1. I opened the add books page and filled in all the fields for the form.
    2. All form fields are required so will not let me ignore a field before submitting.
    3. On Submit I am redirected to the newly created book page as expected.
    4. The book is also added into the all books page.
    5. Checking the database and everything is added as expected.
    6. I have no form of moderation for the form submissions so any data input will be uploaded to the database which could be an issue in future.
    7. During development I had forgot to add a user_rating_average field and this made the new book page fail and also the all books page i fixed this by adding the field with a null value.

9. Edit Book Form.
    1. I select a book which does not have the full information available and press the edit book button.
    2. A form is shown with all the information on the book already, I chose a book which needed both the url and the description adding.
    3. I first added the url and submitted and the field and the book page was updated with the URL. Incorrect URLs are able to be passed and this will end up in a blank cover.
    4. Secondly I checked the description field and this acted as expected and input a description to the book page.
    5. Once all the book info was added the edit book button was removed  as I planeed, as I do not feel the books need to be edited further.
    6. This again is an issue if an incorrect url and a description is input as it will remove the button and you cannot edit it any further. Again I plan to fix this in the future.

10. Add Review Form.
    1. I first select a book I want to add a review for and press the add review button.
    2. I fill out the form and all the fields are required and all the fill out this field error appears if a field has been forgotten.
    3. Once submitted I am redirected to the books page with my new review at the top as expected.
    4. I then check the all reviews page to see if my review has been added in which it has.
    5. I also check my account page which also shows the newly added review.
    6. To check to see if I can still add more reviews to the same book I click the edit button again on the book and im given an error that I have already reviewed this book as i expected.

11. Edit Review Form.
    1. To test the edit review form I first go to the account page and select the edit button for the review I want to change.
    2. I am given virtually the same form as the Add review page and I fill it out again.
    3. Once submitted I am redirected back to my account where I can see the updated review.
    4. I then check then all reviews page and can see it has updated.
    5. The books page has also updated so everything works as expected.
    6. A few times during development I would find that one of the reviews would not update this was for various reasons but was fixed by how the page form updates the databases.

12. Delete Buttons.
    1. For the delete buttons I firstly log in and navigate to my account.
    2. Next I select the delete button on one of the reviews, this brings me to a delete page asking if i really want to delete the review. 
    3. Once confirmed the review is deleted from the account page, all reviews and the book page as expected.
    4. Next I checked the delete book button by first adding a fake book entry and adding a couple reviews.
    5. I then select the delete button and am taken to the delete confirmation page which I confirm and am brought back to the all books page.
    6. I check the all reviews page to check to see if all the reviews have deleted which they have.
    7. Finally the delete user button, I created a fake account and then pressed the delete account button.
    8. The same Confirmation page is displayed and I confirm my delete.
    9. This brings me back to the homescreen with a warnng to let the user know their account is deleted.

<p align="right">
  <a href="#bookclub---book-review-website---third-milestone-project">Back to Top :arrow_heading_up:</a> 
</p>

## Deployment
I am currently deploying my website on Heroku deploying from the master branch. My Github Repository and Heroku are linked and are currently set to automatic deploys as I was having issues using multiple machines when I was using Heroku Git originally.
Due to this all commits will deploy from the master branch automatically. The site can be viewed at https://bookclub-ms3.herokuapp.com/. For my site to run in Heroku I have had to supply a requirements.txt file to let Heroku and any other developers know what dependencies are needed for my site. 
I have also supplied a Procfile which lets heroku know the process type of my application.

### Commiting to Github
1. Using my terminal window I firstly use `git pull https://github.com/kushberrycream/BookReviewSite.git` to pull the most upto date version of my repository.
2. Once upto date I edit everything I need to and use `git add .` to stage all the edited files for commiting.

3. Using `git status` I usually view to see I have staged all the files I want to and I have no unwanted files being commited.
4. Next using `git commit` I commit to the local Repository and then `git push` to finally push the changes to the master branch.
### Deploying to Heroku
1. Firstly I needed to go to my Account dashboard, here I can select New and Create New App.
2. I chose a unique app name, the region of Europe and then pressed create app.
3. Once Created I was brought to the deploy section of my app, here I decided to chose to deploy with Github.
4. Heroku then asked for the repo name of my app I wished to deploy.
5. I selected connect once my repo was found and I was then able to commit to the master branch on Github. 
It will then Deploy Automatically as I have automatic deploys turned on.
6. The site is almost deployed but I then needed to go to the settings section and let Heroku know of any enviroment variables such as the ip, Port, Secret key and database URI.
### Cloning the repository
To run this repository locally:
1. Click "Code" at the top of this repository.
2. Select Download Zip or Copy the URL to your clipboard. 
3. Open up Terminal and select the location in which you wish to clone this directory.
4. Then type `git clone` and copy `https://github.com/kushberrycream/BookReviewSite.git` 
5. Press enter and you will have succesfully cloned this Repository. 
### Installing dependencies
Installing Dependencies is very simple and I have supplied a requirements.txt to help with this process. Once the repository has been cloned before it can be ran the user will need to open the terminal on their IDE and type `pip3 install -r requirements.txt`. All the dependencies should now download and you are ready to go.

<p align="right">
  <a href="#bookclub---book-review-website---third-milestone-project">Back to Top :arrow_heading_up:</a> 
</p>

## Credits
### Content
- [Book Database](https://www.kaggle.com/zygmunt/goodbooks-10k?select=books.csv) To fill my website with Books I found a Dataset online and uploaded this into MongoDB.
- ![The Footer links](https://github.com/kushberrycream/BookReviewSite/blob/master/static/images/footer-links.png?raw=true "The Footer links!") Apart from the LinkedIn and Facebook all links have been found on google 
and I do not claim to own or have anything to do with these.
### Media
- [Book Background](https://i.pinimg.com/originals/67/18/22/671822c2f63dd5f65d8fd15c9710420b.jpg) This is the picture used throughout the site as the background.
- [Favicon](https://flyclipart.com/book-icons-book-icon-png-569911) I have used this Icon as the Favicon.
- [Navbar Logo](https://www.freelogodesign.org/) The logo was made on this website.
- [No Image Placeholder](https://cdn.bookauthority.org/dist/images/book-cover-not-available.6b5a104fa66be4eec4fd16aebd34fe04.png) Used on all Books without a Book Cover URL.

### Acknowledgments
- [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/) Helped me with the syntax and any queries I had with the flask Framework
- [ShubhamJain](https://shubhamjain.co/til/how-to-render-human-readable-time-in-jinja/) Helped me create a filter to use within the jinja templates. The filter formats
timestamps to be in a human readable format.
- [MDBootstrap](https://mdbootstrap.com/) The Homepage began as a MDBootstrap template which has been edited sufficently and also multiple components used.
- [StackOverflow](https://stackoverflow.com/questions/22150273/how-can-i-break-a-for-loop-in-jinja2) StackOverflow seems to be where I find the answers and solutions to my most challenging problems, 
I have used a question that helped me with a problem I had for the link.
- [w3 Schools](https://www.w3schools.com/howto/howto_css_star_rating.asp) w3 Schools was used for when I needed a little help, the linked page shows the star rating tutorial that help me style my star ratings.

<p align="right">
  <a href="#bookclub---book-review-website---third-milestone-project">Back to Top :arrow_heading_up:</a> 
</p>
