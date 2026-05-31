from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt
from typing import Iterable, List, Tuple

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass
class Stop:
    name: str
    lat: float
    lon: float
    packages: int = 1
    priority: int = 3


@dataclass
class RouteResult:
    ordered_stops: List[Stop]
    total_distance_km: float
    estimated_minutes: float
    legs: List[dict]


DEPOT = Stop("Depot", 33.4484, -112.0740, 0, 3)


def haversine_km(a: Stop, b: Stop) -> float:
    earth_radius_km = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [a.lat, a.lon, b.lat, b.lon])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * earth_radius_km * asin(sqrt(h))


def train_predictive_model(random_seed: int = 42) -> Pipeline:
    rng = np.random.default_rng(random_seed)
    sample_count = 1200

    distance_km = rng.uniform(0.5, 35, sample_count)
    traffic = rng.integers(1, 4, sample_count)
    weather = rng.integers(1, 4, sample_count)
    packages = rng.integers(1, 12, sample_count)
    priority = rng.integers(1, 6, sample_count)

    base_minutes = distance_km * 2.15
    traffic_penalty = traffic * distance_km * 0.55
    weather_penalty = weather * distance_km * 0.25
    service_time = packages * 1.8
    priority_bonus = (6 - priority) * 0.4
    noise = rng.normal(0, 3, sample_count)

    minutes = base_minutes + traffic_penalty + weather_penalty + service_time + priority_bonus + noise
    minutes = np.maximum(minutes, 2)

    features = np.column_stack([distance_km, traffic, weather, packages, priority])

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("regressor", RandomForestRegressor(n_estimators=80, random_state=random_seed)),
        ]
    )

    model.fit(features, minutes)
    return model


MODEL = train_predictive_model()


def predict_leg_minutes(start: Stop, end: Stop, traffic: int, weather: int) -> float:
    distance = haversine_km(start, end)
    features = np.array([[distance, traffic, weather, end.packages, end.priority]])
    return float(MODEL.predict(features)[0])


def score_route(stops: Iterable[Stop], traffic: int, weather: int, depot: Stop = DEPOT) -> Tuple[float, float, List[dict]]:
    ordered = list(stops)
    current = depot
    total_distance = 0.0
    total_minutes = 0.0
    legs = []

    for stop in ordered:
        distance = haversine_km(current, stop)
        minutes = predict_leg_minutes(current, stop, traffic, weather)

        legs.append(
            {
                "from": current.name,
                "to": stop.name,
                "distance_km": round(distance, 2),
                "estimated_minutes": round(minutes, 1),
            }
        )

        total_distance += distance
        total_minutes += minutes
        current = stop

    distance = haversine_km(current, depot)
    minutes = predict_leg_minutes(current, depot, traffic, weather)

    legs.append(
        {
            "from": current.name,
            "to": depot.name,
            "distance_km": round(distance, 2),
            "estimated_minutes": round(minutes, 1),
        }
    )

    total_distance += distance
    total_minutes += minutes

    return total_distance, total_minutes, legs


def nearest_neighbor_route(stops: List[Stop], traffic: int, weather: int, depot: Stop = DEPOT) -> List[Stop]:
    unvisited = stops.copy()
    route = []
    current = depot

    while unvisited:
        best_stop = min(
            unvisited,
            key=lambda stop: predict_leg_minutes(current, stop, traffic, weather),
        )
        route.append(best_stop)
        unvisited.remove(best_stop)
        current = best_stop

    return route


def two_opt_improve(route: List[Stop], traffic: int, weather: int) -> List[Stop]:
    if len(route) < 4:
        return route

    best_route = route.copy()
    _, best_minutes, _ = score_route(best_route, traffic, weather)
    improved = True

    while improved:
        improved = False

        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route)):
                if j - i == 1:
                    continue

                candidate = best_route[:i] + best_route[i:j][::-1] + best_route[j:]
                _, candidate_minutes, _ = score_route(candidate, traffic, weather)

                if candidate_minutes < best_minutes:
                    best_route = candidate
                    best_minutes = candidate_minutes
                    improved = True

    return best_route


def optimize_route(stops: List[Stop], traffic: int = 2, weather: int = 1) -> RouteResult:
    first_route = nearest_neighbor_route(stops, traffic, weather)
    improved_route = two_opt_improve(first_route, traffic, weather)

    total_distance, estimated_minutes, legs = score_route(improved_route, traffic, weather)

    return RouteResult(
        ordered_stops=improved_route,
        total_distance_km=round(total_distance, 2),
        estimated_minutes=round(estimated_minutes, 1),
        legs=legs,
    )


def parse_stops(raw_text: str) -> List[Stop]:
    stops = []

    for line_number, line in enumerate(raw_text.strip().splitlines(), start=1):
        if not line.strip():
            continue

        parts = [part.strip() for part in line.split(",")]

        if len(parts) < 3:
            raise ValueError(f"Line {line_number} needs at least: name, latitude, longitude")

        name = parts[0]
        lat = float(parts[1])
        lon = float(parts[2])
        packages = int(parts[3]) if len(parts) >= 4 and parts[3] else 1
        priority = int(parts[4]) if len(parts) >= 5 and parts[4] else 3

        stops.append(Stop(name, lat, lon, packages, priority))

    return stops