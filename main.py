
from puzzle import Puzzle
from relationship_enum import Relationship

# The Brit lives in the Red house.
# The Swede keeps Dogs as pets.
# The Dane drinks Tea.
# The Green house is exactly to the left of the White house.
# The owner of the Green house drinks Coffee.
# The person who smokes Pall Mall rears Birds.
# The owner of the Yellow house smokes Dunhill.
# The man living in the centre house drinks Milk.
# The Norwegian lives in the first house.
# The man who smokes Blends lives next to the one who keeps Cats.
# The man who keeps Horses lives next to the man who smokes Dunhill.
# The man who smokes Blue Master drinks Beer.
# The German smokes Prince.
# The Norwegian lives next to the Blue house.
# The man who smokes Blends has a neighbour who drinks Water.

pz = Puzzle()
pz.add_values("Home", [1, 2, 3, 4, 5])
pz.add_values("Color", ["Blue", "Green", "Red", "White", "Yellow"])
pz.add_values("Nationality", ["Brit", "Dane", "German", "Norwegian", "Swede"])
pz.add_values("Drink", ["Beer", "Coffee", "Milk", "Tea", "Water"])
pz.add_values("Cigarette", ["Blends", "Blue Master", "Dunhill", "Pall Mall", "Prince"])
pz.add_values("Pet", ["Birds", "Cats", "Dogs", "Horses", "Fish"])

# The Brit lives in the Red house.
pz.add_condition(Relationship.EQ, {"Nationality": "Brit"}, {"Color": "Red"})
# The Swede keeps Dogs as pets.
pz.add_condition(Relationship.EQ, {"Nationality": "Swede"}, {"Pet": "Dogs"})
# The Dane drinks Tea.
pz.add_condition(Relationship.EQ, {"Nationality": "Dane"}, {"Drink": "Tea"})
# The owner of the Green house drinks Coffee.
pz.add_condition(Relationship.EQ, {"Color": "Green"}, {"Drink": "Coffee"})
# The person who smokes Pall Mall rears Birds.
pz.add_condition(Relationship.EQ, {"Cigarette": "Pall Mall"}, {"Pet": "Birds"})
# The owner of the Yellow house smokes Dunhill.
pz.add_condition(Relationship.EQ, {"Color": "Yellow"}, {"Cigarette": "Dunhill"})
# The man living in the centre house drinks Milk.
pz.add_condition(Relationship.EQ, {"Home": 3}, {"Drink": "Milk"})
# The Norwegian lives in the first house.
pz.add_condition(Relationship.EQ, {"Nationality": "Norwegian"}, {"Home": 1})
# The man who smokes Blue Master drinks Beer.
pz.add_condition(Relationship.EQ, {"Cigarette": "Blue Master"}, {"Drink": "Beer"})
# The German smokes Prince.
pz.add_condition(Relationship.EQ, {"Nationality": "German"}, {"Cigarette": "Prince"})
# The Green house is exactly to the left of the White house.
pz.add_condition(Relationship.EQ, {"Color": "Green"}, {"Color": "White"}, "Home", -1)
# The man who keeps Horses lives next to the man who smokes Dunhill.
pz.add_condition(Relationship.GE, {"Pet": "Horses"}, {"Cigarette": "Dunhill"}, "Home", -1)
pz.add_condition(Relationship.LE, {"Pet": "Horses"}, {"Cigarette": "Dunhill"}, "Home", 1)
# The man who smokes Blends lives next to the one who keeps Cats.
pz.add_condition(Relationship.GE, {"Cigarette": "Blends"}, {"Pet": "Cats"}, "Home", -1)
pz.add_condition(Relationship.LE, {"Cigarette": "Blends"}, {"Pet": "Cats"}, "Home", 1)
# The Norwegian lives next to the Blue house.
pz.add_condition(Relationship.GE, {"Nationality": "Norwegian"}, {"Color": "Blue"}, "Home", -1)
pz.add_condition(Relationship.LT, {"Nationality": "Norwegian"}, {"Color": "Blue"}, "Home", 1)
# The man who smokes Blends has a neighbour who drinks Water.
pz.add_condition(Relationship.GE, {"Cigarette": "Blends"}, {"Drink": "Water"}, "Home", -1)
pz.add_condition(Relationship.LE, {"Cigarette": "Blends"}, {"Drink": "Water"}, "Home", 1)

if pz.solve():
    for elm in pz.solution:
        print(elm)

# iteration:  1781
# Sonuç Bulundu!
# [1, 'Yellow', 'Norwegian', 'Water', 'Dunhill', 'Cats']
# [3, 'Red', 'Brit', 'Milk', 'Pall Mall', 'Birds']
# [2, 'Blue', 'Dane', 'Tea', 'Blends', 'Horses']
# [4, 'Green', 'German', 'Coffee', 'Prince', 'Fish']
# [5, 'White', 'Swede', 'Beer', 'Blue Master', 'Dogs']
