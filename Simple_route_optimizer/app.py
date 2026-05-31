from flask import Flask, render_template, request

from route_optimizer import optimize_route, parse_stops

app = Flask(__name__)

EXAMPLE_STOPS = """Warehouse A,33.4662,-112.0318,4,5
Customer B,33.5092,-112.0857,2,3
Customer C,33.4152,-111.8315,6,4
Customer D,33.5806,-112.2374,1,2
Customer E,33.3062,-111.8413,3,5"""


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    raw_stops = EXAMPLE_STOPS
    traffic = 2
    weather = 1

    if request.method == "POST":
        raw_stops = request.form.get("stops", "")
        traffic = int(request.form.get("traffic", 2))
        weather = int(request.form.get("weather", 1))

        try:
            stops = parse_stops(raw_stops)
            result = optimize_route(stops, traffic=traffic, weather=weather)
        except Exception as exc:
            error = str(exc)

    return render_template(
        "index.html",
        raw_stops=raw_stops,
        traffic=traffic,
        weather=weather,
        result=result,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)