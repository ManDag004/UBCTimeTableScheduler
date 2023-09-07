from bs4 import BeautifulSoup
from .Class import Class
import requests

from .Professor import Professor

ua = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_8_2) AppleWebKit/531.2 (KHTML, like Gecko) Chrome/26.0.869.0 Safari/531.2'}

status_index = 0
section_index = 1
activity_index = 2
term_index = 3
days_index = 6
start_time_index = 7
end_time_index = 8


def scrape_course(dept, num, required_term):
    url = f"https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept={dept}&course={num}"
    result = requests.get(url, headers=ua)
    doc = BeautifulSoup(result.text, "html.parser")

    classes = []

    main_table = doc.find('table', {"class": "section-summary"})
    c = 0
    for row in main_table.findAll('tr')[1:]:

        try:
            status = row.select('tr > td')[status_index].text
            professor = None
            section = row.select('tr > td')[section_index].text
            activity = row.select('tr > td')[activity_index].text
            term = row.select('tr > td')[term_index].text
            days = row.select('tr > td')[days_index].text.strip()
            start_time = row.select('tr > td')[start_time_index].text
            end_time = row.select('tr > td')[end_time_index].text

            if term == str(required_term) and activity not in ["Waiting List"]:
                if activity == "Lecture":
                    prof_url = f"https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept={dept}&course={num}&section={section.split(' ')[2]}"

                    prof_result = requests.get(prof_url, headers=ua)
                    prof_doc = BeautifulSoup(prof_result.text, "html.parser")
                    prof_name = \
                        prof_doc.select("body > div.container > div.content.expand > table")[2].select("tr > td")[
                            1].text
                    try:
                        last, first = prof_name.split(", ")
                        professor = Professor(first.split(' ')[0].title() + " " + last.split(' ')[0].title())
                    except ValueError:
                        print("Cannot split", prof_name)
                classes.append(Class(section, start_time, end_time, days.split(" "), activity, professor))
        except IndexError:
            pass

    return classes
