"""
Objects are created without exposing the logic to client and referring to the newly created object using a common interface.
"""

class Button(object):
    html = ""

    def get_html(self):
        return self.html

class Image(Button):
    html = "<img></img>"

class Input(Button):
    html = "<input></input>"

class Flash(Button):
    html = "<flash></flash>"

class ButtonFactory:
    def create_button(self,button_type):
        button_class = button_type.capitalize()
        return globals()[button_class]

if __name__=='__main__':
    buttons = ["image","flash","input"]
    obj = ButtonFactory()
    for button in buttons:
        print(obj.create_button(button))

