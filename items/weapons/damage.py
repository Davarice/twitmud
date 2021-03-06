"""
Weapon Parts that contribute damage to the weapon. Blades, heads, points, spikes...Anything that can be used to kill.
"""
from numpy import round

from items import materials, decor

# from treasure_core import TreasureObject, form_out
from .structure import WPart


class Damager(WPart):
    size = 10
    type_damage = {}  # Coefficients of each damage type done by this component

    # How much damage does it do? (This will be greatly multiplied later)
    base_damage = 10
    # How fast can it be used?
    base_speed = 10

    Effectiveness = 4  # How much better the "good" damages are than the "bad" damages
    DamageTypesGood = []  # List of damage types that this component is good for
    DamageTypesBad = []  # List of damage types that this component is bad for
    # 0: Crush, 1: Pierce, 2: Slice

    # traits = {"Material": (materials.Metal.weapons, [100, 90, 50, 1])}
    # traits = {"Material": [materials.Steel]}
    materials = (materials.Metal.weapons, [100, 90, 50, 1])

    base_durability = 5
    TreasureType = "Weapon Component"

    def __init__(self, *a, override_material=None, **kw):
        super().__init__(*a, **kw)
        if override_material:
            self._material = override_material

    def damage_rating(self, split=True):
        # Amount of damage contributed by this component
        d = []
        try:  # FC: Assume the part contributes damage
            # for damage_type, coeffs in self.type_damage.items():
            for damage_type in ["Crush", "Pierce", "Slice"]:
                damage = 0
                # for damage_stat, coeff in self.stat_damage.items():
                # print(self, damage_type + ":")
                stats = self.type_damage.get(damage_type, {})
                for damage_stat, coeff in stats.items():
                    dmore = getattr(self.material, damage_stat) * coeff * self.size
                    # print(str(dmore), "from", getattr(self.material, damage_stat), damage_stat, "(" + self.material.__name__ + ")")
                    damage += dmore
                damage = damage * (1 - self.dmg["phys"] / 1000)
                d.append(damage / 100)

            for i in range(len(d)):
                if i in self.DamageTypesGood:
                    d[i] *= self.Effectiveness
                if i in self.DamageTypesBad:
                    d[i] /= self.Effectiveness
        except AttributeError:  # FC: It has been found that this part contributes no damage
            d = [0, 0, 0]
        d_out = [round(i, 2) for i in d]
        if not split:
            d_out = sum(d_out)
        return d_out


class Blade(Damager):
    """A long flat plane with sharp edges"""

    image = [
        "   ▄   ",
        "  ▟█▙  ",
        "  ███  ",
        "  ███  ",
        "  ███  ",
        "  ███  ",
        "  ███  ",
        "  ███  ",
    ]

    additions = [([None, decor.MetalPlating, decor.MetalInlay], [5, 3, 1])]
    size = 8
    type_damage = {  # Coefficients of each damage type done by this component
        "Crush": {"Density": 1, "Hardness": 0.5, "Flexibility": -0.2},
        "Pierce": {"Density": 0.3, "Hardness": 1, "Flexibility": 0.5},
        "Slice": {"Density": 0.2, "Hardness": 1, "Flexibility": 1},
    }

    base_damage = 10
    base_speed = 10

    Effectiveness = 4
    DamageTypesGood = [2]

    base_durability = 4
    TreasureType = "typical blade"


class BladeBig(Blade):
    """A very long flat plane with sharp edges"""

    image = [
        "   █   ",
        "  ▗█▖  ",
        "  ▐█▌  ",
        "  ▐█▌  ",
        "  ▟█▙  ",
        "  ███  ",
        "  ███  ",
        "  ███  ",
        " ▂███▂ ",
        "  ███  ",
        "  ███  ",
        "  ███  ",
    ]

    size = 14
    base_damage = 12
    base_speed = 6

    Effectiveness = 4
    DamageTypesGood = [2]
    DamageTypesBad = [1]

    TreasureType = "great blade"


class BladeCurved(Blade):
    """A short flat plane with sharp edges"""

    image = [
        "  ▄    ",
        "  █▙   ",
        "  ██▌  ",
        "  ███  ",
        "  ███  ",
        "  ███  ",
        "  ███  ",
    ]

    size = 7
    base_damage = 11
    base_speed = 14

    Effectiveness = 4
    DamageTypesGood = [2]
    DamageTypesBad = [0, 1]

    TreasureType = "curved blade"


class BladeCurvedBig(Blade):
    """A short flat plane with sharp edges"""

    image = [
        "▃▄▂    ",
        " ▜█▙   ",
        " ▐██▌  ",
        " ▐███  ",
        " ▝███  ",
        "  ███  ",
        " ▂███  ",
        "  ███  ",
        " ▂███  ",
        "  ███  ",
        "  ███  ",
        "  ███  ",
    ]

    size = 14
    base_damage = 12
    base_speed = 8

    Effectiveness = 3
    DamageTypesGood = [2]
    DamageTypesBad = [1]

    TreasureType = "great curved blade"


class Spike(Damager):
    """A cone with sharp edges, made for stabbing"""

    image = [
        "   ▂   ",
        "   █   ",
        "  ▐█▌  ",
        "  ▐█▌  ",
    ]

    additions = [([None, decor.MetalPlating, decor.MetalInlay], [5, 3, 1])]
    size = 4
    type_damage = {  # Coefficients of each damage type done by this component
        "Crush": {"Density": 1, "Hardness": 0.5, "Flexibility": -0.2},
        "Pierce": {"Density": 1, "Hardness": 2, "Flexibility": 1},
        "Slice": {"Density": 0.2, "Hardness": 0.6, "Flexibility": 0.7},
    }
    base_damage = 8
    base_speed = 14

    Effectiveness = 6
    DamageTypesGood = [1]
    DamageTypesBad = [0, 2]

    TreasureType = "bladed point"


class HeadClub(Damager):
    """A smooth heavy block or cylinder"""

    image = [
        "   ▄   ",
        "  ███  ",
        " ▐███▌ ",
        "  ███  ",
    ]

    additions = [([None, decor.GemEncrust, decor.MetalPlating, decor.MetalInlay], [10, 1, 3, 5])]
    size = 5
    type_damage = {  # Coefficients of each damage type done by this component
        "Crush": {"Density": 2.4, "Hardness": 0.1, "Flexibility": 0.2}
    }
    Effectiveness = 8
    DamageTypesGood = [0]
    TreasureType = "club head"


class Sphere(HeadClub):
    """A basic and smooth orb"""

    image = [
        "   ▀   ",
    ]

    additions = [([None, decor.GemEncrust], [10, 1])]
    size = 2
    type_damage = {  # Coefficients of each damage type done by this component
        "Crush": {"Density": 1.4, "Hardness": 0.2, "Flexibility": 0}
    }
    Effectiveness = 2
    TreasureType = "simple orb"


class HeadMace(HeadClub):
    """A heavy cylinder, with flanges or blades attached"""

    image = [
        "   ▄   ",
        " ╞███╡ ",
        " ╞███╡ ",
        " ╞███╡ ",
    ]

    size = 5
    type_damage = {  # Coefficients of each damage type done by this component
        "Crush": {"Density": 2.1, "Hardness": 0.1, "Flexibility": 0.2},
        "Slice": {"Density": 0.4, "Hardness": 0.3, "Flexibility": 0.1},
    }
    Effectiveness = 9
    TreasureType = "flanged head"


class HeadStar(HeadClub):
    """A heavy mass, with spikes attached"""

    image = [
        "   ╻   ",
        "  ▚█▞  ",
        " ╺███╸ ",
        "  ▞█▚  ",
    ]

    size = 5
    type_damage = {  # Coefficients of each damage type done by this component
        "Crush": {"Density": 2.1, "Hardness": 0.1, "Flexibility": 0.2},
        "Pierce": {"Density": 1, "Hardness": 0.3, "Flexibility": 0.1},
    }
    Effectiveness = 9
    TreasureType = "spiked head"


class HeadAxe(Damager):
    """A heavy blade that uses momentum to cleave"""

    image = [
        "█▙ ▄   ",
        "█████▙ ",
        "██████ ",
        "█▛ █ ▝ ",
    ]

    additions = [([None, decor.MetalInlay], [5, 1])]
    size = 7
    type_damage = {  # Coefficients of each damage type done by this component
        "Crush": {"Density": 0.8, "Hardness": 0.1, "Flexibility": -0.2},
        # "Pierce": {"Density": 0, "Hardness": 0, "Flexibility": 0},
        "Slice": {"Density": 1, "Hardness": 1.2, "Flexibility": 0.6},
    }
    Effectiveness = 4
    DamageTypesGood = [0, 2]
    TreasureType = "crescent blade"


class HeadHalberd(HeadAxe):
    """An axe blade with an additional spike"""

    image = [
        "   ▄   ",
        "█▙ █   ",
        "█████▙ ",
        "██████ ",
        "█▛ █ ▝ ",
    ]

    size = 8
    type_damage = {  # Coefficients of each damage type done by this component
        "Crush": {"Density": 0.8, "Hardness": 0.1, "Flexibility": -0.2},
        "Pierce": {"Density": 0.5, "Hardness": 1, "Flexibility": 0.5},
        "Slice": {"Density": 1, "Hardness": 1.2, "Flexibility": 0.6},
    }
    Effectiveness = 3

