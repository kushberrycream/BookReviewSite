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

## Credits

### Content

### Media

### Acknowledgments
