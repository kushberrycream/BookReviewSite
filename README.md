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
The site has a full page background throughout but on everypage except the homepage it is displayed behind a container with a white background this give it a clean and simple design, it also avoids any issues with contrast between background
and fonts, it also makes it look alot cleaner on smaller devices as full page backgrounds do not display correct on iOS devices. The font throughout is roboto as this is very clean and readable. The Navbar and Footer are both the same shade of 
grey and have the same colour font. All book Thumbnails are displayed the same on everypage to bring a uniformity to my website. 

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

<p align="right">
  <a href="#bookclub---book-review-website---third-milestone-project">Back to Top :arrow_heading_up:</a> 
</p>

## Testing

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
