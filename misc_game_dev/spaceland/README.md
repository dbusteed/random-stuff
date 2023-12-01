## Gameplay (Big Picture)

- you are a spaceship pilot
- gameplay driven by exploration
- space is filled with STUFF
    - inhabited planets
    - unexplored, uninhabited planets
    - aliens
    - space stuff
        - asteroids
        - junk
        - satelites
        - black holes
    - other space explorers
- maybe some animal crossing objectives (ie find all the ships, meet all the aliens)
- travel with warp jump
- maybe different questlines? or maybe pretty isolated adventures
- factions and groups
- different "areas" of space, with different risk factors
- is there dialogue where you can choose responses? with like charisma skill? that might be too outta scope

## World

- Needs a combination of simulation and static map
    - so like planets stay in place, but things like other ships and space junk needs to be simulated
- systems are clusters of planets and others stuff
- maybe player starts in one system, then get's super warp jump which let's them jump systems?
- or maybe just a really really big map?
- how to deal with boundaries?

- quadrant > system > universe
quadrant isn't "real", but just a map unit
so all systems will be 3x3 quadrant (123, 456, 789)
these systems are BIG! so that warping in a system is necessary

but how do you go from sys to sys?


- different factions, different relationships within those factions
    - ie they might be neutral to you, or kidnap you, or attack on sight
- individual ships can have multiple loyalties like you, so they might be loyal to humans and pirates, 
  but since they are pirate they will attack, etc. maybe that's too much, just do it off factions.
- various levels of loyalty have different benefits, ie if your a good friend with a group they will aid in fights,
  if they are like super friends you can command them or something or have them follow you in formation

start with the basics

aliens

maybe this takes place at the beginning of the space period, so one objective would be like the forming of the space federation of aliens
- so like start out as the first human to explore space? or maybe not even that, cause there gotta be other planets for fun

"Fractured Space"

so..... who joins the Confederation? is it species? or planets?

who opposes the GC? hostile planets? but why?

k basics. what's the goal of the GC? why put one together in the first place?
- fight evil?
- economic prosperity?
- prevent wars?

trade routes?? oh no not this again!
- keep it simple

corporations
pirates
rebels
merchants
idealogical societies



## Mechanics

- flying
    [ ] gotta be good since that's the primary interaction
    [x] turn with A/D
    [x] discrete throttle adjustment with W/S
    [ ] different flying "abilities"?
        [ ] maybe this (and other traits) dictated by the ship you have
        [ ] or upgrades, like quick turn
    [ ] warp jump
        - need to stop first, then launch?
        - no! but warping while moving is more unstable
        - this needs to feel and look good!
        - kinda need a big map / minimap for testing this
        - IDEA #1: when you start to charge the warp, the minimap opens up, which shows
          a rudimentary version of the area, as you charge the possible landing zone indicator grows,
          you can turn left and right and it will update, can escape the warp sequence, or just hold
          and let go when ready, then minimap closes and you are launched
          - cool if this (and other UI elements) could get a cool retro scanline effect, or something along those lines
- weapons / tools
    - laser
    - tractor beam
    - probe?
    - shield
    - flare / mine
    - seeking missile
- n-body physics? or even non-simulated orbits

## UI

- HUD!
    [x] minimap
    [x] location
    [x] health 
    [ ] warp drive
    [ ] throttle / direction?
    [ ] weapons / abilities (left)

- ship computer (pipboy kinda)
    - full map
    - other stuff
    - bloom effect would be cool (but no WASM)

- warp interface
    - pulls up overlay window

minimap
[ ] zoom
[ ] hide minimap?
[ ] full map?
[ ] only represents explored areas...

would need some sort of "fog" on the map.
that might be pretty tricky, so instead maybe
just keep track of notable objects discovered per quadrant
- mostly planets, but maybe other things
and that can be displayed in the location area (2/?, etc)


need to build the map!
- bosco-size map will be one quadrant
- 

boundaries?
- maybe something about too far from the universe center, could make everything dark cause too far from universe. we need to mix the fun of exploring but needs some bounds i guess

basically a sudoku board 
- 9 systems, each made up of 9 sectors

map
- sector map
    - show the current sector, show discovered POI
    - location of player
    - % of POI discovered
    - arrow keys to toggle thru POI with details
- system map
    - show the 3x3 grid, scaled down POI from the sectors
    - location of player
    - use arrow keys to hover over different sectors and select them
    - unvisisted sectors will be grayed and can't be clicked
    - visisted ones can show the discovery level
- galaxy map
    - similar to above

when it comes to warp jumping
- can't warp within a sector?
- so when start to warp, warp interface (the map) opens up at the system level and shows
  where you are headed (the line grows as you hold and angles as you a/d)


when the map turns, game is paused, so don't need to update positions,
but will need to "sync and spawn" the translated positions of the markers


there will need to be some sort of sector offset (LATER)

the map needs to feel good! (cause map is fun, but also used for warp jump)
- tween to open window
- when open then call an event to show content

make the exploration fun with some randomly generated elements

different quest lines, ie if you follow the galactic federation path you will make the council HQ
what's the story behind it all?
- maybe you're the official ambassador for earth, but there's other humans flying around.
- the timeline dictates the need for exploration and amount of existing colonies etc
- exploration > colonies
- So the game begins with Earth discovering space travel? nah that's weird

so maybe you explore and that's it. who cares about the explanation, so there can be earth colonies, etc.
and it's possible to get a map but not very common (or it's very expensive)

maybe warp drive  also is like AP for other manuevers like quick turns, etc

basically ya

each POI needs to know how to draw its marker
- when discovered, the marker entity exists on that camera

how to manage all the different entities...kinda bigger dev concept
nah just put them all there! when discovered we spawn the minimap marker

+---+---+---+ 
| α | β | γ |
+---+---+---+
| δ | θ | κ |
+---+---+---+
| λ | σ | ω |
+---+---+---+

+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+

+-----------+
|         * |
| *         |
|        @  |
|    %      |
|         * |
+-----------+

example:
    sector width (SW) = 1000
    9x9 sectors = 81 sectors

translate coordinates to 0-80?
and then translate that to galaxy-sector?