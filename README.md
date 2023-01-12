# Meal Planner

## A Scale-based Inventory Management System

### Overview



### Installation

A Python virtual environment is recommended. The Python requirements can be installed with `pip install -r requirements.txt`. To run the app, run `uvicorn main:app --reload`.

A systemd unit file is included in `/systemd/`. This should be moved to `/etc/systemd/system/` and enabled. It will run the application on a unix socket at `/tmp/mealplanner.service`.

Also included is an nginx config file in `/nginx/`. This should be moved to `/etc/nginx/sites-available/` and linked to `/etc/nginx/sites-enabled/`. It will listen on port 80 and forward to the unix socket at `/tmp/mealplanner.sock`.
