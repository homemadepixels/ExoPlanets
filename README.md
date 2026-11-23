# ExoPlanets

A catalog of every confirmed exoplanet with a known distance, one entry per planet, built from NASA's data. It's the starting point for placing exoplanets on a map of the Milky Way.

**Pass 1** covers five categories: position, planet size, distance from its star, star type, and star size.

## Current numbers

| | |
|---|---|
| Planets in NASA's file | 6,473 |
| Planets in this catalog | 6,416 |
| Skipped (no distance from Earth) | 57 (see `catalog/skipped_no_distance.csv`) |
| NASA download date | Nov 22, 2026, 18:40:45 |

## Files

- `Nasa_Database_2026.11.22_18.40.45.csv.zip`: the original NASA download, untouched. Everything else is built from this file.
- `scripts/build_catalog.py`: the script that builds the catalog.
- `catalog/planets.csv`: the catalog, one row per planet, sorted from nearest to farthest. Opens in any spreadsheet app.
- `catalog/planets.json`: the same data for code and web use, plus a `meta` section with the counts and download date.
- `catalog/skipped_no_distance.csv`: planets left out because NASA lists no distance for them.

## Where the data comes from

NASA Exoplanet Archive, **Planetary Systems Composite Parameters** table
(https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PSCompPars), downloaded with all columns and all rows, as CSV, with "Values only" unchecked.

This table has one row per planet. For each planet, NASA picks the best available value for each field, and sometimes those values come from different scientific papers.

## Empty values

An empty cell means the value hasn't been measured. Wherever people will see the data, show it as **"Not measured"**. Every category also has a `_source` column that says this in words.

## Fields

### IDs and basics
| Field | Meaning |
|---|---|
| `planet_name` | NASA's official planet name. This is the ID for each planet. |
| `star_system` | Name of the star the planet orbits. Planets with the same value share a star system. |
| `planets_in_system` | How many known planets that star system has. |
| `found_by` | How the planet was discovered (Transit, Radial Velocity, Microlensing, Imaging, and others). This explains a lot of the gaps: transit planets usually have a measured size, while radial velocity (wobble) planets usually don't. |

### 1. Position
| Field | Meaning |
|---|---|
| `sky_ra_deg`, `sky_dec_deg` | Position in Earth's sky (right ascension and declination), in degrees. |
| `galactic_lon_deg`, `galactic_lat_deg` | The same position, measured against the Milky Way instead of Earth. Longitude 0 points to the galaxy's center. |
| `distance_ly` | Distance from Earth, in light-years. NASA gives this in parsecs; 1 parsec = 3.26156 light-years. |
| `distance_ly_plus`, `distance_ly_minus` | How far above and below that value the true distance could be. |
| `x_ly`, `y_ly`, `z_ly` | 3D position in light-years, with the Sun at 0,0,0. **x** points toward the galaxy's center, **y** points in the direction the Sun is moving around the galaxy, and **z** points up out of the galaxy's flat disk. These are the numbers used to place planets on a galaxy map. |

### 2. Planet size
| Field | Meaning |
|---|---|
| `planet_size_earths` | Planet radius. Earth = 1. |
| `planet_size_plus`, `planet_size_minus` | Give-or-take range. |
| `planet_size_source` | `measured`, `estimated from mass` (NASA calculated the size from the planet's mass because it wasn't measured directly), `lower limit` (the planet is at least this big), or `not measured`. |

### 3. Distance from its star
| Field | Meaning |
|---|---|
| `star_distance_au` | Average distance between the planet and its star, in AU. 1 AU is the distance from Earth to the Sun. |
| `star_distance_plus`, `star_distance_minus` | Give-or-take range. |
| `star_distance_source` | `measured`, `lower limit`, or `not measured`. |

### 4. Star type
| Field | Meaning |
|---|---|
| `star_type` | The star's type, such as `G2 V`. The first letter is the main type, from hottest to coolest: O, B, A, F, G, K, M. The Sun is a G star. |
| `star_type_source` | `measured`, `estimated from temperature`, or `not measured`. |
| `star_temp_k` | The star's surface temperature in Kelvin. When NASA lists no star type, the type is estimated from this temperature using these standard ranges: O 30,000+, B 10,000–30,000, A 7,500–10,000, F 6,000–7,500, G 5,200–6,000, K 3,700–5,200, M below 3,700. Estimated types are only the letter, with no number or size class. |

### 5. Star size
| Field | Meaning |
|---|---|
| `star_size_suns` | Star radius. Sun = 1. |
| `star_size_plus`, `star_size_minus` | Give-or-take range. |
| `star_size_source` | `measured` or `not measured`. |

## How complete each category is (pass 1)

| Category | Measured | Estimated | Limit only | Not measured |
|---|---|---|---|---|
| Position | 6,416 | – | – | 57 skipped |
| Planet size | 4,832 | 1,530 (from mass) | 5 | 49 |
| Distance from star | 5,915 | – | 4 | 497 |
| Star type | 2,398 | 3,758 (from temperature) | – | 260 |
| Star size | 6,089 | – | – | 327 |

## Things to know

- **Star values can differ a little between planets of the same star.** NASA picks star values separately for each planet, so in 191 star systems the star size isn't identical on every planet's row. The catalog keeps NASA's values as they are.
- **Some skipped planets orbit well-known stars.** For example, GJ 504 b is skipped because NASA's table leaves its distance blank, even though its star is well studied.
- **Planets found by microlensing** are often far away, toward the galaxy's center, and usually have only rough values.

## Updating the catalog

1. Download a new copy of the NASA table (same settings as above) and zip it.
2. Replace the old zip in the repo root. There must be only one `.csv.zip` there.
3. From the repo root, run `python3 scripts/build_catalog.py` (needs Python with pandas).
4. Update the numbers at the top of this file.

## Next passes

Planned: placing planets on a Gaia-based Milky Way image (waiting on a closer image), then more fields such as planet mass, density, and atmosphere readings.

## Credit

Data: NASA Exoplanet Archive, operated by Caltech under contract with NASA. Please credit the archive when using this data.
