class View(object):
   """
   View represents the HTML files, which interact with the end user. It represents the model’s data to user.
   """

   def __init__(self):
      self.start_view()

   def show_all_people(self, list):
      print('In our db we have %i users. Here they are:' % len(list))
      for item in list:
         print(item.name())

   def start_view(self):
      print('MVC -  example')
      print('Do you want to see everyone in my db?[y/n]')

   def end_view(self):
      print('Goodbye!')
