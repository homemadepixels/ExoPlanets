"""Make the small data file the map page uses (web/data/planets_web.json).
Run after build_catalog.py:  python3 scripts/build_web_data.py
Only planets with a distance, planet size and star temperature are included,
because the first three sliders require those values. The later sliders (mass,
starlight, star age, gravity) may be empty; the map hides those planets only
when that slider is in use."""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SUN_TEMP_K = 5772  # our Sun's surface temperature (IAU nominal value)

p = pd.read_csv(ROOT / "catalog" / "planets.csv")
keep = p.dropna(subset=["distance_ly", "planet_size_earths", "star_temp_k", "x_ly", "y_ly"])
fields = ["planet_name", "star_system", "found_by", "x_ly", "y_ly", "distance_ly",
          "planet_size_earths", "planet_size_source", "star_temp_k", "star_type",
          "star_type_source", "star_distance_au", "star_size_suns",
          "planet_mass_earths", "planet_mass_source", "starlight_earths", "starlight_source",
          "star_age_gyr", "star_age_source", "surface_gravity_earths", "surface_gravity_source"]
rows = []
for _, r in keep[fields].iterrows():
    rows.append([None if pd.isna(v) else (round(v, 4) if isinstance(v, float) else v) for v in r])
meta = json.loads((ROOT / "catalog" / "planets.json").read_text())["meta"]
out = {"fields": fields, "sun_temp_k": SUN_TEMP_K,
       "planets_in_catalog": int(len(p)), "planets_hidden_missing_data": int(len(p) - len(keep)),
       "nasa_download": meta["nasa_download"], "planets": rows}
(ROOT / "web" / "data" / "planets_web.json").write_text(json.dumps(out, separators=(",", ":")))
print(len(keep), "planets written;", len(p) - len(keep), "hidden for missing size or star temperature")
