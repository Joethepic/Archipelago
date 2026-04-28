# Gets the current Game status, as if you are in-game, in the menu, viewing the logo, etc.
CURRENT_GAME_STATUS: int = 0x809A90DC
# Gets the current galaxy that you are in. This address also says "File-Select" if you have not chosen a file yet.
CURRENT_GALAXY_STATUS: int = 0x809A90FC
# RAM Address offset to the start of all Galaxy struct address pointers
GALAXY_STRUCT_ADDR: int = 0x80900B18

# RAM Address for handling 1-ups
ONEUP_RAM_ADDR: int = 0x80F63CF0