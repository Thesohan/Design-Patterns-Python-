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
    IMAGE = "image"
    INPUT = "input"
    FLASH = "flash"
    BUTTON_FACTORY_MAP = {
        IMAGE:Image,
        INPUT:Input,
        FLASH:Flash,
    }

    def create_button(self,button_type):
        return self.BUTTON_FACTORY_MAP.get(button_type)()


if __name__=='__main__':
    buttons = ["image","flash","input"]
    obj = ButtonFactory()
    for button in buttons:
        butt = obj.create_button(button)
        print(butt.get_html())

