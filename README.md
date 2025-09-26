# Exercise 3.4 — Regular expressions of *Frankenstein*

This project searches **Frankenstein; Or, The Modern Prometheus** (Project Gutenberg) for the pattern:

- **`for … years`**, where the dots stand for **one or more words** between “for” and “years”.  
- We do **no heavy preprocessing** (per the instructions). We only trim the Gutenberg header/footer so the matches reflect the novel’s body text.

## Approach (regex)

Python `re` pattern (case‑insensitive):

```
(?i)for\s+([\w’'-]+(?:\s+[\w’'-]+)*)\s+years
```

- `(?i)` — case insensitive
- `for` … `years` — anchors the phrase
- `([\w’'-]+(?:\s+[\w’'-]+)*)` — captures **one or more words** (letters/digits/apostrophes/hyphen) in between
- We additionally **count words** in the capture group and keep basic context.

## How to run

Inside the project folder:

    # (optional) create & activate venv
    python3 -m venv .venv
    source .venv/bin/activate

    # run
    python regex_for_years.py

Outputs go to `outputs/`:
- `for_years.csv` — full matches with indices and context
- `preview.md` — human‑readable summary

## Results

Total matches found: **12**.

Below are the 12 matches (start/end are character offsets in the cleaned text). Context is lightly trimmed.

1. **for the first fourteen years** — between: `the first fourteen` (3 words), start=9592, end=9620  
   *…of difficulties. But it is a still greater evil to me that I am self-educated:* **for the first fourteen years** *of my life I ran wild on a common…*

2. **for many years** — between: `many` (1), 15905–15919  
   *…more fortunate than I, who may not see my native land, perhaps,* **for many years** *. I am, however, in good spirits…*

3. **for many years** — between: `many` (1), 32621–32635  
   *…My ancestors had been* **for many years** *counsellors and syndics…*

4. **for several years** — between: `several` (1), 37552–37569  
   *…I remained* **for several years** *their only child…*

5. **for nearly two years** — between: `nearly two` (2), 86349–86369  
   *…I had worked hard* **for nearly two years** *, for the sole purpose of infusing life…*

6. **for nearly six years** — between: `nearly six` (2), 119581–119601  
   *…which I had not seen* **for nearly six years** *…*

7. **for many years** — between: `many` (1), 139303–139317  
   *…witnesses were called who had known her* **for many years** *, and they spoke well of her…*

8. **for five and at another for nearly two years** — between: `five and at another for nearly two` (7), 140199–140243  
   *…at one time* **for five and at another for nearly two years** *. During all that period she appeared to me the most amiable…*

9. **for many years** — between: `many` (1), 216037–216051  
   *…where he had lived* **for many years** *in affluence…*

10. **for many years** — between: `many` (1), 216579–216593  
   *…had inhabited Paris* **for many years** *, when, for some reason…*

11. **for several years** — between: `several` (1), 408349–408366  
   *…the only happy one which I have enjoyed* **for several years** *. The forms of the beloved dead…*

12. **For forty years** — between: `forty` (1), 438067–438082  
   *…that could be freely shared with anyone.* **For forty years** *, he produced and distributed Project Gutenberg™ eBooks…*

> **Note**: #12 occurs in the Gutenberg license section; if your instructor prefers *only* narrative matches, filter out lines whose surrounding context mentions “Project Gutenberg”.

## Files

- `regex_for_years.py` — main script (download → trim boilerplate → regex → CSV/MD)
- `outputs/for_years.csv` — full table with columns: `match,start,end,between_words,num_words,left_context,right_context`
- `outputs/preview.md` — quick preview

---

*Course: Statistical Methods for Text Data Analysis — Exercise 3.4*
