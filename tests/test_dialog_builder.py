# shouldn't need this one, but without it player_character has circular includes
import cnerpg.world_map as world_map
import cnerpg.dialogue_builder as dialog_builder
import cnerpg.player_character as player_character


def test_character_creator_node_1():
    x = world_map.character_creator_node_1
    assert x.formatting_dict['charisma']() == 0

def run_lambda():
    y = world_map.character_creator_node_1.formatting_dict
    for key, value in y.items():
        value = value()
    return y

 def test_run_lambda():
    y = run_lambda()
    assert y["charisma"] == 0
