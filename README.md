# BookClub - Book Review Website | Third Milestone Project
**Stream Three Project: Data Centric Development - Code Institute**
## Introduction
This is my third project showcasing the knowledge I have gained in Python3, Databases such as MongoDB and Frameworks like Flask. I believe I have 
created a user friendly website 
I have built a simple CRUD application that a user is able to interact with and perform all the basic create, read, update and delete functions.
Users can create accounts, add books, review books, edit account info, upload user images, delete books etc! 
## Demo

Click the image below to view my Live Portfolio.
<a href="https://bookclub-ms3.herokuapp.com/">here</a>

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
| User | User Stories |
| ------ | ------ |
| Book lovers | As A book lover I want to be able to see a vast amount of books
| Children |
| The once in a while reader |

### Structure

### Skeleton

### Surface

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
- [JavaScript](https://www.javascript.com/)
    - JavaScript Improves the User Experience on my site.
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

### Features Left To Implement
- [ ] Due to using an existing dataset I was limited to the data I had been provided as such I have not got information such as 
genre or category. In the future I plan to use my own data which does provide all the information I want.
- [ ] In the Future I plan to have Friends / Followers where you are able to view other users profiles, books people are reviewing and what they like.
Also providing a means to message or comment on each others pages.
- [ ] At the moment the Add book form is unmoderated so if a user uploads incorrect data, rude data etc then it will just be uploaded. In the future I plan to moderate 
all posts so I can keep my database clean.


## Testing

## Deployment
I am currently deploying my website on Heroku deploying from the master branch. My Github Repository and Heroku are linked and are currently set to automatic deploys as I was having issues using multiple machines when I was using Heroku Git originally.
Due to this all commits will deploy from the master branch automatically. The site can be viewed at https://bookclub-ms3.herokuapp.com/. 
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
### Cloning the repository
To run this repository locally:
1. Click "Code" at the top of this repository.
2. Select Download Zip or Copy the URL to your clipboard. 
3. Open up Terminal and select the location in which you wish to clone this directory 
4. Then type `git clone` and copy `https://github.com/kushberrycream/BookReviewSite.git` 
5. Press enter and you will have succesfully cloned this Repository. 
## Credits
### Content
- [Book Database](https://www.kaggle.com/zygmunt/goodbooks-10k?select=books.csv) To fill my website with Books I found a Dataset online and uploaded this into MongoDB.
- ![The Footer links](https://github.com/kushberrycream/BookReviewSite/blob/master/static/images/footer-links.png?raw=true "The Footer links!") Apart from the LinkedIn and Facebook all links have been found on google 
and I do not claim to own or have anything to do with these.
### Media
- [Book Background](https://i.pinimg.com/originals/67/18/22/671822c2f63dd5f65d8fd15c9710420b.jpg) This is the picture used throughout the site as the background.
- [Favicon](https://flyclipart.com/book-icons-book-icon-png-569911) I have used this Icon as the Favicon.
- [Navbar Logo](https://www.freelogodesign.org/) The logo was made on this website.
### Acknowledgments
- [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/) Helped me with the syntax and any queries I had with the flask Framework
- [ShubhamJain](https://shubhamjain.co/til/how-to-render-human-readable-time-in-jinja/) Helped me create a filter to use within the jinja templates. The filter formats
timestamps to be in a human readable format.
- [MDBootstrap](https://mdbootstrap.com/) The Homepage began as a MDBootstrap template which has been edited sufficently and also multiple components used.
- [StackOverflow](https://stackoverflow.com/questions/22150273/how-can-i-break-a-for-loop-in-jinja2) StackOverflow seems to be where I find the answers and solutions to my most challenging problems, 
I have used a question that helped me with a problem I had for the link.
