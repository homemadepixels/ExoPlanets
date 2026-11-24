# UX Brief: ExoPlanets

_Last updated: Nov 24, 2026 by App UX Partner_

## What the app is
- **One line:** An iPhone app for exploring every known exoplanet on a map of the Milky Way, and finding the ones most like Earth.
- **Platforms:** iOS · phone
- **Who it's for:** Curious people who want to explore exoplanets visually (no login, no onboarding; people jump straight in).
- **Main job:** Find exoplanets on the galaxy map, narrow them down by how Earth-like they are, and learn about one planet before backing out to look for another.

## Current stage
2 Shaping · 3 Flows · 5 Critique (first ideation round; nothing is set in stone yet)

## Screens (Marcus's current plan, still open to change)
| Screen | Type | Purpose | Key UI | Notes |
| --- | --- | --- | --- | --- |
| Galaxy map | Maps and location | Home screen. Shows where exoplanets are. | Milky Way map with planet dots; floating card at the bottom with sliders (size vs Earth, warmth vs Earth, etc.) | Built as a web prototype in `web/index.html` |
| Search and A–Z list | Search and filters, Lists | Find a planet by name, or browse the planets that match the current sliders | Inside the floating card, possibly as a tab | |
| Planet details | Detail page | Picture of the planet and a short description | One card in a swipeable carousel | |
| Planet vs Earth | Detail page | Compare the planet with Earth | Second card in the carousel | |
| Its solar system vs ours | Detail page | Compare the planet's star system with ours | Third card in the carousel | |

## Flows (decided)
- None yet.

## Navigation model
- Not decided. Current leaning: the map is the one main screen, with everything else floating above it.

## Design decisions
| Date | Decision | Layer (proven / standout / avant-garde) | Why | Reference |
| --- | --- | --- | --- | --- |
| Nov 24, 2026 | No login and no onboarding; people start on the map | Proven | Let people get value first | `references/app-structure-and-flows.md` ("Ask only what you need") |

## Suggested in round 1, waiting on Marcus
| Date | Idea | Layer | Reference |
| --- | --- | --- | --- |
| Nov 24, 2026 | Map is the only main screen; no tab bar. Everything else is a sheet over it. | Proven | Uber ride flow, AllTrails (Mobbin) |
| Nov 24, 2026 | Bottom sheet with 3 heights: peek (search box + "1,204 planets match" + filter chips), half (results list), full (list with sort + A–Z index). One list instead of tabs. | Proven | Klook, Strava map filters (Mobbin) |
| Nov 24, 2026 | Sliders move out of the card into one filter sheet per chip, with a live match count; a one-tap "Like Earth" preset | Proven + standout | Strava length filter (Mobbin) |
| Nov 24, 2026 | Planet opens as a sheet over the map (map flies to it). Swipe down or X returns to the same results, filters and zoom. | Proven | Airbnb map card, AllTrails place sheet (Mobbin) |
| Nov 24, 2026 | Replace the 3-card side-swipe carousel with one scrolling detail page with jump chips (Overview · vs Earth · Its system). Use side-swipe for next/previous planet in the results instead. | Proven | `references/detail-pages.md` |
| Nov 24, 2026 | Earth comparison as paired bars plus plain-English lines ("A year here lasts 37 days") | Proven + standout | Hevy comparison, MLS stats (Mobbin) |
| Nov 24, 2026 | "Sky from here" view: the star's size and color in the sky vs our Sun | Avant-garde | Sky Guide (ADA Spatial Computing finalist 2024) for the motion idea |
| Nov 24, 2026 | Discovery timeline slider that replays planets appearing 1992 → today | Avant-garde | Needs discovery year added to the catalog |
| Nov 24, 2026 | Extra screens: Saved planets, Famous planets / tours, About the data, "New since your last visit" | Proven + standout | |

## Explored but not chosen
| Date | Idea | Why not | Reference |
| --- | --- | --- | --- |
| | | | |

## Open questions
- [ ] Keep the 3-card side-swipe for details, or switch to one scrolling page with jump chips?
- [ ] Which 3–4 filters show as chips by default, and which go under "More filters"?
- [ ] How should the planet picture be labeled, since almost all are artist's impressions?
- [ ] How does a tap pick a planet when many dots overlap on a phone screen?
- [ ] Which desktop prototype controls stay on phone (zoom buttons, depth tuning panel)?

## Session log
- Nov 24, 2026: First session. Wrote the brief from Marcus's description of the app and the README. Gave round 1 of written suggestions on structure, the map sheet, filters, details and comparison pages, and extra screens.
