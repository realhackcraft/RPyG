---
dependencies:
  - "[[Refactor Map loading into classes]]"
---
Multi-tile structures can be achieved by placing a marker at the top left corner of the structure, then replacing it in the map rendering with the real tiles.

Example of structure file:

`asset/structures/house.txt`

```
C: asset/colors.txt, S: H, T: X
X X X X X H H X X X X X
X X H H H H H H H H X X
X X X H W W W W H X X X
X X X H W W W W H X X X
X X X H W D D W H X X X
```

`asset/map.txt`
```
C: asset/colors.txt, I: asset/structures/house.txt 
H W W W W W W W W W W W W W W
W W W W W W W W W W W W W W W
W W W W W W W W W W W W W W W
W W W W W W W W W W W W W W W
W W W W W W W W W W W W W W W
W W W W W W W W W W W W W W W
W W W W W W W W W W W W W W W
```

This map will result in the following render:

```
W W W W W H H W W W W W W W W
W W H H H H H H H H W W W W W
W W W H W W W W H W W W W W W
W W W H W W W W H W W W W W W
W W W H W D D W H W W W W W W
W W W W W W W W W W W W W W W
W W W W W W W W W W W W W W W
```
(The `W` inside the `H` stands for "Wall" instead of "Water", can because the "Wall" is rendered using differing colors than the map, the wall can be, for example, beige instead of blue.)

Attributes:


| Symbols | Description                                                    | Notes                                           |
| ------- | -------------------------------------------------------------- | ----------------------------------------------- |
| `C`     | The color sheet of the map                                     | Doesn't need to include the transparent tile    |
| `T`     | The symbol used to mark gaps for transparency                  | Will be ignored if using the structure as a map |
| `I`     | Other structures to import                                     |                                                 |
| `S`     | The symbol that other maps can use to reference this structure |                                                 |


Also note that:
- The structure can embed its colors independently from its map, and therefore allow a map to contain two symbols of different colors.