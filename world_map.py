import cpu_behaviors    as cb
import dialogue_builder as db
import dice_roller      as dr
import entity_manager   as em
import global_constants as gc
import player_character as pc

player = pc.Player(x=0, y=0)

BLOCKS = [
	gc.pygame.Rect(100,100,10,10),
	gc.pygame.Rect(100,110,10,10),
	gc.pygame.Rect(100,120,10,10),
	gc.pygame.Rect(100,130,10,10),
	gc.pygame.Rect(100,140,10,10),
	gc.pygame.Rect(100,150,10,10),
	gc.pygame.Rect(300,200,20,80),
	gc.pygame.Rect(400,400,200,100),
	gc.pygame.Rect(-10,-10,10,500),
	gc.pygame.Rect(-10,-10,500,10),
	# gc.pygame.Rect(-10,400,500,10),
	gc.pygame.Rect(490,-10,10,500),
	gc.pygame.Rect(-50,200,200,10),
]

character_creator = em.Entity(
	name = "Character Creator",
	x = -60,
	y = -60,
	width = 30,
	height = 30,
	dialogue_dict = {},
	speed = 5,
	behavior = cb.randommovement,
)

guy1 = em.Entity(
	name = "guy1", 
	x = 40, 
	y = 40, 
	width = 30, 
	height = 30, 
	dialogue_dict = {},
	speed = 5,
	behavior = cb.randommovement,
)

ENTITIES = [
	character_creator,
	guy1,
]



##############################
#BELOW THIS POINT IS DIALOGUE#
##############################

character_creator_node_1 = db.Node(text="Your stats are {charisma} charisma, "\
	"{constitution} constitution, {dexterity} dexterity, {intelligence} intelligence, "\
	"{strength} strength, and {wisdom} wisdom. Next, choose your class.", 
	responses={
			"A" : db.Response("Cleric", 2, [lambda: setattr(player, "character_class", "Cleric")]),
			"B" : db.Response("Druid", 2, [lambda: setattr(player, "character_class", "Druid")]),
			"C" : db.Response("Dwarf", 2, [lambda: setattr(player, "character_class", "Dwarf")]),
			"D" : db.Response("Elf", 2, [lambda: setattr(player, "character_class", "Elf")]),
			"E" : db.Response("Fighter", 2, [lambda: setattr(player, "character_class", "Fighter")]),
			"F" : db.Response("Halfling", 2, [lambda: setattr(player, "character_class", "Halfling")]),
			"G" : db.Response("Magic-User", 2, [lambda: setattr(player, "character_class", "Magic-User")]),
			"H" : db.Response("Paladin", 2, [lambda: setattr(player, "character_class", "Paladin")]),
			"I" : db.Response("Ranger", 2, [lambda: setattr(player, "character_class", "Ranger")]),
			"J" : db.Response("Warlock", 2, [lambda: setattr(player, "character_class", "Warlock")]),
	}
)

character_creator_node_2 = db.Node(text="You selected {character_class}. What is your name?",
	responses={
		"A" : db.Response("Yaay", 3, []),
	},
	is_text_entry_node=True,
	class_owning_attr=player,
	attr_to_receive_user_text="name"
)

character_creator_node_3 = db.Node(text="Your name is {name}.",
	responses={
		"A" : db.Response("Thank you. Goodbye.", 3, is_end_of_dialogue=True),
	}

)

character_creator.dialogue_dict = {
	0 : db.Node("Welcome to the character creator. First, select how you will generate your stats.", {
		"A" : db.Response("Extreme.", 1, [
			lambda: setattr(player, "charisma", dr.roll_x_d_n_and_keep_highest_k(3,20,1)),
			lambda: setattr(player, "constitution", dr.roll_x_d_n_and_keep_highest_k(3,20,1)),
			lambda: setattr(player, "dexterity", dr.roll_x_d_n_and_keep_highest_k(3,20,1)),
			lambda: setattr(player, "intelligence", dr.roll_x_d_n_and_keep_highest_k(3,20,1)),
			lambda: setattr(player, "strength", dr.roll_x_d_n_and_keep_highest_k(3,20,1)),
			lambda: setattr(player, "wisdom", dr.roll_x_d_n_and_keep_highest_k(3,20,1))
			]),
		"B" : db.Response("Standard.", 1, [
			lambda: setattr(player, "charisma", dr.roll_x_d_n_and_keep_highest_k(3,10,2)),
			lambda: setattr(player, "constitution", dr.roll_x_d_n_and_keep_highest_k(3,10,2)),
			lambda: setattr(player, "dexterity", dr.roll_x_d_n_and_keep_highest_k(3,10,2)),
			lambda: setattr(player, "intelligence", dr.roll_x_d_n_and_keep_highest_k(3,10,2)),
			lambda: setattr(player, "strength", dr.roll_x_d_n_and_keep_highest_k(3,10,2)),
			lambda: setattr(player, "wisdom", dr.roll_x_d_n_and_keep_highest_k(3,10,2))
			]),
		"C" : db.Response("Classic.", 1, [
			lambda: setattr(player, "charisma", dr.roll_x_d_n(3,6)),
			lambda: setattr(player, "constitution", dr.roll_x_d_n(3,6)),
			lambda: setattr(player, "dexterity", dr.roll_x_d_n(3,6)),
			lambda: setattr(player, "intelligence", dr.roll_x_d_n(3,6)),
			lambda: setattr(player, "strength", dr.roll_x_d_n(3,6)),
			lambda: setattr(player, "wisdom", dr.roll_x_d_n(3,6))
			]),
	}),
	1 : character_creator_node_1,
	2 : character_creator_node_2,
	3 : character_creator_node_3,
}

guy1.dialogue_dict = {
	0 : db.Node("Yes or no?", { 
			"A" : db.Response("Yes.", 0, is_end_of_dialogue=True),
			"B" : db.Response("No.", 0, [lambda: guy1.a_star_pathfind(-100,-100, BLOCKS)], is_end_of_dialogue=True),
			"C" : db.Response("N/A.", 0, is_end_of_dialogue=True, display_bool=False),
		}),
}