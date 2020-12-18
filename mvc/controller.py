from mvc.model import Person
from mvc.view import View


class Controller:
    """
   It acts as an intermediary between view and model. It listens to the events triggered by view and queries model for the same.
   """

    def __init__(self):
        pass

    def start(self):
        view = View()
        user_input = input()
        if user_input == 'y':
            all_people = Person.get_all()
            return view.show_all_people(all_people)
        else:
            return view.end_view()


if __name__ == "__main__":
    # running controller function
    Controller().start()
