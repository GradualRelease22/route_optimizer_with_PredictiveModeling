# My Simple Intelligent Route Optimizer 
Hello!
This is my project that is a simple intelligent route optimization system built with Python and Flask.

The app lets a user enter delivery stops, then it predicts the estimated time for each part of the route and returns an optimized stop order.

The project is intentionally simple so beginners can understand how it works, run it locally, and explain it clearly.

---

# What my Project Does

The system takes a list of delivery stops and finds a better order to visit them.

Each stop includes:

Name
Latitude
Longitude
Number of packages
Priority level

The app also lets the user choose:

Traffic level
Weather level

The system then uses those values to estimate how long each route leg will take.

After estimating travel times, it chooses an efficient route and shows:

Recommended stop order
Total estimated distance
Total predicted time
A leg-by-leg route breakdown

---

# How It Works

The project has two main parts:

1. Predictive modeling
2. Route optimization

---

# 1. Predictive Modeling

The predictive model estimates how long it will take to travel from one stop to another.

The model uses these inputs:

Distance between two locations
Traffic level
Weather level
Number of packages
Stop priority

The model is trained inside the project using synthetic sample data.

This means the project does not need a real delivery company dataset to work.

The model learns a simple pattern:

Longer distances usually take more time.
Heavy traffic increases travel time.
Bad weather increases travel time.
More packages increase service time.
Higher priority stops may slightly affect the route decision.

The project uses scikit-learn to train a Random Forest Regressor model.

The model is created when the app starts.

---

# 2. Route Optimization

After the model predicts travel time, the route optimizer decides the order of stops.

The optimizer starts at a fixed depot location.

The default depot is set to Phoenix, Arizona.

The optimizer first uses a nearest-neighbor method.

This means it looks at all unvisited stops and chooses the next stop with the lowest predicted travel time.

After that, it uses a simple improvement method called 2-opt.

2-opt checks whether reversing parts of the route makes the total route faster.

This helps improve the first route.

The final result is not meant to compete with advanced commercial routing software, but it is functional and easy to understand.

---

# Project Files

The project contains these files:

app.py

This is the main Flask web application.

It starts the web server, displays the web page, accepts user input, and sends the stop data to the optimizer.

route_optimizer.py

This file contains the main logic.

It includes:

The Stop data structure
The travel-time prediction model
The distance calculation
The route scoring logic
The nearest-neighbor optimizer
The 2-opt improvement step
The function that reads stop data from text input

requirements.txt

This file lists the Python packages needed to run the project.

templates/index.html

This is the web page users interact with.

It contains the form for entering stops, choosing traffic and weather levels, and displaying the optimized route result.

---

# Required Software

Before running the project, install:

Python 3
Visual Studio Code
The Python extension for Visual Studio Code

You will also need these Python packages:

Flask
scikit-learn
numpy

These packages are listed in requirements.txt.

---

# How to Start the Project

Open the project folder in Visual Studio Code.

Open the terminal in VS Code.

Create a virtual environment:

python -m venv .venv

Activate the virtual environment.

On Windows:

.venv\Scripts\activate

On Mac or Linux:

source .venv/bin/activate

Install the required packages:

pip install -r requirements.txt

Run the app:

python app.py

After running the app, the terminal should show a local web address like:

http://127.0.0.1:5000

Open that address in your browser.

The web app should now be running.

---

# How to Use the App

When the app opens in the browser, you will see a text box with example stops.

Each stop should be written on its own line.

The format is:

Name, latitude, longitude, packages, priority

Example:

Warehouse A,33.4662,-112.0318,4,5
Customer B,33.5092,-112.0857,2,3
Customer C,33.4152,-111.8315,6,4

The first value is the stop name.

The second value is latitude.

The third value is longitude.

The fourth value is the number of packages.

The fifth value is the priority level.

Priority is usually from 1 to 5.

1 means lower priority.

5 means higher priority.

After entering the stops, choose a traffic level and weather level.

Then click:

Optimize Route

The app will display the optimized route result.

---

# Example Input

Warehouse A,33.4662,-112.0318,4,5
Customer B,33.5092,-112.0857,2,3
Customer C,33.4152,-111.8315,6,4
Customer D,33.5806,-112.2374,1,2
Customer E,33.3062,-111.8413,3,5

---

# Example Output

The app will return something like:

Total distance: 95.42 km

Predicted time: 187.6 minutes

Recommended stop order:

Customer B
Customer D
Warehouse A
Customer C
Customer E

Route legs:

Depot to Customer B
Customer B to Customer D
Customer D to Warehouse A
Warehouse A to Customer C
Customer C to Customer E
Customer E to Depot

The exact result may vary slightly because the predictive model is trained inside the project.

---

# Important Notes

This project uses synthetic training data.

That means the predictive model is trained using generated example data, not real company delivery data.

This keeps the project simple and easy to run.

For a real-world version, the synthetic data should be replaced with real historical delivery data.

A real-world version could also use:

Google Maps API
Mapbox API
Live traffic data
Real driver delivery times
Vehicle capacity limits
Delivery time windows
Multiple drivers
Database storage

---

# Beginner Explanation

This project is like a simple delivery planning assistant.

Instead of manually guessing which stop should come first, the app checks the stops and predicts how long each trip might take.

Then it builds a route that should take less time.

The machine learning part predicts travel time.

The optimization part decides the stop order.

The Flask part creates the web page so people can use the system in a browser.

---

# How to Stop the App

Go back to the VS Code terminal.

Press:

Ctrl + C

This stops the local Flask server.

---

# Troubleshooting

If python app.py does not work, make sure you are inside the correct project folder.

The folder should contain:

app.py
route_optimizer.py
requirements.txt
templates

If Flask is missing, run:

pip install -r requirements.txt

If the browser does not open automatically, manually go to:

http://127.0.0.1:5000

If the terminal says Python is not recognized, reinstall Python and make sure Add Python to PATH is selected during installation.

---

# Project Summary

This Simple Intelligent Route Optimizer is my simple Python project that combines machine learning and route optimization.

It predicts route travel time using a trained model and then finds a better order for delivery stops.

The project is small, easy to run, and useful for demonstrating predictive modeling, optimization, and web app development.
