# shouldn't need this one, but without it player_character has circular includes
import cnerpg.world_map as world_map
import cnerpg.dialogue_builder as dialogue_builder
import cnerpg.player_character as player_character


def test_character_creator_node_1():
    x = world_map.character_creator_node_1
    assert x.formatting_dict['charisma']() == 0

def test_run_lambda():
    x = world_map.character_creator_node_1
    updated_dict = dialogue_builder.run_lambdas(x.formatting_dict)
    assert updated_dict["charisma"] == 0