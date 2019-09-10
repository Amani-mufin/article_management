# Article Management System
A Flask-based web app where authors can create accounts, login and share their articles. Also, visitors can view articles and search using specific keywords.

## Requirements
    cs50
    Flask
    Flask-Session

## Installation
Run the following commands on your terminal in your preferred directory:
```
$ git clone https://github.com/sirsuccess/article_management.git
$ cd article_management
```
If you don't have all of the above requirements installed in your python virtual environment, run this code in your terminal 
```
$ pip install -r requirements.txt
```
If you don't know how to create and activate virtual environments, [follow this link](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/).

After completing the necessary installation in your virtual environment, run the following commands
```
$ export FLASK_APP=application.py
$ flask run
```
After running the above commands, click the link that shows up in the terminal and you should be greeted by a page that looks like this:
![AMS Homepage](https://res.cloudinary.com/doctor-vee/image/upload/v1567674075/ams.png)

## User Stories
Authors should be able to 
- Sign Up
- Log in
- Create articles which will have
    1. Title
    2. Description
    3. Content
    4. Tags

Users should be able to 
- View all articles 
- Search for articles that contain a particular keyword
- Search for all articles written by a particular author
- Like or dislike articles

## Authors
| [Victor CHINEWUBEZE](https://github.com/Victor-Chinewubeze) | [Amani Kanu](https://github.com/sirsuccess) | [Promise](https://github.com/smartpro1) |
| --- | --- | --- |
| ![Victor](https://res.cloudinary.com/doctor-vee/image/upload/v1554915401/PIC_450px.jpg) | ![Amani](https://res.cloudinary.com/doctor-vee/image/upload/v1567675231/amani.jpg) | ![Promise](https://res.cloudinary.com/doctor-vee/image/upload/v1568082570/promise.jpg) |
