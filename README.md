# Pune Trip Planner

A road-trip planner for a vegetarian family travelling by car from Pune. It follows a simple method:

1. **Priorities, in order:** budget (₹), happiness, health, relaxing as well as experience, time.
2. **Pass/fail rules first:** budget cap, maximum driving hours a day, no driving after dark, in-season places only, pure veg meals.
3. **Distance rings from Pune:** up to about 300 km for 2–3 days, 350–500 km for the first stop of a week-long trip.
4. **Rhythm:** after each travel day, at least one stay day. Every day gets one relaxing slot and one experience slot.

## What's in the app

| Tab | What it does |
| --- | --- |
| Explore | 29 places around Pune with experience tags, best months, veg rating, local tips, risks, a Maps route link and a 7-day forecast |
| Plan | Trip brief, then a Claude prompt you copy into Claude; paste the answer back to see and save the plan |
| Trips | Saved trips with spending log and after-trip review |
| Stays | Saved stays plus compare links for today's prices |
| Prep | Countdown checklist for 30 days, 7 days and 1 day before leaving |
| Road watch | Road news and closures with sources and the date checked |
| Research log | Every search, with sources; backup and restore of your changes |

## Where the data lives

- `data/*.json`: places, stays, routes, road alerts, research and the checklist. Edit these files (or ask Claude) to update them for everyone.
- `data/weather.json`: written every morning by the GitHub Actions job from [Open-Meteo](https://open-meteo.com/).
- Your own trips, spending and ticks are saved in your browser. Use **Download backup** in the Research log tab to move them.

## Running it

GitHub Pages hosts the site. The workflow in `.github/workflows/deploy.yml` runs on every push and every day at 6 AM IST: it refreshes the weather and redeploys.

To run it on your computer: `python3 -m http.server` in this folder, then open http://localhost:8000.

Distances and drive times are approximate. Always check road news 7 days before you leave.
