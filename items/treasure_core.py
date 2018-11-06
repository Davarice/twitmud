from numpy import random as npr

# Traits NOT to list (normally) in *.describe()
DEBUG = False


def normalize(in_):
    s = sum(in_)
    return [float(i) / s for i in in_]


def choose_from(choices: list, q=1, probability: list = None):
    """
    Choices will be a list. Each item of the list may also be a list or a tuple.
        If an item of Choices is a tuple, it will be a list of subchoices and a list of probabilities.
    Probability will be a list of numbers and overrides a probability list packed with the choices.
    Choose Q objects from Choices and return them.
    """
    if type(choices) not in [tuple, list]:
        # If Choices is a single item, return it immediately.
        return choices

    prob = None
    if type(choices) == tuple:
        (choices, prob) = choices

    if not probability:
        probability = prob or [1 for _ in choices]

    if DEBUG:
        print("\nChoices =", [type(x) for x in choices], "\nProbab. =", probability)

    choice: list = npr.choice(
        choices, size=q, replace=False, p=normalize(probability)
    ).tolist()
    for i in range(len(choice)):
        if type(choice[i]) == tuple:
            # If a tuple, 0 is list and 1 is prob; Choose
            choice[i] = choose_from(choice[i][0], 1, choice[i][1])
        while type(choice[i]) == list and len(choice[i]) > 1 and q == 1:
            # If a list of >1, choose one; Repeat
            choice[i] = choose_from(choice[i])
        while type(choice[i]) == list and len(choice[i]) == 1:
            # Remove all recursion from final result
            choice[i] = choice[i][0]
    return choice


def shuffle(obj, feat=None, r=False):
    for attr, (amin, amax, poss) in obj.attrs.items():
        if attr == feat or not feat:
            q = npr.randint(amin, amax + 1)
            selected = choose_from(poss, q)
            obj.dictAttr[attr] = selected
    for trait, poss in obj.traits.items():
        if trait == feat or not feat:
            selected = choose_from(poss)[0]
            obj.dictTrait[trait] = selected
    if r:
        for comp, obj2 in obj.dictComp.items():
            shuffle(obj2, feat, r)


class TreasureObject:
    attrs = {}
    # ATTRIBUTES: Flavor modifiers, no effect; Any number of a certain attribute type
    # A value in attrs MUST be: a TUPLE or LIST containing: INT1, INT2, LIST1
    # A value in the ATTRDICT of an instance of this class will then be:
    #     - a LIST containing between INT1 and INT2, inclusive, elements from LIST1
    traits = {}
    # TRAITS: Defining modifiers, possibly with effects; Exactly one of a given trait
    components = {}
    # COMPONENTS: Sub-objects that make up this object; Should be class name
    additions = {}
    # ADDITIONS: Extra sub-objects added on; Gemstones, precious metal inlay, etc
    materials = []
    # MATERIALS: Possibilities for object materials; May be left blank

    TreasureType = "Generic Treasure"
    BaseType = "item"

    # Damage FX; Adjectives applied when item is damaged
    dmg_FX = {
        "phys": ["dented", "chipped", "cracked", "broken"],
        "burn": ["singed", "charred", "melted"],
    }
    # Aesthetic FX; Adjectives applied when item is cold, bloody, etc
    aes_FX = {
        "cold": ["frosted", "frozen"],
        "blood": [
            "blood-speckled",
            "blood-spattered",
            "bloody",
            "bloodsoaked",
            "sanguinated",
        ],
    }
    size = 3

    def __init__(self, *args, **kwargs):
        self.dictAttr = {}
        self.dictTrait = {}
        self.dictComp = {}
        self.dictAdd = {}
        self.adjectives = []

        self.Value = 0
        self.TreasureLabel = None
        self.material = choose_from(self.materials)[0] if self.materials else None

        self.hp = 100
        self.dmg = {x: 0 for x in list(self.dmg_FX)}
        self.aes = {x: 0 for x in list(self.aes_FX)}
        # self.dmg = {x: npr.randint(0, 90) for x in list(self.dmg_FX)}
        # self.aes = {x: npr.randint(0, 90) for x in list(self.aes_FX)}

        for comp, v in self.components.items():
            if type(v) == list:
                choice = choose_from(v)[0]
                if not choice:
                    continue
            else:
                choice = v
            c = choice(*args, **kwargs)
            self.dictComp[comp] = c
        shuffle(self)

    def weight(self):
        w = 0
        try:
            w += self.size * self.material.Density
        except:
            pass
        for k, v in self.dictComp.items():
            w += v.weight()
        return w

    def clone(self, fulldata=True):
        """
        Create a clone of this object, but not necessarily with any non-obvious
            information maintained
        NOTE: If a user knowledge system is ever implemented, this could
            be used to create a "knowledge model", an INCOMPLETE representation
            of the object which may still hold secrets; for example, the kill
            history or given name of a historical sword
        """
        pass
