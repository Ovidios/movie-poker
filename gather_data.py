import rottentomatoes as rt
from bs4 import BeautifulSoup
import urllib.request, json

# get a list of the top movies of each of the last few years
years = list(range(1980, 2023))
movies = []

for year in years:
    print(year)
    uf = urllib.request.urlopen(f"https://www.boxofficemojo.com/year/{year}/")
    html = uf.read()
    soup = BeautifulSoup(html, "html.parser")
    tds = soup.find_all("td")
    num = 0
    max_num = 25
    for td in tds:
        a = td.find("a")
        if a:
            text = a.get_text()
            if not "\n\n" in text:
                num += 1
                # only take top 25 movies
                if num > max_num:
                    break
                movies.append(text)

# collect movie information
output = []
for movie in movies:
    print("> " + movie)
    info, url = None, None

    # find movie using RT API
    try:
        info = rt.Movie(movie)
        url = rt.search.top_movie_result(movie).url
    except:
        print(f"Couldn't find Movie: {movie}")
        continue

    # get movie synopsis seperately
    uf = urllib.request.urlopen(url)
    html = uf.read()
    soup = BeautifulSoup(html, "html.parser")
    synopsis = soup.find(id="movieSynopsis").get_text().strip()

    # append info to output
    output.append({
        "title": info.movie_title,
        "tomatometer": info.tomatometer,
        "audience": info.audience_score,
        "genres": ", ".join(info.genres),
        "actors": ", ".join(info.actors),
        "directors": ", ".join(info.directors),
        "year": info.year_released,
        "runtime": info.duration,
        "synopsis": synopsis
    })

with open("data.json", "w") as outfile:
    outfile.write(json.dumps(output))