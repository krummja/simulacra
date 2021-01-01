# Apparata Graph Engine and Parser

1. Build individual areas
   - Plains, towns, roads, rocky passages, etc.
   - Define every area with a mini-grammar, specifying how nodes should branch.
   - Include endpoints where areas may connect
2. Use a higher-level set of rules to specify which areas should be generated and the optimal place to attach them, e.g. attach a forest first, then a town, then a bridge, etc.
   - Ideally, able to specify chains of features:
        forest -> tunnel -> town -> road -> mountain -> ...
3. Clean up unused paths. Build other map features like rivers and other things.
4. Map the objects to a grid and finally build tiles to populate the map.


## Graph Grammar
Parts of areas should be specified as smaller graphs that map the topology of the surroundings.

```
town1
{
    w = 30;
    h = 30;
}

plains1
{
    w = 100;
    h = 100;
}

town1 -> path1
{
    adjacent;
    copies = 10;
    dist = 64;
    angle = 90;
}

path1
{
    w = 16;
    h = 16;
}
```

## Generator Grammars