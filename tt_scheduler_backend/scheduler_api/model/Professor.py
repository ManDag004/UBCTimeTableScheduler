import ratemyprofessor

school = ratemyprofessor.get_school_by_name("University of British Columbia")

prof_dict = {}


class Professor:
    def __init__(self, name):
        self.name = name

        if prof_dict.get(self.name) is None:
            try:
                self.rating = ratemyprofessor.get_professor_by_school_and_name(school, self.name).rating
            except AttributeError:
                self.rating = 0
            prof_dict[self.name] = self.rating
        else:
            self.rating = prof_dict[self.name]


