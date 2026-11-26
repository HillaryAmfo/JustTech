import io
import os
import re
import sys

sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "just_tech.settings")

import django

django.setup()

from django.test import Client

c = Client(SERVER_NAME="localhost")
c.cookies["lang"] = "fr"
r = c.get("/services/", HTTP_HOST="localhost")
html = r.content.decode("utf-8")
print("status:", r.status_code)
print("intro FR:", "Vous vous concentrez sur l’événement" in html)
lanes = re.findall(r"fl-lane--[ab]", html)
print("lanes A/B counts:", lanes.count("fl-lane--a"), lanes.count("fl-lane--b"))
print("wide+hex cards:", html.count("fl-card--wide"), html.count("fl-card--hex"))
print("monogram handles:", html.count("fl-card-monogram-text"))
print("FR fact:", "Scène live" in html)
print("FR role (encore):", "jusqu’au rappel" in html)
print("FR alt (pre-existing):", "Public de concert sous les lumières de scène" in html)
leaks = sum(
    html.count(x)
    for x in ["We arrive early and tune", "Full shows — FOH mixing, monitoring"]
)
print("EN leak sample count:", leaks)
print("coords markers:", html.count("+005.6037"))
base = open("templates/main_app/base.html", encoding="utf-8").read()
print("css v48:", "?v=48" in base, "(v47 leak:", "?v=47" in base, ")")