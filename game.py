import random
import time
import csv
import sys
from numpy.random import choice

## Welcome to my basic adventuring Python text game! The current objectives/functionality of this game are to kill monsters, level up, 
## and collect gold! All data can be saved with a proper exit and the required .csv files being in the same directory of this script.

## The main functionality of this game revolves around the Player class. This class is created once upon starting the game and reads all 
## of the save data to initilize its attributes. These attributes change during the flow of the game and then are resaved into a csv upon exiting.

## As a result, not all functions need to properly return a value. Some return values were added for testing purposes.
## To ensure a proper test done using pytest, use the script game_for_pytest.py and the test_save_file.csv
## These very slightly altered files lead to consistent results which can be tested using pytest (some features require a lot of human input or are
## sometimes up to chance which would be bad otherwise for testing. These random parts are left out of the script for a pytest script to run.)

## The imported packages are obviously required. The only ones not inherent to Python are csv and numpy.


## Load your save file. If no Existing file exists, use the default new game file.
## The next save will create the save file for the next time the game is run if you save properly.
## Saving/Reading is done by writing/reading a .csv file.
try:
    allinfo = open('save_file.csv','r').read().rsplit(',')
except:
    allinfo = open('new_game_stats.csv','r').read().rsplit(',')


## Define all the classes: Sword, Armor, Special Ability, Player, Enemy, Store

## Define sword for use by player and enemy. 
class Sword():
    ## Initilize the sword's 'power' stat upon creation
    def __init__(self, power=0):
        self.power = power
    ## Based on the sword user's strength and the current sword,
    ## find total power. Add randomness for RNG effect in battle
    ## Return total_power.
    def Attack_power(self,player_strength):
        total_power = player_strength + self.power + random.randint(0,4)
        print("Attacker's Strength:", total_power)
        return total_power

## Similar to sword class. Armor stats for use by player and enemies.
class Armor():
    ## Initilize the sword's power upon creation
    def __init__(self, armor=0):
        self.armor = armor
    ## Based on the player's strength and the current sword, 
    ## find total power. Add randomness for RNG effect in battle. Return total_resist
    def Damage_resist(self,player_strength):
        total_resist = player_strength + self.armor
        print("Defender Resists:", total_resist)
        return total_resist


## The most important piece of code for this project. 
## Define the player and his many stats. To cut down on the number of functions used and
## variables returned, all the many attributes associated with the play are defined in this class.
## Many other functions directly manipulate these values for this game.
class Player():
    ## Initilize the player's attributes. All the attributes are initialized by reading
    ## The list from the .csv save file. Additional attributes can be added here.
    ## A brief run down of the less intuitive attributes:
        ## Weapon_inventory & armor inventory - a list of weapons and armor respectively in your bag. Empty slots are marked by "Empty slot" 
        ## Spell_list - All available spells. This is a set because as loot you can get more spells. Unlike swords/armor, you shouldn't be able to have a double up on spells in this list. Sets keep only unique values.
        ## Player items - A labelled dictionary for health and mana potions. The count is the only value the player needs to hold.
        ## Every thing else is just an int, str, or list that holds basic info on your character.
   
        ## One very particular design choice: many attributes can easily be increased. If I add more entries in the save file,
        ## and change the indexes, all the inventories and the selected spells can be expanded in a future development.
    def __init__(self, player_strength=int(allinfo[0]), player_health=int(allinfo[1]),player_mana=int(allinfo[2]),gold_count=int(allinfo[3]),
        player_weapon_inventory=allinfo[4:8],player_sword_equipped=allinfo[8],player_armor_inventory=allinfo[9:11],player_armor_equipped=allinfo[11],
        player_spell_list=set(allinfo[12:15]),player_selected_spells=allinfo[15:17],player_items={"Health Potion": {"count": int(allinfo[17])},
        "Mana Potion": {"count": int(allinfo[18])}},player_exp=int(allinfo[19]),player_level=int(allinfo[20]),until_next_level=int(allinfo[21])):
        self.player_strength = player_strength
        self.player_health = player_health
        self.player_mana = player_mana
        self.gold_count = gold_count
        self.player_weapon_inventory = player_weapon_inventory
        self.player_sword_equipped = player_sword_equipped
        self.player_armor_inventory = player_armor_inventory
        self.player_armor_equipped = player_armor_equipped
        self.player_spell_list = player_spell_list
        self.player_selected_spells = player_selected_spells
        self.player_items = player_items
        self.player_exp = player_exp
        self.player_level = player_level
        self.until_next_level = until_next_level

    ## This method is called when the player's exp reaches the until_next_level mark.
    ## Levels up the character by one, increases their strength, and resets the player's 
    ## exp with a new until_next_level threshold.  
    def leveling_up(self):
        self.player_level+=1
        level = self.player_level
        print("You are now level", self.player_level)

        self.player_exp = 0

        self.player_strength=15+self.player_level*4
        print("New player strength =",self.player_strength)

        self.until_next_level += 20+self.player_level*2
        print("EXP until next level is now =", self.until_next_level)
        return level

    ## Decrement the player's health when they get hurt and print it.
    def health(self,current_health, damage_dealt):
        health = current_health
        health -= damage_dealt
        print("Current Health: "+str(health)+"\n_________________________")
        return health

    ## This method is called to define the loot the player has and the spells he can equip.
    ## The defeated enemy generates a reward and this method parses it and adds it to the player's bag accordingly.

    def inventory(self,loot_string):
        ## All loot comes in as a string that needs to be parsed for a key word.

        ## Add gold to the gold count
        if "gold pieces" in loot_string:
            loot = int(loot_string.rsplit()[0])
            self.gold_count += loot
        ## Add spells to the spell list
        elif "Scroll" in loot_string:
            #Spells are a set instead of list so all entries are unique (e.g. if you get two Scrolls of Fireball, Fireball should only appear in the spell list once)
            loot = loot_string.split('of ')[-1]
            #print(loot)
            if len(self.player_spell_list)<4:
                self.player_spell_list.remove("Empty Slot")
                self.player_spell_list.add(loot)
                #return self.player_spell_list
            else:
                print("Spell Slots full!")

        ## Add swords to the weapon inventory if there is an empty slot.
        elif "Sword" in loot_string:
            loot = loot_string
            if "Empty Slot" in self.player_weapon_inventory:
                self.player_weapon_inventory.remove("Empty Slot")
                self.player_weapon_inventory.append(loot) 
                return self.player_weapon_inventory
            else:
                print("Sword Inventory Full! Can't add more!")

        ## Add armor to the armor inventory if there is an empty slot.
        elif "Armor" in loot_string:
            if "Empty Slot" in self.player_armor_inventory:
                self.player_armor_inventory.remove("Empty Slot")
                self.player_armor_inventory.append(loot)
                return self.player_armor_inventory 
            else:
                print("Armor Inventory Full! Can't add more!")
 
        ## Increase potion count depending on the potion earned. 
        ## This one is called by Shop() when the player buys more potions.
        elif "Potion" in loot_string:
            self.player_items[loot_string]['count']+=1
            return self.player_items


## Make the Enemy class by inheriting the PLayer class. It has a lot less attributes
## but still needs a method to decrement its health in battle. 
class Enemy(Player):
    ## Initilaize an enemy with a random strength and health
    def __init__(self):
        ## Make the enemy's health and strength random. Make sure you run if it happens to be too strong!
        self.enemy_strength = random.randint(2,12)
        self.enemy_health = random.randint(20,40)
        self.affliction = "None"
    ## Same as player health() - decrement the enemy's health accordingly
    def health(self,current_health, damage_dealt):
        return Player.health(self,current_health, damage_dealt)


## global var whitelist. This is used for removing unwanted characters for screen printouts (i.e. for removing '[' ']' when printing a value in a string)
whitelist = set(',abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')


## Dictionary of Sword types to their respective power
## This is used because Sword_equipped is stored as a string. This dict maps that to a numerical strength.
Sword_power = {
    "Empty Slot": 0,
    "Wood Sword": 10,
    "Iron Sword": 20,
    "Steel Sword": 30,
    "Magic Sword": 40,
    "Adamantium Sword": 60,
}


## Dictionary of Armor types to their respective armor rating
## This is used because Armor_equipped is stored as a string. This dict maps that to a numerical resist factor.
Armor_armor = {
    "Empty Slot": 0,
    "Iron Armor": 5,
    "Steel Armor": 10,
    "Magic Armor": 15,
    "Adamantium Armor": 30,
}

## This dictionary holds all the types of spells in the game. There are only 3 for demo purposes but the game is designed to easily allow more.
## Fireball shoots a fire blast and potentially burns, Ice beam hurts the enemy and can freeze. Heal heals the player.
## 'damage' - The damage amount. 'effect'- what a spell can do.
## 'success rate' - chance the effect takes place. 'mana cost' - mana cost amount.

## Another design note: More spells can be easily added by just filling out this list and making a few other minimal changes (adding the scroll for that spell in the loot part of generate_rewards()
Spells_dictionary = {
    'Fireball': {'damage': random.randint(10,20), 'effect': 'Burn', 'success_rate': .3, 'mana_cost':15},
    'Heal': {'damage': random.randint(8,12), 'effect': 'Gain HP', 'success_rate': 1, 'mana_cost':10},
    'Ice Beam': {'damage': random.randint(20,35), 'effect': 'Freeze', 'success_rate': .2, 'mana_cost':20},
    'Hyper Beam': {'damage': 100, 'effect':'None', 'success_rate': 0, 'mana_cost':60}
}

## Similar to spells but for the two main items - Health and mana potions.
Items_Dictionary = {
    'Health Potion': {'effect': 'Heals you for a lot of HP', 'amount': 25},
    'Mana Potion': {'effect': 'Heals you for a lot of MP', 'amount': 25},
}

## Make an instance of the player and their equipment. These instances are the player
## until the game shuts off. 
player = Player()
player_sword = Sword()
player_armor = Armor()




def Battle():
    ## In this function, the following needs to occur
    ## 1) Generate and display an enemy based on the enemy class
    ## 2) Give the player options for how to fight
    ## 3) Player and enemy have to do their actions. Go back to 2 until the fight is over.
    
    ## Make a random enemy. Give him a sword and armor at random.
    current_enemy = Enemy()
    enemy_sword = Sword()
    enemy_sword.power = Sword_power[random.choice(['Wood Sword', 'Iron Sword','Steel Sword'])]
    enemy_armor = Armor()
    enemy_armor.armor = Armor_armor[random.choice(['Iron Armor', 'Steel Armor'])]
    player_armor.armor = Armor_armor[player.player_armor_equipped]
    player_sword.power = Sword_power[player.player_sword_equipped]


    while True:
        print("\nYour Current Level:", player.player_level)
        print("Your Current Health:", player.player_health)
        print("Your Current Mana:", player.player_mana)

        ## Take the player's choice and act accordingly. Anything besides '1', '2', or '3' will run from the fight.
     
        player_choice = input ("\nDo you want to 1) Use your sword. 2) Use a spell. 3) Use an item. 4) Run.")
        if player_choice in ['1','2','3','4']:
            
            ## Basic sword attack protocol.
            if player_choice == '1':
                print("\nPlayer Attacks the enemy!")

                ## Based on the current sword equipped, find the sword's power for the full strength calculation.

                ## Find the damage done. The player attacks with his full strength = player's strength + sword's power.
                ## The enemy resists with his strength + armor factor.
                Damage_to_Enemy_calculation = player_sword.Attack_power(player.player_strength) - enemy_armor.Damage_resist(current_enemy.enemy_strength)
                if Damage_to_Enemy_calculation < 0: Damage_to_Enemy_calculation = 0
                print("Damage dealt: ",Damage_to_Enemy_calculation)
                current_enemy.enemy_health = current_enemy.health(current_enemy.enemy_health,Damage_to_Enemy_calculation)
                
                ## Check if the enemy died. If so, generate rewards and move on.
                if current_enemy.enemy_health <= 0: 
                    exp = generate_rewards(current_enemy)
                    
                    break

                ## The enemy attacks after you do if it did not die.
                enemy_attacks(current_enemy,enemy_sword,player,player_armor)


            ## Battle choice 2, use a spell.
            #1) print your spells and their effects
            #2) Take the user input and apply the damage and effect if successful chance
            elif player_choice == '2':
                counter = 0

                ## print out the current spells loaded.
                for i in player.player_selected_spells:
                    counter += 1
                    spell_text = Spells_dictionary[i]['effect']
                    print(str(counter) + ") " + i + ' -> Effect: ' + Spells_dictionary[i]['effect']+ '; Success rate: ' + str(Spells_dictionary[i]['success_rate']))

                ## Pass the spell choice to the spell_attack function. Requires all player and enemy instances as well. 
                spell_choice = input ("\nEnter the number of the spell you want to cast (<enter> to cancel): ")
                spell_attack(spell_choice,current_enemy,enemy_armor,player,player_armor)
                enemy_attacks(current_enemy,enemy_sword,player,player_armor)

                
            ## Battle choice 3, use an item. Trigger the use and item function and then make the enemy attack when it returns
            elif player_choice == '3':
                Use_item(player)
                enemy_attacks(current_enemy,enemy_sword,player,player_armor)
            else:
                break
    return exp

        
## Use item function. Prints out the player's potion counts and allows them to select one. The proper effect is applied.

def Use_item(player): 
    counter = 0

    ## Print the potion counts. 
    for i in player.player_items:
        counter += 1
        print(str(counter) + ") " + i + ": " + str(player.player_items[i]["count"]))
    item_choice = input ("\nEnter the number of the item you want to use: ")
    print(player.player_items["Health Potion"]["count"])
    
    ## Take the choice and execute the expected result. Choice 1 and 2 are very similar but for Health potion and Mana potion respectively.
    if item_choice == "1" and ((player.player_items["Health Potion"]["count"])>=1):
        print("Used a Health Potion! You gained 25 HP!")
        player.player_health += 25

        ## The max health in this game is 100 HP.
        if player.player_health >= 100: player.player_health = 100
        player.player_items["Health Potion"]["count"] -= 1
        if player.player_items["Health Potion"]["count"] < 0: player.player_items["Health Potion"]["count"] = 0
        health = player.player_health
        print(health)
        return health


    elif item_choice == "2" and player.player_items["Mana Potion"]["count"]>0:
        print("Used a Mana Potion! You gained 25 MP!")
        player.player_mana += 25
        print(player.player_mana)
        player.player_items["Mana Potion"]["count"] -= 1
        if player.player_items["Mana Potion"]["count"] < 0: player.player_items["Mana Potion"]["count"] = 0
    else:
        print("Invalid Choice")
    return

## Function that makes the enemy do a basic attack on the player.

def enemy_attacks(current_enemy,enemy_sword,player,player_armor):

    ## Check the affliction due to spells. If frozen, the enemy should lose his turn. If burned, he should get hurt at the very beginning of his turn.
    if current_enemy.affliction != "Freeze":
        print("\r\nEnemy attacks you!")
        if current_enemy.affliction == "Burn":
            current_enemy.enemy_health -= 6
            print("Enemy burned for 4 HP!")
        
        ## Similarly to how the player attacks, the enemy will attack the player. Damage calculations are based on strenghs, enemy sword, and player armor

        Damage_to_player_calculation = enemy_sword.Attack_power(current_enemy.enemy_strength) - player_armor.Damage_resist(player.player_strength)
        if Damage_to_player_calculation < 0: Damage_to_player_calculation = 0
        print("Damage dealt: "+str(Damage_to_player_calculation))
        


        player.player_health = player.health(player.player_health,Damage_to_player_calculation)
        damage_confirm = Damage_to_player_calculation
        
        ## If the player dies, then the game should end. No save! 
        if player.player_health <= 0:
            print("\nYou died! Rerun the game to start over from your last save!")
            sys.exit()

    else:
        print("Enemy is frozen still!")
        pass
    ## return the player's health. This is primarily used for pytest checks. The actual player health lies in the player.Player() instance
    return damage_confirm


## Generate the rewards function. Should pick a random prize and award exp.

def generate_rewards(current_enemy):
    
    ## The enemy died! End the battle and claim your rewards!
    print("\nYou won the battle!\n_________________________")
    
    ## EXP is based on the enemy's strength. Add the exp and level up if you hit the required amount of exp for the next level.
    exp = current_enemy.enemy_strength + 5
    player.player_exp += exp
    if player.player_exp >= player.until_next_level:
        level = player.leveling_up()

    ## Choose a battle reward with a probability distribution. 
    loot = str(choice([str(random.randint(5,15))+" gold pieces", 'Scroll of Fireball', 'Scroll of Ice Beam', 'Iron Sword', 'Steel Sword', 'Adamantium Sword', 'Iron Armor', 'Steel Armor', 'Adamantium Armor'],1,[.69,.05,.05,.05,.05,.01,.05,.04,.01]))
    ## Do some minimal filtering to clean up the string
    loot_string = ''.join(filter(whitelist.__contains__, loot))
    
    print("\nYour rewards: \nExp: " + str(exp) + "\nLoot: " + loot_string+"\n_________________________\n_________________________")
    player.inventory(loot_string)

    ## return the loot string. Mostly for pytest testing.
    return exp

## The function that controls the main menu of the game. All it does is present your current info and then call the proper function based on your choice. 

def Main_menu():
    while True:
        print("\nYour Current Level:", player.player_level)
        print("Your Current Health:", player.player_health)
        print("Your Current Mana: ", player.player_mana)
        print("Your Current Gold: ", player.gold_count)
        player_choice = input ("\nWhat do you want to do?\n 1) Look for a fight. 2) Change loadout. 3) Go to the shop. 4) Use an item. 5) Save and quit."+"\n_________________________________________________________________________________________________")
        if player_choice in ['1','2','3','4','5']:
           
            if player_choice == '1':
                Battle()
            elif player_choice == '2':
                Change_loadout()
            elif player_choice == '3':
                Shop()
            elif player_choice == '4':
                Use_item(player)
            elif player_choice == '5':
                Save_game()
            else:
                print("Invalid choice")
                

## The spell attack function. Needs the current player and enemy instances for damage calculations.

def spell_attack(spell_choice,current_enemy,enemy_armor,player,player_armor):

    ## Builds a small dictionary based on your spell loadout and the numbering in the prompt.
    print("\nThese are your currently equipped spells:")

    spell_choice_dict={'1':player.player_selected_spells[0],
            '2': player.player_selected_spells[1],}
    
    current_spell = Spells_dictionary[spell_choice_dict[spell_choice]]

    ## Takes the player choice. If it is Heal, the player needs to gain health. If it is an attack spell, the damage should
    ## be calculated and the effect applied if the probability check is passed. The mana should be decremented accordingly.

    if spell_choice in ['1','2'] and (player.player_mana - Spells_dictionary[spell_choice_dict[spell_choice]]['mana_cost'] >= 0):
        ## Takes the number input and converts it to the correct spell string --< needed to index the spell dictionary 
        
        ## declare a local variable for the valid spell chosen for organization
        if spell_choice_dict[spell_choice] == 'Heal':
            heal_amount = Spells_dictionary['Heal']['damage']
            player.player_health += heal_amount
            ## The max health in this game is 100 HP.
            if player.player_health >= 100: player.player_health = 100
            print("Player healed for ",str(heal_amount) +"HP")
            return heal_amount
        else:
            print("Spell Power: ",Spells_dictionary[spell_choice_dict[spell_choice]]['damage'])
            
            ## Similar to basic attack. The spell damage - the total enemy resist equals the damage done.
            Damage_to_Enemy_calculation = current_spell['damage'] - enemy_armor.Damage_resist(current_enemy.enemy_strength)
            
            ##Make sure there is no negative damage
            if Damage_to_Enemy_calculation < 0: Damage_to_Enemy_calculation = 0
            print("Damage dealt: ",Damage_to_Enemy_calculation)
            if current_spell['success_rate'] >= 0:#random.random():
                print("Enemy is afflicted with " + current_spell['effect'])
                current_enemy.affliction = current_spell['effect']
            current_enemy.enemy_health = current_enemy.health(current_enemy.enemy_health,Damage_to_Enemy_calculation)

        ## decrement the player's mana.
        player.player_mana -= current_spell['mana_cost']

        if player.player_mana <= 0: player.player_mana = 0


    else:
        print("Invalid Entry or Not enough mana!")
    
#Check if the status is afflicted. Take success rate and compare it to a random value generated.
    
    
    ## check if the enemy died. If so, generate rewards and move on.

    if current_enemy.enemy_health <= 0: 
        loot = generate_rewards(current_enemy)
        

    ## Return the damage done, mostly for pytest testing
    return current_spell['damage']


## This function is to manipulate the player's current loadout. You can change swords, armors, and spells.

def Change_loadout():

    while True:
        ## Take the player's choice and behave accordingly. 
        player_choice = input ("\nDo you want to change 1) Weapon. 2) Armor. 3) Spells. 4) Cancel. ")
        if player_choice in ['1','2','3','4']:
            if player_choice == '1':

                print("Current Weapon: "+player.player_sword_equipped)
                ## some filtering for presentation.
                print(''.join(filter(whitelist.__contains__, str(player.player_weapon_inventory))))
                ## Type in the correct name of the desired equipment to be put on.
                selected_weapon = input ("Correctly type in the item you want to equip: ")
                
                ## If the player has the equipment in his inventory, equip it.
                if selected_weapon in player.player_weapon_inventory:
                    player.player_sword_equipped = selected_weapon

                    print('Weapon changed to:'+selected_weapon)
                else:
                    print("Invalid choice")

            ## Same process as swords (choice 1 above this block) but for armor.    
            elif player_choice == '2':
                print("Current Armor: "+player.player_armor_equipped)
                print(''.join(filter(whitelist.__contains__, str(player.player_armor_inventory))))
                selected_armor = input ("Correctly type in the item you want to equip(<enter> to cancel): ")
                if selected_armor in player.player_armor_inventory:
                    player.player_armor_equipped = selected_armor
                    print('Armor changed to:'+ selected_armor)
                else:
                    print("Invalid choice")   

            ## Similar to sword and armor choices but slightly different because you can have two spells selected at once. You need to select the new choice
            ## and then the existing one in your current loadout to replace.
            elif player_choice == '3':
                print("These are your available spells: ")
                print(''.join(filter(whitelist.__contains__, str(player.player_spell_list))))

                print("\nThese are your currently equipped spells:")
                print(''.join(filter(whitelist.__contains__, str(player.player_selected_spells))))

                ## 
                selected_spell = input ("\nSelect the spell you want to add [2 spells max.](<enter> to cancel): ")
                if selected_spell in player.player_spell_list:
                    spell_to_replace = input ("Correctly type in the spell you want to replace(<enter> to cancel): ")

                    player.player_selected_spells.remove(spell_to_replace)
                    player.player_selected_spells.append(selected_spell)

                    print('Replaced: '+ spell_to_replace + " with " + selected_spell)
                else:
                    print("Invalid choice")
            else:
                break
    return

## Shop function. Print out the options in the store. Options right now include potions and a rare sword.
## If the player selects an item and can afford it, he should get that item added to his inventory, his gold properly decremented.
## If he wants to sell, then his inventory should be printed and the option to be sold selected.

def Shop():

    while True:
        print("\nWelcome to ye Olde Shoppe! Check out my wares!\n")

        shop_choice_dict={'1':{'name':'Health Potion','price':20},
                        '2':{'name':'Mana Potion','price':10},
                        '3':{'name':'Magic Sword','price':100},
                        '4':{'name':'Scroll of Ice Beam','price':80}}

        ## Take a choice. If it is 1 2 or 3, then perform the expected transaction.
        player_choice = input ("Enter the number of what you want to buy.\n\n1) Health Potion: 20 GP. \n2) Mana Potion: 30 GP. \n3) Magic Sword: 100 GP. \n4) Scroll of Ice Beam: 80 GP\n\n5) Sell item. \n6) Cancel.\n\n")
        if player_choice in ['1','2','3','4']:
            
            if shop_choice_dict[player_choice]['price']<=player.gold_count:    
                if player_choice in ['1','2']: 
                    
                    player.player_items[shop_choice_dict[player_choice]['name']]['count']+=1
                    
                    for i in player.player_items:
                        print(i + ': ' +str(player.player_items[i]['count']))
                    player.gold_count-=shop_choice_dict[player_choice]['price']
                    return player.player_items[shop_choice_dict[player_choice]['name']]['count'] 
                elif player_choice in ['3','4']: 
                    player.inventory(shop_choice_dict[player_choice]['name'])
                    player.gold_count-=shop_choice_dict[player_choice]['price']
                    print("Added "+shop_choice_dict[player_choice]['name'] +" to your inventory")
                    return player.gold_count

        ## If the choice is 4, then print out all of the player's equipment and let him type in the name of the item to be sold. remove the item, replace it with 
        ## "Empty slot" and then add the gold to the player's count.
        elif player_choice == '5':

            price_dictionary={
                "Empty Slot":0,
                "Wood Sword":1,
                "Iron Sword":5,
                "Iron Armor":5,
                "Steel Sword":10,
                "Steel Armor":10,
                "Adamantium Sword":15,
                "Adamantium Armor":15,
                "Magic Sword":50,
            }
            all_items = list(filter(lambda a: a !="Empty Slot", player.player_weapon_inventory + player.player_armor_inventory))
            

            # print(all_items)
        
            # print(all_items[0])
            # print(type(all_items[0]))
            print("\nI'll take any of these off of ya, for my price of course!\n")

            counter = 0
            for i in all_items:
                #if all_items[counter]!="Empty Slot":
                print(str(counter+1) + ") " + all_items[counter] + ": " +str(price_dictionary[all_items[counter]]) )
                counter += 1
                # else:
                #     pass
           

            item_to_sell = input("Correctly enter the name of the item you want to sell: ")
            if item_to_sell in price_dictionary:
                if "Sword" in item_to_sell:
                    player.player_weapon_inventory.remove(item_to_sell)
                    player.player_weapon_inventory.append("Empty Slot")
                    player.gold_count += price_dictionary[item_to_sell]

                    if player.player_sword_equipped == item_to_sell:
                        player.player_sword_equipped="Empty Slot"


                elif "Armor" in item_to_sell:
                    player.player_armor_inventory.remove(item_to_sell)
                    player.player_armor_inventory.append("Empty Slot")
                    player.gold_count += price_dictionary[item_to_sell]

                    if player.player_armor_equipped == item_to_sell:
                        player.player_armor_equipped="Empty Slot"


                print("\nSold " + item_to_sell + " for " +str(price_dictionary[item_to_sell]))


            else:
                print("Invalid Choice")
        else:
            break
    return

## Save game function. Appends all the current player instance's attributes into a single list. 
## The list is the written on one line in a localized .csv file. The file will be created if it does not already exist. 
## Tampering with this save file will cause issues upon running the game as the script automatically loads the player's data.
## As of right now, to start a new game, delete this save file and ensure the new_game.csv is in the same directory that your save file was in.

def Save_game():
    with open('save_file.csv',"w") as sf:
        write = csv.writer(sf)

      
        complete_save_file = [player.player_strength,player.player_health,player.player_mana,player.gold_count]+player.player_weapon_inventory+[player.player_sword_equipped]+player.player_armor_inventory+[player.player_armor_equipped]+spells+player.player_selected_spells+[player.player_items["Health Potion"]["count"]]+[player.player_items["Mana Potion"]["count"]]+[player.player_exp,player.player_level,player.until_next_level]
        print(complete_save_file)    
        write.writerow(complete_save_file)

        return complete_save_file
    sys.exit()

## Call the Main menu function to run the game. All other functions and methods are called accordingly.


## This function needs to either be called in another script or command line or uncommented to run.
## It must be commented out for pytest to run properly.
#Main_menu()
