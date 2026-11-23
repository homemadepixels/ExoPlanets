"""Build the ExoPlanets catalog (pass 1) from the NASA Exoplanet Archive download.

Input:  the single *.csv.zip in the repo root (NASA "Planetary Systems Composite
        Parameters" table, all columns, all rows, CSV).
Output: catalog/planets.csv, catalog/planets.json, catalog/skipped_no_distance.csv

Run from the repo root:  python3 scripts/build_catalog.py
To add a field in a later pass, add it to build_row() and run again.
"""
import glob, io, json, math, sys, zipfile
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "catalog"
PC_TO_LY = 3.26156  # 1 parsec in light-years


def load_nasa():
    zips = glob.glob(str(ROOT / "*.csv.zip"))
    if len(zips) != 1:
        sys.exit(f"Expected exactly one *.csv.zip in the repo root, found {len(zips)}")
    with zipfile.ZipFile(zips[0]) as z:
        names = [n for n in z.namelist() if n.endswith(".csv") and not n.startswith("__MACOSX")]
        raw = z.read(names[0]).decode("utf-8")
    created = raw.splitlines()[1].lstrip("# ").strip()  # NASA's download timestamp
    df = pd.read_csv(io.StringIO(raw), comment="#", low_memory=False)
    return df, Path(zips[0]).name, names[0], created


def num(v, digits=None):
    if v is None or pd.isna(v):
        return None
    v = float(v)
    return round(v, digits) if digits is not None else v


def limit_source(lim, default="measured"):
    if lim == 1:
        return "upper limit"   # true value is at most this
    if lim == -1:
        return "lower limit"   # true value is at least this
    return default


def value_with_range(r, col, scale=1.0, digits=4, calc_label=None):
    """Value, plus/minus range, and where it came from."""
    v = r.get(col)
    if pd.isna(v):
        return None, None, None, "not measured"
    src = "measured"
    if calc_label and "CALCULATED" in str(r.get(col + "_reflink", "")):
        src = calc_label
    src = limit_source(r.get(col + "lim"), src)
    plus = num(r.get(col + "err1"))
    minus = num(r.get(col + "err2"))
    return (round(v * scale, digits),
            None if plus is None else round(plus * scale, digits),
            None if minus is None else round(abs(minus) * scale, digits),
            src)


def star_type(r):
    t = r.get("st_spectype")
    if isinstance(t, str) and t.strip():
        return t.strip(), "measured"
    temp = r.get("st_teff")
    if pd.isna(temp):
        return None, "not measured"
    # Standard temperature ranges for the main star types (Kelvin)
    for low, letter in [(30000, "O"), (10000, "B"), (7500, "A"), (6000, "F"),
                        (5200, "G"), (3700, "K"), (0, "M")]:
        if temp >= low:
            return letter, "estimated from temperature"


def position(r):
    """Sun at (0,0,0). x points to the galaxy's center, y points the way the Sun
    is moving around the galaxy, z points 'up' out of the disk. Light-years."""
    d = r["sy_dist"] * PC_TO_LY
    l, b = math.radians(r["glon"]), math.radians(r["glat"])
    return (round(d * math.cos(b) * math.cos(l), 3),
            round(d * math.cos(b) * math.sin(l), 3),
            round(d * math.sin(b), 3))


def build_row(r):
    row = {
        "planet_name": r["pl_name"],
        "star_system": r["hostname"],
        "planets_in_system": int(r["sy_pnum"]) if not pd.isna(r["sy_pnum"]) else None,
        "found_by": r["discoverymethod"],
    }
    # 1. Position
    dist, dplus, dminus, _ = value_with_range(r, "sy_dist", PC_TO_LY, 3)
    x, y, z = position(r)
    row.update({
        "sky_ra_deg": num(r["ra"], 6), "sky_dec_deg": num(r["dec"], 6),
        "galactic_lon_deg": num(r["glon"], 6), "galactic_lat_deg": num(r["glat"], 6),
        "distance_ly": dist, "distance_ly_plus": dplus, "distance_ly_minus": dminus,
        "x_ly": x, "y_ly": y, "z_ly": z,
    })
    # 2. Planet size (Earth = 1)
    v, p, m, s = value_with_range(r, "pl_rade", calc_label="estimated from mass")
    row.update({"planet_size_earths": v, "planet_size_plus": p, "planet_size_minus": m,
                "planet_size_source": s})
    # 3. Distance from its star (AU; Earth to Sun = 1)
    v, p, m, s = value_with_range(r, "pl_orbsmax", digits=6)
    row.update({"star_distance_au": v, "star_distance_plus": p, "star_distance_minus": m,
                "star_distance_source": s})
    # 4. Star type (with temperature kept as backup)
    t, s = star_type(r)
    row.update({"star_type": t, "star_type_source": s,
                "star_temp_k": num(r.get("st_teff"), 1)})
    # 5. Star size (Sun = 1)
    v, p, m, s = value_with_range(r, "st_rad")
    row.update({"star_size_suns": v, "star_size_plus": p, "star_size_minus": m,
                "star_size_source": s})
    # ---- Pass 2 ----
    # 6. Planet mass (Earth = 1). NASA's "best mass" can be a true mass, a minimum
    #    mass (wobble method only gives a lower bound), or an estimate from the size.
    v, p, m, s = value_with_range(r, "pl_bmasse")
    prov = str(r.get("pl_bmassprov", ""))
    if v is not None and s == "measured":
        s = {"Msini": "minimum mass", "M-R relationship": "estimated from size"}.get(prov, "measured")
    row.update({"planet_mass_earths": v, "planet_mass_plus": p, "planet_mass_minus": m,
                "planet_mass_source": s})
    # 7. Starlight received (Earth = 1): energy the planet gets from its star
    v, p, m, s = value_with_range(r, "pl_insol", calc_label="calculated from star brightness and orbit")
    row.update({"starlight_earths": v, "starlight_plus": p, "starlight_minus": m, "starlight_source": s})
    # 8. Star age (billions of years; Sun = 4.6)
    v, p, m, s = value_with_range(r, "st_age")
    row.update({"star_age_gyr": v, "star_age_plus": p, "star_age_minus": m, "star_age_source": s})
    # 9. Surface gravity (Earth = 1) = mass / radius^2, both in Earth units
    mass, rad = row["planet_mass_earths"], row["planet_size_earths"]
    if mass is None or rad is None or rad <= 0:
        g, gs = None, "not measured"
    else:
        g = round(mass / rad ** 2, 4)
        ms, rs = row["planet_mass_source"], row["planet_size_source"]
        if rs == "measured" and ms == "measured":
            gs = "calculated from measured mass and size"
        elif rs == "measured" and ms == "minimum mass":
            gs = "calculated from minimum mass (true value may be higher)"
        else:
            gs = "uses estimated values"
    row.update({"surface_gravity_earths": g, "surface_gravity_source": gs})
    return row


def main():
    df, zip_name, csv_name, created = load_nasa()
    OUT.mkdir(exist_ok=True)
    has_dist = df["sy_dist"].notna() & df["glon"].notna() & df["glat"].notna()
    planets = pd.DataFrame([build_row(r) for _, r in df[has_dist].iterrows()])
    planets = planets.sort_values("distance_ly", kind="stable").reset_index(drop=True)
    planets.to_csv(OUT / "planets.csv", index=False)

    meta = {"source": "NASA Exoplanet Archive, Planetary Systems Composite Parameters (PSCompPars)",
            "nasa_download": created, "input_file": f"{zip_name} / {csv_name}",
            "planets_in_nasa_file": int(len(df)), "planets_in_catalog": int(len(planets)),
            "planets_skipped_no_distance": int((~has_dist).sum()),
            "coordinates": "Sun at origin; x toward galactic center, y toward direction of travel, z out of the disk; light-years"}
    records = json.loads(planets.to_json(orient="records"))
    (OUT / "planets.json").write_text(json.dumps({"meta": meta, "planets": records}, indent=1))

    skipped = df[~has_dist][["pl_name", "hostname", "discoverymethod"]].rename(
        columns={"pl_name": "planet_name", "hostname": "star_system", "discoverymethod": "found_by"})
    skipped.sort_values("planet_name").to_csv(OUT / "skipped_no_distance.csv", index=False)

    print(json.dumps(meta, indent=1))
    for col in ["planet_size_source", "star_distance_source", "star_type_source", "star_size_source",
                "planet_mass_source", "starlight_source", "star_age_source", "surface_gravity_source"]:
        print(col, planets[col].value_counts().to_dict())


if __name__ == "__main__":
    main()
