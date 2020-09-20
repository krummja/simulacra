import weakref


class WeakProperty:

    def __init__(self, name: str) -> None:
        self.name = name

    def __get__(self, cls, desc):
        if self is None:
            return desc

        try:
            ref = self.__dict__[desc.name]
        except KeyError:
            return None
        else:
            value = ref()
            if value is None:
                del self.__dict__[desc.name]
            return value
    
    def __set__(self, value, desc):
        self.__dict__[desc.name] = weakref.ref(value)

    def __delete__(self, desc):
        del self.__dict__[desc.name]


class Relation:
    """Some kind of relationship that exists between two entities. Common
    example is containment: if an item is in an inventory, then the entity with
    the inventory 'contains' the item, and a relation `Contains(entity, item)`
    exists.
    """

    from_entity = WeakProperty('from_entity')
    to_entity = WeakProperty('to_entity')

    def __init__(self, from_entity, to_entity) -> None:
        self.from_entity = from_entity
        self.to_entity = to_entity

        self.attach()

    @classmethod
    def create(cls, from_entity, to_entity):
        relation = cls(from_entity, to_entity)
        return CreateRelationEvent(relation)

    def attach(self):
        cls = type(self)
        self.from_entity.relates_to[cls].add(self)

    
class CreateRelationEvent:

    def __init__(self, relation) -> None:
        self.relation = relation
        self.target = relation.to_entity
    
    # def fire(self, world):
    #     subevent = self.relation.on_create(
    #         self.relation.from_entity,
    #         self.relation.to_entity
    #     )
    #     subevent.fire(world)
    #     if not subevent.cancelled:
    #         self.relation.attach()