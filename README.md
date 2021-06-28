# embedded_game
TETRIS GAME

Down, Left, Right, B button activated.

Down: Drop block faster \
Left: Move block left \
Right: Move block right

B: Rotate block as clockwise


Build-up

FIELD / BLOCK(current) / BLOCK(NEXT) / MESSAGES


1. Calculate things on array. \
  Create 7 types of block & Make class about block (including update)

2. Move array values to pixel coordinate. \
  Draw basic game field.(Only wall and floor) \
  Draw Block. \
  \
  Dropping current block til crashing wall, floor or other blocks. \
  If it crashes, block info will saved on field.
  
3. LOOP
  Read button signal \
  Use update function to check crash and erase. \
  Calculate score \
  Check if game ends. \
  Draw field & block continuously.
  
  Show display
