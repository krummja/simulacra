# Chiseling Algorithm

We want to start by building a 2D array with "articulation point", or cells that, if they were to be marked as unwalkable, would split the remaining cells into separate untraversable components.

## Articulation Points

1. Apply a Depth-First Search (DFS) on a graph. Get the DFS tree.
2. A node which is visited earlier is a "parent" of those nodes which are reached by it and visited later.
3. If any child node does not have a path to any of the ancestors of its parent, it means that removing this node would make this child disjoint from the graph.
4. There is an exception: the root of the tree. If it has more than one child, then it is an articulation point. Otherwise, not.

The following is a pseudo-code implementation.

```cpp
DFS ()  ;; graph G = (V, E)
    foreach v in V
        if (! v.visited)
        then Visit (v)

Visit (vertex v)
    v.visited = true
    foreach w adjacent to v
        if (! w.visited)
        then Visit (w)
```

### Biconnectivity

A connected, undirected graph is _biconnected_ if the graph is still connected after removing any one vertex.

If a graph is not biconnected, the disconnecting vertices are called _articulation points_.

### Finding Articulation Points

1. From any vertex v, perform DFS and number vertices as they are visited.
2. Let `Low(v)` = lowest-numbered vertex reachable from v using 0 or more spanning tree edges, and then at most one back edge.


```
Num(v) is the visited number
Low(v) = minimum of
    Num(v)
    Lowest Num(w) among all back edges (v,w)
    Lowest Low(w) among all tree edges (v,w)

Root is articulation point iff it has more than one child
Any other vertex v is articulation point iff
    v has some child w such that Low(w) >= Num(v)
    i.e. is there a child w of v that cannot reach a vertex visited before v?
         if yes, removing v will disconnect w -> v is an articulation point
```

There is a higher-level algorithm that can do this.

1. Perform pre-order traversal to compute Num.
2. Perform post-order traversal to compute Low.
3. Perform another post-order traversal to detect articulation points.

```cpp
void Graph::assignNum( Vertex v )
{
    v.num = counter++;
    v.visited = true;
    for each Vertex w adjacent to v
    {
        if ( !w.visited )
        {
            w.parent = v;
            assignNum( w );
        }
    }
}

void Graph::assignLow( Vertex v )
{
    v.low = v.num;  // Rule 1
    for each Vertex w adjacent to v
    {
        if ( w.num > v.num )  // Forward edge
        {
            assignLow( w );
            if ( w.low >= v.num )
                cout << v << " is an articulation point" << endl;
            v.low = min( v.low, w.low );  // Rule 3
        }
        else
        if ( v.parent != w )  // Back edge
            v.low = min( v.low, w.num );  // Rule 2
    }
}

void Graph::findArt( Vertex v )
{
    v.visited = true;
    v.low = v.num = counter++;  // Rule 1
    for each Vertex w adjacent to v
    {
        if ( !w.visited )  // Forward edge
        {
            w.parent = v;
            findArt( w );
            if ( w.low >= v.num )
                cout << v << " is an articulation point" << endl;
            v.low = min( v.low, w.low );  // Rule 3
        }
        else
        if ( v.parent != w )  // Back edge
            v.low = min( v.low, w.num );  // Rule 2
    }
}
```
