from .Class import Class
from .Extractor import scrape_course


# cpsc110lec1 = Class("cpsc110lec1", "8:00", "10:00", ["Tue", "Thu"])
# cpsc110lec2 = Class("cpsc110lec2", "10:00", "12:00", ["Tue", "Thu"])
# cpsc110lec3 = Class("cpsc110lec3", "12:00", "14:00", ["Tue", "Thu"])
# cpsc110lab1 = Class("cpsc110lab1", "8:00", "11:00", ["Mon"])
# cpsc110lab2 = Class("cpsc110lab2", "11:00", "14:00", ["Wed"])
# cpsc110lab3 = Class("cpsc110lab3", "14:00", "17:00", ["Fri"])
# cpsc110tut1 = Class("cpsc110tut1", "8:00", "11:00", ["Mon"])
# cpsc110tut2 = Class("cpsc110tut2", "11:00", "14:00", ["Wed"])
# cpsc110tut3 = Class("cpsc110tut3", "11:00", "14:00", ["Fri"])
# cpsc121lec1 = Class("cpsc121lec1", "8:00", "10:00", ["Mon", "Wed", "Fri"])
# cpsc121lec2 = Class("cpsc121lec2", "10:00", "12:00", ["Mon", "Wed", "Fri"])
# cpsc121lec3 = Class("cpsc121lec3", "12:00", "14:00", ["Mon", "Wed", "Fri"])
# cpsc121lab1 = Class("cpsc121lab1", "8:00", "10:00", ["Tue", "Thu"])
# cpsc121lab2 = Class("cpsc121lab2", "10:00", "12:00", ["Tue", "Thu"])
# cpsc121lab3 = Class("cpsc121lab3", "12:00", "14:00", ["Tue", "Thu"])
# cpsc121tut1 = Class("cpsc121tut1", "8:00", "10:00", ["Mon"])
# cpsc121tut2 = Class("cpsc121tut2", "10:00", "12:00", ["Mon"])
# cpsc121tut3 = Class("cpsc121tut3", "12:00", "14:00", ["Mon"])
# math100lec1 = Class("math100lec1", "8:00", "10:00", ["Tue", "Thu"])
# math100lec2 = Class("math100lec2", "10:00", "12:00", ["Tue", "Thu"])
# math100lec3 = Class("math100lec3", "12:00", "14:00", ["Tue", "Thu"])
# math100lab1 = Class("math100lab1", "8:00", "10:00", ["Wed"])
# math100lab2 = Class("math100lab2", "10:00", "12:00", ["Wed"])
# math100lab3 = Class("math100lab3", "12:00", "14:00", ["Wed"])
# math100tut1 = Class("math100tut1", "8:00", "12:00", ["Mon"])
# math100tut2 = Class("math100tut2", "12:00", "14:00", ["Wed"])
# math100tut3 = Class("math100tut3", "8:00", "10:00", ["Fri"])
#
# available_classes = {
#     "Lecture": {
#         "CPSC 110": [cpsc110lec1, cpsc110lec2, cpsc110lec3],
#         "CPSC 121": [cpsc121lec1, cpsc121lec2, cpsc121lec3],
#         "Math 100": [math100lec1, math100lec2, math100lec3]
#     },
#     "Labs": {
#         "CPSC 110": [cpsc110lab1, cpsc110lab2, cpsc110lab3],
#         "CPSC 121": [cpsc121lab1, cpsc121lab2, cpsc121lab3],
#         "Math 100": [math100lab1, math100lab2, math100lab3]
#     },
#     "Tutorials": {
#         "CPSC 110": [cpsc110tut1, cpsc110tut2, cpsc110tut3],
#         "CPSC 121": [cpsc121tut1, cpsc121tut2, cpsc121tut3],
#         "Math 100": [math100tut1, math100tut2, math100tut3]
#     }
# }


required_classes = 0
available_classes = {}
curr_state = []


# Total number of classes: Lectures + Any type of small classes (labs, tutorials etc)
def get_required_classes():
    count = 0
    for t in available_classes:
        count += len(list(available_classes[t].values())[0]) + 1

    return count


def is_valid_timing(c, temp_c):
    a = c.get_start_time() >= temp_c.get_end_time()
    b = c.get_end_time() <= temp_c.get_start_time()
    if a or b:
        return True
    return False


def get_next_classes():
    if len(available_classes) > len(curr_state):
        classes = list(available_classes[list(available_classes.keys())[len(curr_state)]].keys())
        return sorted(classes, key=lambda x: x.professor.rating if x.professor is not None else float("-inf"), reverse=True)
    else:
        count = len(available_classes)
        main_count = 0
        for t in available_classes:
            count += len(list(available_classes[t].values())[0])
            if count > len(curr_state):
                try:
                    return list(available_classes[t][curr_state[main_count]].values())[count - len(curr_state) - 1]
                except IndexError:
                    pass
            main_count += 1


def get_next_valid_classes():
    classes = get_next_classes()
    valid_classes = []

    try:
        for c in classes:
            valid_classes.append(c)
            for temp_c in curr_state:
                if len(set(c.days + temp_c.days)) != len(c.days + temp_c.days) and not is_valid_timing(c, temp_c):
                    valid_classes.pop()
                    break
    except TypeError:
        pass

    return valid_classes


def is_valid_combination():
    return len(curr_state) == required_classes


def solve():
    if is_valid_combination():
        return True

    for c in get_next_valid_classes():
        curr_state.append(c)
        if solve():
            return True
        curr_state.pop()
    return False


def merge_with_available_classes(classes):
    temp_name = classes[0].name.split(" ")
    name = temp_name[0] + " " + temp_name[1]
    curr_lec = None

    for c in classes:
        if available_classes.get(name) is None:
            available_classes[name] = {}

        if c.class_type == "Lecture":
            curr_lec = c
            available_classes[name][c] = {}
            if curr_lec.professor:
                print(curr_lec.professor.name)
                print(curr_lec.professor.rating)
        elif available_classes[name][curr_lec].get(c.class_type) is None:
            available_classes[name][curr_lec][c.class_type] = []

        if c.class_type != "Lecture":
            available_classes[name][curr_lec][c.class_type].append(c)


def find_schedule(courses):
    global required_classes, available_classes, curr_state
    required_classes = 0
    available_classes = {}
    curr_state = []

    for course in courses:
        name, section = course.split(" ")
        merge_with_available_classes(scrape_course(name, section, 1))

    required_classes = get_required_classes()

    if solve():
        print([c.name for c in curr_state])
        return [c.name for c in curr_state]
    else:
        return ["No Combination"]
    
    
