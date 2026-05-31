# Simple Intelligent Route Optimizer

I built this project as a lightweight route optimization system with a basic predictive travel-time model.

The app lets a user enter delivery stops, choose traffic and weather conditions, and generate an optimized route. It predicts the estimated time between stops, then uses those predictions to recommend a better stop order.

## What It Does

- Accepts delivery stops with latitude, longitude, package count, and priority
- Estimates travel/service time using a machine learning regression model
- Optimizes the route using predicted travel time
- Shows the recommended stop order
- Displays total distance, predicted time, and each route leg

![imagealt](https://github.com/GradualRelease22/route_optimizer_with_PredictiveModeling/blob/main/RouteOpt_Github.png)

![imagealt](https://github.com/GradualRelease22/route_optimizer_with_PredictiveModeling/blob/main/RouteOpt_Result_GitHub.png)








## Tech Stack

- Python
- Flask
- scikit-learn
- NumPy
- HTML/CSS

## How It Works

The predictive model estimates how long each route leg may take based on distance, traffic, weather, package count, and priority.

The optimizer then uses those predicted times to build a more efficient route. It starts with a nearest-neighbor approach and improves the result with a simple 2-opt optimization step.

The model is trained on synthetic data, so this project is meant as a functional demo of predictive routing, not a production logistics platform.

## How to Run It

Clone or download the project.

Create a virtual environment:

```bash
python -m venv .venv

Activate it:

Windows:

.venv\Scripts\activate

Mac/Linux:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Start the app:

python app.py

Open this in your browser:

http://127.0.0.1:5000
Stop Format

Each stop should be entered like this:

Name, latitude, longitude, packages, priority

Example:

Warehouse A,33.4662,-112.0318,4,5
Customer B,33.5092,-112.0857,2,3
Customer C,33.4152,-111.8315,6,4
Notes

I kept this project simple on purpose. The goal was to build a clean, understandable route optimization app that still includes a real predictive modeling component.

A future version would use real delivery history, live traffic APIs, driver schedules, time windows, and multiple vehicles.
