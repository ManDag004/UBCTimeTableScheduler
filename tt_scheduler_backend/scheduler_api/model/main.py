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

min_time = 8
max_time = 20


def get_required_classes():
    """
    Total number of classes: Lectures + Any type of small classes (labs, tutorials etc)
    """
    count = 0
    for t in available_classes:
        count += len(list(available_classes[t].values())[0]) + 1

    return count


def within_limits(c):
    """
    Checks if the class is within the time limits.
    """
    return c.get_start_time() >= min_time and c.get_end_time() <= max_time


def does_not_overlap(c, temp_c):
    """
    Checks if the timings of the new class and the current class overlap.
    """

    starts_later = c.get_start_time() >= temp_c.get_end_time()
    ends_before = c.get_end_time() <= temp_c.get_start_time()

    if (starts_later or ends_before):
        return True
    return False


def get_next_classes():
    """
    Gets the next classes by checking if the number of classes in the current state
    """
    if len(available_classes) > len(curr_state):
        # get the next lecture classes
        classes = list(available_classes[list(available_classes.keys())[len(curr_state)]].keys())
        # sort the lecture sections by the professor rating
        return sorted(classes, key=lambda x: x.professor.rating if x.professor is not None else float("-inf"), reverse=True)
    else:
        # get the next class based on how many classes have been added
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
    """
    Gets the next valid classes by checking if the days and timings of the new classes do not
    overlap with those of classes in the current state.
    """
    classes = get_next_classes()
    valid_classes = []

    try:
        for c in classes:
            if within_limits(c):
                valid_classes.append(c)
                for temp_c in curr_state:
                    # if the days and timings of the new class and the current class overlap, remove the new class from the list of valid classes
                    if len(set(c.days + temp_c.days)) != len(c.days + temp_c.days) and not does_not_overlap(c, temp_c):
                        valid_classes.pop()
                        break
    except TypeError:
        pass

    return valid_classes


def is_valid_combination():
    """
    Checks if the current state is valid by checking if the number of classes in the current 
    state is equal to the required number of classes.
    """
    return len(curr_state) == required_classes


def solve():
    """
    Solves the problem recursively by adding the next valid class to the current state and 
    checking if the current state is valid.
    """
    if is_valid_combination():
        return True

    for c in get_next_valid_classes():
        curr_state.append(c)
        if solve():
            return True
        curr_state.pop()
    return False


def merge_with_available_classes(classes):
    """
    merges the classes with all of the already existing classes. 
    """
    temp_name = classes[0].name.split(" ") # getting the course name from the first class
    name = temp_name[0] + " " + temp_name[1] # removing the section number from the course name
    curr_lec = None

    for c in classes:

        # if the course name is not in the dictionary, create its corresponding dictionary
        if available_classes.get(name) is None:
            available_classes[name] = {}

        # if the class is a lecture, set the current lecture to the class and create a dictionary for it as the other classes will come under it 
        if c.class_type == "Lecture":
            curr_lec = c
            available_classes[name][c] = {}
            if curr_lec.professor:
                print(curr_lec.professor.name)
                print(curr_lec.professor.rating)
        elif available_classes[name][curr_lec].get(c.class_type) is None:
            available_classes[name][curr_lec][c.class_type] = []

        # add the class to the dictionary of its type in its lecture class
        if c.class_type != "Lecture":
            available_classes[name][curr_lec][c.class_type].append(c)


def find_schedule(course_names, term, min_start_time, max_end_time):
    from .Class import get_time
    global required_classes, available_classes, curr_state, min_time, max_time

    required_classes = 0
    available_classes = {}
    curr_state = []
    min_time = get_time(min_start_time) if min_start_time else min_time
    max_time = get_time(max_end_time) if max_end_time else max_time

    for course_name in course_names:
        name, section = course_name.split(" ")
        merge_with_available_classes(scrape_course(name, section, term))
    
    required_classes = get_required_classes()

    if solve():
        print([c.name for c in curr_state])
        return [{"title": c.name, "start_time": c.start_time, "end_time": c.end_time, "days": c.days} for c in curr_state]
    else:
        return ["No Combination"]
    
    
