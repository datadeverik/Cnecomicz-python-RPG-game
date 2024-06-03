class Response:
    def __init__(self, display_bool, response, next_dialogue, trigger_call=None):
        self.display_bool = display_bool
        self.response = response
        self.next_dialogue = next_dialogue
        self.trigger_call = trigger_call or (lambda entity: None)

    def trigger(self, entity):
        self.trigger_call(entity)


class Dialogue:
    def __init__(self, text, responses=None):
        self.text = text
        self.responses = responses or {}


class Entity:
    def __init__(self, name, x, y, width, height, dialogues):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dialogues = dialogues
        self.current_dialogue_id = 0

    def get_current_dialogue(self):
        return self.dialogues.get(self.current_dialogue_id)

    def choose_response(self, response_key):
        current_dialogue = self.get_current_dialogue()
        if current_dialogue:
            response = current_dialogue.responses.get(response_key)
            if response and response.display_bool:
                response.trigger(self)
                self.current_dialogue_id = response.next_dialogue

    def change_attribute(self, attribute, value):
        setattr(self, attribute, value)

def trigger_change_x(entity):
    entity.change_attribute('x', 100) # or whatever

def trigger_change_y(entity):
    entity.change_attribute('y', 200) # random values

    
dialogue_0 = Dialogue(
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur purus nulla, finibus et interdum sed, porta quis massa. Suspendisse quis convallis turpis. Maecenas pellentesque nisi metus, in eleifend nunc accumsan eget. Fusce a tortor quam. Integer sit amet malesuada leo. Sed vel laoreet ipsum. Curabitur pretium nisi nec neque imperdiet, in fermentum tellus sagittis.",
    {
        "A": Response(True, "Yes.", 1, trigger_change_x),
        "B": Response(True, "No.", 2, trigger_change_y),
    }
)

dialogue_1 = Dialogue("You said yes.")
dialogue_2 = Dialogue("You said no.")

dialogues = {
    0: dialogue_0,
    1: dialogue_1,
    2: dialogue_2,
}

print(dialogues)

guy1 = Entity(name="guy1", x=40, y=40, width=30, height=30, dialogues=dialogues)

guy1 = Entity(name="guy1", x=40, y=40, width=30, height=30, dialogues=dialogues)