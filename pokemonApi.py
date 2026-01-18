import requests
import json
offset=0
limit=1350
damage_multipliers = { #Here we have all damage multipliers for attacker-target types combinations
    "normal": {
        "normal": 1.0, "fighting": 1.0, "flying": 1.0, "poison": 1.0,
        "ground": 1.0, "rock": 0.5, "bug": 1.0, "ghost": 0.0,
        "steel": 0.5, "fire": 1.0, "water": 1.0, "grass": 1.0,
        "electric": 1.0, "psychic": 1.0, "ice": 1.0, "dragon": 1.0,
        "dark": 1.0, "fairy": 1.0
    },
    "fighting": {
        "normal": 2.0, "fighting": 1.0, "flying": 0.5, "poison": 0.5,
        "ground": 1.0, "rock": 2.0, "bug": 0.5, "ghost": 0.0,
        "steel": 2.0, "fire": 1.0, "water": 1.0, "grass": 1.0,
        "electric": 1.0, "psychic": 0.5, "ice": 2.0, "dragon": 1.0,
        "dark": 2.0, "fairy": 0.5
    },
    "flying": {
        "normal": 1.0, "fighting": 2.0, "flying": 1.0, "poison": 1.0,
        "ground": 1.0, "rock": 0.5, "bug": 2.0, "ghost": 1.0,
        "steel": 0.5, "fire": 1.0, "water": 1.0, "grass": 2.0,
        "electric": 0.5, "psychic": 1.0, "ice": 1.0, "dragon": 1.0,
        "dark": 1.0, "fairy": 1.0
    },
    "poison": {
        "normal": 1.0, "fighting": 1.0, "flying": 1.0, "poison": 0.5,
        "ground": 0.5, "rock": 0.5, "bug": 1.0, "ghost": 0.5,
        "steel": 0.0, "fire": 1.0, "water": 1.0, "grass": 2.0,
        "electric": 1.0, "psychic": 1.0, "ice": 1.0, "dragon": 1.0,
        "dark": 1.0, "fairy": 2.0
    },
    "ground": {
        "normal": 1.0, "fighting": 1.0, "flying": 0.0, "poison": 2.0,
        "ground": 1.0, "rock": 2.0, "bug": 0.5, "ghost": 1.0,
        "steel": 2.0, "fire": 2.0, "water": 1.0, "grass": 0.5,
        "electric": 2.0, "psychic": 1.0, "ice": 1.0, "dragon": 1.0,
        "dark": 1.0, "fairy": 1.0
    },
    "rock": {
        "normal": 1.0, "fighting": 0.5, "flying": 2.0, "poison": 1.0,
        "ground": 0.5, "rock": 1.0, "bug": 2.0, "ghost": 1.0,
        "steel": 0.5, "fire": 2.0, "water": 1.0, "grass": 1.0,
        "electric": 1.0, "psychic": 1.0, "ice": 2.0, "dragon": 1.0,
        "dark": 1.0, "fairy": 1.0
    },
    "bug": {
        "normal": 1.0, "fighting": 0.5, "flying": 0.5, "poison": 0.5,
        "ground": 1.0, "rock": 1.0, "bug": 1.0, "ghost": 0.5,
        "steel": 0.5, "fire": 0.5, "water": 1.0, "grass": 2.0,
        "electric": 1.0, "psychic": 2.0, "ice": 1.0, "dragon": 1.0,
        "dark": 2.0, "fairy": 0.5
    },
    "ghost": {
        "normal": 0.0, "fighting": 1.0, "flying": 1.0, "poison": 1.0,
        "ground": 1.0, "rock": 1.0, "bug": 1.0, "ghost": 2.0,
        "steel": 1.0, "fire": 1.0, "water": 1.0, "grass": 1.0,
        "electric": 1.0, "psychic": 1.0, "ice": 1.0, "dragon": 1.0,
        "dark": 0.5, "fairy": 1.0
    },
    "steel": {
        "normal": 1.0, "fighting": 1.0, "flying": 1.0, "poison": 1.0,
        "ground": 1.0, "rock": 2.0, "bug": 1.0, "ghost": 1.0,
        "steel": 0.5, "fire": 0.5, "water": 0.5, "grass": 1.0,
        "electric": 0.5, "psychic": 1.0, "ice": 2.0, "dragon": 1.0,
        "dark": 1.0, "fairy": 2.0
    },
    "fire": {
        "normal": 1.0, "fighting": 1.0, "flying": 1.0, "poison": 1.0,
        "ground": 1.0, "rock": 0.5, "bug": 2.0, "ghost": 1.0,
        "steel": 2.0, "fire": 0.5, "water": 0.5, "grass": 2.0,
        "electric": 1.0, "psychic": 1.0, "ice": 2.0, "dragon": 0.5,
        "dark": 1.0, "fairy": 1.0
    },
    "water": {
        "normal": 1.0, "fighting": 1.0, "flying": 1.0, "poison": 1.0,
        "ground": 2.0, "rock": 2.0, "bug": 1.0, "ghost": 1.0,
        "steel": 1.0, "fire": 2.0, "water": 0.5, "grass": 0.5,
        "electric": 1.0, "psychic": 1.0, "ice": 1.0, "dragon": 0.5,
        "dark": 1.0, "fairy": 1.0
    },
    "grass": {
        "normal": 1.0, "fighting": 1.0, "flying": 0.5, "poison": 0.5,
        "ground": 2.0, "rock": 2.0, "bug": 0.5, "ghost": 1.0,
        "steel": 0.5, "fire": 0.5, "water": 2.0, "grass": 0.5,
        "electric": 1.0, "psychic": 1.0, "ice": 1.0, "dragon": 0.5,
        "dark": 1.0, "fairy": 1.0
    },
    "electric": {
        "normal": 1.0, "fighting": 1.0, "flying": 2.0, "poison": 1.0,
        "ground": 0.0, "rock": 1.0, "bug": 1.0, "ghost": 1.0,
        "steel": 1.0, "fire": 1.0, "water": 2.0, "grass": 0.5,
        "electric": 0.5, "psychic": 1.0, "ice": 1.0, "dragon": 0.5,
        "dark": 1.0, "fairy": 1.0
    },
    "psychic": {
        "normal": 1.0, "fighting": 2.0, "flying": 1.0, "poison": 2.0,
        "ground": 1.0, "rock": 1.0, "bug": 1.0, "ghost": 1.0,
        "steel": 0.5, "fire": 1.0, "water": 1.0, "grass": 1.0,
        "electric": 1.0, "psychic": 0.5, "ice": 1.0, "dragon": 1.0,
        "dark": 0.0, "fairy": 1.0
    },
    "ice": {
        "normal": 1.0, "fighting": 1.0, "flying": 2.0, "poison": 1.0,
        "ground": 2.0, "rock": 1.0, "bug": 1.0, "ghost": 1.0,
        "steel": 0.5, "fire": 0.5, "water": 0.5, "grass": 2.0,
        "electric": 1.0, "psychic": 1.0, "ice": 0.5, "dragon": 2.0,
        "dark": 1.0, "fairy": 1.0
    },
    "dragon": {
        "normal": 1.0, "fighting": 1.0, "flying": 1.0, "poison": 1.0,
        "ground": 1.0, "rock": 1.0, "bug": 1.0, "ghost": 1.0,
        "steel": 0.5, "fire": 1.0, "water": 1.0, "grass": 1.0,
        "electric": 1.0, "psychic": 1.0, "ice": 1.0, "dragon": 2.0,
        "dark": 1.0, "fairy": 0.0
    },
    "dark": {
        "normal": 1.0, "fighting": 0.5, "flying": 1.0, "poison": 1.0,
        "ground": 1.0, "rock": 1.0, "bug": 1.0, "ghost": 2.0,
        "steel": 1.0, "fire": 1.0, "water": 1.0, "grass": 1.0,
        "electric": 1.0, "psychic": 1.0, "ice": 1.0, "dragon": 1.0,
        "dark": 0.5, "fairy": 0.5
    },
    "fairy": {
        "normal": 1.0, "fighting": 2.0, "flying": 1.0, "poison": 0.5,
        "ground": 1.0, "rock": 1.0, "bug": 1.0, "ghost": 1.0,
        "steel": 0.5, "fire": 0.5, "water": 1.0, "grass": 1.0,
        "electric": 1.0, "psychic": 1.0, "ice": 1.0, "dragon": 2.0,
        "dark": 2.0, "fairy": 1.0
    }
}


class Pokemon :
    """Pokemon class. Stores pokemon characteristics, methods to calculate damage multipliers, damage dealt, damage taken, increase score count"""
    def __init__(self, name, hp, attack, defense, special_attack, special_defense, speed, weight, height, ability_count, moves_count, base_exp, types):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        self.weight = weight
        self.height = height
        self.ability_count = ability_count
        self.moves_count = moves_count
        self.base_exp = base_exp
        self.types = types
        self.attack_count = 0 #To know when attacker should use special_attack instead of attack
        self.defense_count = 0 #To know when target should use special_defense instead of defense
        self.win_score = 0 #To know how many duels target has won

    def takeDamage(self, damage) : #extract attacker damage from target hp
        """
        Calculates and extracts damage from pokemons hp
        :param damage: Amount of damage taken
        """
        if self.defense_count == 1:
            self.hp -= max(0, damage - (self.special_defense / 2)) #decrease hp by damage decreased by half of special_defense. Can not be negative
            self.defense_count = 0
        else :
            self.hp -= max(0, damage - (self.defense / 2)) #decrease hp by damage decreased by half of defense. Can not be negative
            self.defense_count += 1
    
    def dealDamage(self, multiplier) : #calculate damage for target
        """
        Calculates amount of damage dealt to target
        :param multiplier: a vaule to multiply pokemons attack damage
        """
        if self.attack_count == 2:
            self.attack_count = 0
            return round(self.special_attack * multiplier)
        else:
            self.attack_count += 1
            return self.attack * multiplier
    
    @staticmethod
    def calculateModifier(attackerType, targetType): #calculate biggest damage multiplier
        """
        Calculates greatest damage multiplier for attacker
        
        :param attackerType: Attacker types
        :param targetType: Target types
        """
        best = 0 #Biggest damage multiplier
        for attack in attackerType:
            multiplier = 1 #Starting damage multiplier
            for defense in targetType:
                multiplier *= damage_multipliers[attack][defense] #Multiplying modifier for each attacker-target multiplier
            if multiplier > best:
                best = multiplier #If new multiplier is bigger than last biggest one, we assing it as a biggest one
        return best
    
    def win(self):
        """
        Increases pokemons score whenever it is called
        """
        self.win_score += 1 #increase win score by 1
        
    def restoreHp(self):
        """
        Sets pokemons hp, attack_count and defense_count back to default
        """
        self.hp = self.maxhp #restore hp after duel
        self.attack_count = 0
        self.defense_count = 0
    
    def to_dict(self) : #form data
        """
        Give only necessary data to store inside JSON file
        """
        return{
            "name": self.name,
            "hp": self.hp,
            "attack": self.attack,
            "defense": self.defense,
            "special_attack": self.special_attack,
            "special_defense": self.special_defense,
            "speed": self.speed,
            "weight": self.weight,
            "height": self.height,
            "ability_count": self.ability_count,
            "moves_count": self.moves_count,
            "base_exp": self.base_exp,
            "types": self.types
        }

def pokeType(data) : #Get pokemon types
    """
    Extracts pokemon's types
    
    :param data: data from the site
    """
    array = []
    for type in data['types']:
        array.append(type['type']['name'])
    return array

def pokeStat(data, name) : #Get characteristic of a pokemon by name
    """
    Docstring for pokeStat
    
    :param data: data from the site
    :param name: name of the parameter we are searching for
    """
    stats = data['stats']
    for stat in stats:
        if stat['stat']['name'] == name:
            return stat['base_stat']

pokemons_data = []
with open("pokemonDatabase.json", "r", encoding="utf-8") as f:
    pokemons = json.load(f)
if not pokemons :
    urls = requests.get(f"https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={limit}").json()['results']
    pokemons = []
    for data in urls:
        data = requests.get(f"{data['url']}").json() #Get parameters of each pokemon
        pokemon = Pokemon(
            name=data['name'],
            hp=pokeStat(data, 'hp'),
            attack=pokeStat(data, 'attack'), 
            defense=pokeStat(data, 'defense'), 
            special_attack=pokeStat(data,'special-attack'), 
            special_defense=pokeStat(data,'special-defense'), 
            speed=pokeStat(data, 'speed'),
            weight=data['weight'], 
            height=data['height'], 
            ability_count=len(data['abilities']), 
            moves_count=len(data['moves']), 
            base_exp=data['base_experience'],
            types=pokeType(data)
        )
        pokemons.append(pokemon.to_dict())
        pokemons_data.append(pokemon)
    with open("pokemonDatabase.json", "w", encoding="utf-8") as f:
        json.dump(pokemons, f, indent=2, ensure_ascii=False)
else :
    for pokemon in pokemons:
        pokemons_data.append(Pokemon(**pokemon))

def Initiative(p1, p2) : #Decide which pokemon starts combat
    """
    Decides which pokemon takes first turn at the start of the combat
    
    :param p1: Pokemon number 1
    :param p2: Pokemon number 2
    """
    combatant1 = (p1.speed, -p1.weight, -p1.height, p1.ability_count, p1.moves_count, p1.base_exp)
    combatant2 = (p2.speed, -p2.weight, -p2.height, p2.ability_count, p2.moves_count, p2.base_exp)
    if combatant1 > combatant2 :
        return p1, p2
    elif combatant2 > combatant1 :
        return p2, p1
    else:
        return None

def duel(pokemon1, pokemon2) :
    """
    Makes two chosen pokemon to fight until one of them is knocked down or it takes longer than 100 turns for anyone to win
    
    :param pokemon1: Pockemon number 1
    :param pokemon2: Pockemon number 2
    """
    print(f"{pokemon1.name} vs {pokemon2.name}")
    rounds = 1
    while(pokemon1.hp > 0 and pokemon2.hp > 0 and rounds < 100) : #duel lasts until one of contestants is dead or it took 100+ turns
        if rounds % 2 == 0:
            pokemon1.takeDamage(pokemon2.dealDamage(Pokemon.calculateModifier(pokemon2.types, pokemon1.types)))
            rounds += 1
        else :
            pokemon2.takeDamage(pokemon1.dealDamage(Pokemon.calculateModifier(pokemon1.types, pokemon2.types)))
            rounds += 1
    if (pokemon2.hp < 1) :
        pokemon1.win()
        pokemon1.restoreHp()
        pokemon2.restoreHp()
    elif (pokemon1.hp < 1) :
        pokemon2.win()
        pokemon1.restoreHp()
        pokemon2.restoreHp()
        
for i in range(len(pokemons_data)): 
    for j in range(i + 1, len(pokemons_data)): 
        order = Initiative(pokemons_data[i], pokemons_data[j])
        if order is None :
            continue
        one, two = order
        duel(one, two)
sortByScore = sorted(pokemons_data, key=lambda p: (-p.win_score, p.name))
score = []
for points in sortByScore:
    score.append(f"Name: {points.name}, points: {points.win_score}")
    
with open("leadersTable.json", "w", encoding="utf-8") as f:
        json.dump(score, f, indent=2, ensure_ascii=False)
print(score)