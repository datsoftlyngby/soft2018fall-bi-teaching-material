import os
import csv
import pygal
import webbrowser
import numpy as np
import country_codes as cc
from download import download, get_url_from_config_file


def load_csv(path_to_file):
    """A function to demonstrate reading CSV files with the `csv` module."""
    with open(path_to_file) as cfg_file:
        reader = csv.reader(cfg_file)
        header_row = next(reader)
        rows = [row for row in reader]

    return header_row, rows


def load_csv_with_numpy(path_to_file):
    data = np.genfromtxt(path_to_file, delimiter=',', dtype=np.uint)
    return data[1:]  # Ignore the header row


def analyze_development_of_nationality_over_time(nationality, data):
    """Let's say we want to see the development of how many people from a 
    certain country lived in CPH in a respective year."""

    if type(nationality) == str:
        nationality = cc.lang_to_code[nationality]

    years = np.unique(data[:, 0])
    development = []
    for year in years:
        amount = data[(data[:, 3] == nationality) &
                      (data[:, 0] == year)][:, -1].sum()
        development.append((int(year), int(amount)))

    np.savetxt('development.tsv', np.array(
        development, np.uint), delimiter="\t", fmt='%u')

    return development


def analyze_where_to_place(nationality, data):
    if type(nationality) == str:
        nationality = cc.lang_to_code[nationality]
    years = np.unique(data[:, 0])
    neighborhoods = np.unique(data[:, 1])

    development = []
    for year in years:
        for neighborhood in neighborhoods:
            amount = data[(data[:, 3] == nationality) &
                          (data[:, 1] == neighborhood) &
                          (data[:, 0] == year)][:, -1].sum()
            development.append(
                (int(year), int(neighborhood), int(amount)))

    development = np.array(development)
    max_neighborhoods = []
    for year in years:
        data_for_year = development[development[:, 0] == year]
        max_for_year = data_for_year[data_for_year[:, 2] == np.max(
            data_for_year[:, 2])]
        for n in max_for_year[:, 1]:
            max_neighborhoods.append((int(year), str(cc.neighborhoods[n])))
    return max_neighborhoods


def plot(xs, ys, nationality):
    if type(nationality) == int:
        nationality = cc.code_to_lang[nationality]

    line_chart = pygal.Line()
    line_chart.title = f'Amount of {nationality} over the years'
    line_chart.x_labels = xs
    line_chart.add(nationality, ys)

    line_chart.render_to_file('development.html')

    webbrowser.open('file://' + os.path.abspath('./development.html'))


def main():
    url = get_url_from_config_file()
    download(url)
    content = load_csv_with_numpy('befkbhalderstatkode.csv')
    nationality = 5134  # 'Tyrkiet'  # 5180  # 'Frankrig'
    stats = analyze_development_of_nationality_over_time(nationality, content)
    years, freqs = zip(*stats)
    plot(years, freqs, nationality)


if __name__ == '__main__':
    main()
