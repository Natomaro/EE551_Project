import pytest
import game  #_for_pytest
import mock
import builtins

#All of these tests are based on the correct save file being loaded into the game.
#To ensure they work, make sure the file named "save_file.csv" matches
#the save file named "test_save_file.csv"


player=game.Player()
test_enemy = game.Enemy()

## Buys a health potion by  mocking a '1' input in the shop menu. Gold will decrement by 20 and health potion count will increase by 1.

def test_shop():
    shop_choice_dict={'1':{'name':'Health Potion','price':20},
                '2':{'name':'Mana Potion','price':10},
                '3':{'name':'Magic Sword','price':100},
                '4':{'name':'Scroll of Hyper Beam','price':100}}
    

    with mock.patch.object(builtins, 'input', lambda _:'1'):
        player.player_items[shop_choice_dict['1']['name']]['count'] = 4


        assert(game.Shop()==5)


## Sword Class. The player's strength and sword equipped strength are added and a up to four more is added too. 
def test_sword_power():
    Sword_power = {
    "Wood Sword": 10,
    "Iron Sword": 20,
    "Steel Sword": 30,
    "Magic Sword": 40,
    "Adamantium Sword": 60,
    }

    player.player_strength=35
    player.player_sword_equipped = "Iron Sword"

    ## e.g. Iron sword (20) plus player (35) = 55. Plus up to 4 randomly.  
    test_sword = game.Sword()
    test_sword.power = Sword_power[player.player_sword_equipped]
    assert(55<=test_sword.Attack_power(player.player_strength)<=59)

## Armor Class. Player strength and armor is added for total resist.
def test_armor():
    Armor_armor = {
    "Iron Armor": 5,
    "Steel Armor": 10,
    "Magic Armor": 15,
    "Adamantium Armor": 30,
    }

    player.player_strength=25
    player.player_armor_equipped = "Steel Armor"
    ## e.g. 25 plus 10 = 35
    test_armor = game.Armor()
    test_armor.armor = Armor_armor[player.player_armor_equipped]
    assert(test_armor.Damage_resist(player.player_strength)==35)


## Player class tests.

## Leveling up. When executed, a player's level should increase by one.
def test_leveling_up():
    player.player_level = 2
    assert (player.leveling_up() == 3)

## If the player has an empty slot in his sword bag and gets a new sword, it should be added to the list and empty slot is removed.
## e.g. add an admantium sword to player weapon inventory.

def test_new_sword():
    player.player_weapon_inventory = ['Wood Sword','Iron Sword', 'Steel Sword', 'Empty Slot']
    assert (player.inventory("Adamantium Sword")==['Wood Sword','Iron Sword', 'Steel Sword', 'Adamantium Sword'])

## Enemy class inherits player class health (so this tests both). If a known damage is applied, the instance health should decrement.
## e.g. 10 - 5 = 5.

def test_enemy_health():
    enemy = game.Enemy()
    enemy.enemy_health = 10
    assert(enemy.health(enemy.enemy_health,5)==5)


## function class tests

## normal attack during battle. This mocks a player input of a '1' over and over again.
## The player's strength is set in the save file as 30. The enemy created in the game during a battle is randomly strong
## When running tests, there is a small chance the enemy wins and this test fails (not a bug in the code though). 
## To ensure success, either make the player strength over 50 in save_game.csv or reload the save info from test_game_save.csv into save_game.csv and try again.
def test_normal_attack():
    player.player_strength=100 #ensure I can win the battle for testing.
    with mock.patch.object(builtins, 'input', lambda _:'1'):
        assert((7<=game.Battle() <= 17))

## Use item - directly tests the function named use_item() which is called in Battle() or main menu()
## Forces a '1' input which triggers. health potion. The player's health should increase by 25 HP then.
## e.g. 50 + 25 = 75 HP
def test_item_use():
    with mock.patch.object(builtins, 'input', lambda _:'1'):
        player.player_health = 50
        assert(game.Use_item(player)==75)

## Enemy attacks
## This function will find the damage calculations for an enemy attack on the player and return the player's new health 
## (This return was added primarily for pytesting). E.g. Iron sword (20) + 5 + rand(0,4) = (25,29). 
## Player armor and strength, 10+5= 15. So damage delivered is 10 to 14 
def test_enemy_attacks():
    Sword_power = {
    "Wood Sword": 10,
    "Iron Sword": 20,
    "Steel Sword": 30,
    "Magic Sword": 40,
    "Adamantium Sword": 60,
    }

    Armor_armor = {
    "Iron Armor": 5,
    "Steel Armor": 10,
    "Magic Armor": 15,
    "Adamantium Armor": 30,
    }
    
    player.player_health=70
    test_enemy.enemy_strength=5
    test_en_sword = game.Sword()
    test_en_sword.power = Sword_power["Iron Sword"]
    player.player_strength=10
  

    player_armor = game.Armor()
    player_armor.armor = Armor_armor["Iron Armor"]

    assert(10<=game.enemy_attacks(test_enemy,test_en_sword,player,player_armor) <= 14)   


## Generate the rewards if we win. There are two rewards that are returned in a list - exp and then the loot. 
## This assertion looks at only the exp because exp is predictable based on enemy strength. 
## Right now, exp is simply 5 + enemy str (e.g. 5 + 15 == 20)

def test_gen_rewards():

    test_enemy = game.Enemy()
    test_enemy.enemy_strength = 15
    assert (game.generate_rewards(test_enemy)==20)


## The remaining pieces of the game are very difficult to develop pytest codes for them. Most of them either have
## too much varying outputs, no easy value to return and test, but more than anything else, there is a lot of different
## combinations of human inputs that can't all be coded. The best way to test everything, like spells and the shop, is
## to play the game! :)