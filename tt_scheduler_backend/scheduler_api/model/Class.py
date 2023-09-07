from .Professor import Professor


def get_time(time):
    hrs, mins = time.split(":")
    hrs = int(hrs)
    mins = 0 if mins == "00" else 0.5
    return hrs + mins


class Class:
    def __init__(self, name, start_time, end_time, days, class_type="Lecture", professor=None):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.days = days
        self.class_type = class_type
        self.professor = professor

    def get_start_time(self):
        return get_time(self.start_time)

    def get_end_time(self):
        return get_time(self.end_time)
