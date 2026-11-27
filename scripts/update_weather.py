"""Fetch a 7-day forecast for every place in data/spots.json from Open-Meteo (free, no key).
Writes data/weather.json. Run by the daily GitHub Actions job."""
import json, urllib.request, urllib.parse, datetime, pathlib, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
spots = json.loads((ROOT / "data" / "spots.json").read_text())

def get(url, tries=4):
    for n in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.loads(r.read())
        except Exception:
            if n == tries - 1:
                raise
            time.sleep(3 * (n + 1))

def coords(s):
    if "lat" in s and "lon" in s:
        return s["lat"], s["lon"]
    q = urllib.parse.urlencode({"name": s["name"].split(" (")[0].split(" & ")[0], "count": 1, "country_code": "IN"})
    res = get("https://geocoding-api.open-meteo.com/v1/search?" + q).get("results") or []
    return (res[0]["latitude"], res[0]["longitude"]) if res else (None, None)

out = {"updated": datetime.datetime.utcnow().isoformat() + "Z", "source": "https://open-meteo.com/", "places": {}}
for s in spots:
    lat, lon = coords(s)
    if lat is None:
        continue
    q = urllib.parse.urlencode({"latitude": lat, "longitude": lon, "timezone": "Asia/Kolkata", "forecast_days": 7,
                                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code"})
    try:
        d = get("https://api.open-meteo.com/v1/forecast?" + q)["daily"]
    except Exception as e:
        print("skip", s["id"], e)
        continue
    out["places"][s["id"]] = {"days": [
        {"date": t, "tmax": a, "tmin": b, "rain": p or 0, "code": c}
        for t, a, b, p, c in zip(d["time"], d["temperature_2m_max"], d["temperature_2m_min"], d["precipitation_sum"], d["weather_code"])]}
    time.sleep(0.2)

(ROOT / "data" / "weather.json").write_text(json.dumps(out, indent=1))
print("weather for", len(out["places"]), "places")
