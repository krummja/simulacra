from components.material import Material

Skin = Material('skin', 'Skin', hardness=0, sharpness=0, potency=0.2, weight=0.1, value=0)
Flesh = Material('flesh', 'Flesh', hardness=0, sharpness=0, potency=0.2, weight=0.15, value=0)
Fur = Material('fur', 'Fur', hardness=0.1, sharpness=0, potency=0.2, weight=1, value=1)
Leather = Material('leather', 'Leather', hardness=0.1, sharpness=0, potency=0.2, weight=1, value=1)
Wood = Material('wood', 'Wood', hardness=0.3, sharpness=0.4, potency=0.5, weight=3, value=0.5)
Bone = Material('bone', 'Bone', hardness=0.5, sharpness=0.5, potency=0.5, weight=5, value=1)
Stone = Material('stone', 'Stone', hardness=0.5, sharpness=0.2, potency=0.1, weight=6, value=0.1)
Iron = Material('iron', 'Iron', hardness=0.7, sharpness=1, potency=0.6, weight=5.85, value=20)
Steel = Material('steel', 'Steel', hardness=0.8, sharpness=1.2, potency=0.8, weight=6.5, value=150)

material_templates = {
    Skin.uid: Skin,
    Flesh.uid: Flesh,
    Fur.uid: Fur,
    Leather.uid: Leather,
    Wood.uid: Wood,
    Bone.uid: Bone,
    Stone.uid: Stone,
    Iron.uid: Iron,
    Steel.uid: Steel
    }