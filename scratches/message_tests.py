from __future__ import annotations

import re

class Message:
    
    def __init__(self, text: str, noun1=None, noun2=None) -> None:
        self.text = self._format(text, noun1=noun1, noun2=noun2)
    
    def _format(self, text: str, noun1=None, noun2=None) -> str:
        result = text
        
        nouns = [noun1, noun2]
        for i in range(len(nouns)):
            noun = nouns[i]
            if noun is not None:
                result = result.replace(f'{i}', noun)
        return result
    
    def __str__(self) -> str:
        return self.text


class Pronoun:
    
    nom: str
    obl: str
    gen: str
    
    def __init__(self, nom: str, obl: str, gen: str) -> None:
        self.nom = nom
        self.obl = obl
        self.gen = gen
    
    @classmethod
    def you(self) -> Pronoun:
        return Pronoun('you', 'you', 'your')


class Player:
    
    @property
    def pronoun(self) -> Pronoun:
        return Pronoun.you


log = []
log.append(Message(f"{0} attack[s] {1}.", noun1="Aulia", noun2="an orc"))
print(log[0])


optional = "\[(\w+?)\]"

text = "The orc pick[s] up the axe."

match = re.search(optional, text)
if match is not None:
    before = text[0:match.span()[0]]
    after = text[match.span()[1]:]
    
    print(f"{before}{match[1]}{after}")
    

player = Player()
pro = player.pronoun()
print(pro)
print(player.pronoun().nom)

them = "obl"
longsword = {
    'noun_text': "Longsword"
}
result = f"you pick up the {1} and stow {1, them}"
result = result.replace(f"{1}", f"{longsword['noun_text']}")
print(result)

result = result.replace(f"({longsword['noun_text']}, 'obl')", 'it')
print(result)
