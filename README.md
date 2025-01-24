# Sprint4ProjectCars

PROJECT TITLE:
Sprint 4 - WEB Application to display and analyze Automobile Data from the vehicles_us.csv file

OBJECTIVES:
We will look at 1 csv file(vehicles_us.csv), and represent the data in this file as a dataframe called df_cars. Then we will attempt to clean and analyze the dataframe and make conclusions and create a web application using the data after it has been cleaned. The Web Application will contain an interactive dataframe that can be filtered by the end user. In addition, the web application will also have a Histogram chart and Scatter Plot chart that can be customized by the end user in real time.

DESCRIPTION OF DATASETS:
FILE 1: vehicles_us.csv: each row corresponds to a car that is for sale
DATAFRAME: df_Cars
'price': Price of car
'model_year': Year car was made
'model': Model of car,(Needs to be broken out to make and model)
'condition': condition of car('good', 'like new', 'fair', 'excellent', 'salvage', 'new')
'cylinders': number of cylinders each car has(6., 4., 8., nan, 5., 10., 3., 12.) Needs to be changed to type int
'fuel': type of fuel the car uses('gas', 'diesel', 'other', 'hybrid', 'electric')
'odometer': provides the mileage on the car
'transmission': type of transmission(automatic vs manual or other)
'type': what type of car('SUV', 'pickup', 'sedan', 'truck', 'coupe', 'van', 'convertible','hatchback', 'wagon', 'mini-van', 'other', 'offroad', 'bus')
'paint_color': color of exterior of car
'is_4wd': Specifies whether or not the car is the car 4 wheel drive(Needs to be of type string for "Yes" or "No" or "Unknown")
'date_posted': Date the car was listed for sale on the site
'days_listed': Number of days the car has been listed for sale

PLAN ON HOW TO ACHIEVE OBJECTIVE GOALS:
STEP 1: Import the file into python and analyze the data by assigning the contents to a dataframe. Then use dataframe methods such as describe(), info() or shape() to help get a big picture understanding of the data
STEP 2: Clean the data within the dataframe using various methods and functions within pandas and python to Identify, remove or replace null values, make sure data types in columns are correct, remove duplicate rows, etc. One the data is cleaned, Explore the relationship between sedan, suv and coupe in relation to price and draw some basic conclusions. We will draw up a box plot and histogram to examine the relationship between these 3 car types and their respective price.
STEP 3: Use the rest of this notebook to run test code to help create the app.py interactive web application. We will be using this juypter notebook in conjunction with visual studio code to develope the web app called app.py. Within this app, we will use streamlit package in conjunction with the github and render websites to help us port our app.py application to the web. Our app.py web application will contain the following functionality:
The first part of the web application will have an interactive dataframe where end users can filter the dataframe in real time by make, car type, price and mileage. The second portion of this web app will contain an interactive histogram and scatter-plot chart. The histogram will have the ability to be customized and filtered by make, type, fuel and paint color in real time by the end user. The scatter-plot chart will have the ability to be customized and filtered by age, odometer, cylinders, model_year, and days listed in real time by the end user.
PLEASE NOTE: This step will contain some scrap code that may or may not be used by the app.py application. The code in Step 3 is merely to be used as a test bed for app.py.

Here are the files involved for this project:
app.py -main code
config.toml -website port configurations for render site to use
requirements.txt - helps set the environment for app.py(package versions etc...)
vehicles_us.csv - main datafile for that app.py web application

Here is the link to my webapp on render: https://moesprint4projectcars.onrender.com/