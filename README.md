# honkers
A discord bot that honks, maintains a blacklist, sends goose gifs, and has an item-finding game.

Core Commands
  goose say - Honkers will say whatever you'd like them to!
  goose say <message>\n   
  b!lastAuthor - Shows the last person to use goose say\n",
  setChannel - Set the channel for Honkers to welcome members in, please only enter channel names, not tags/IDs!
  welcOff - Turns off Honker's welcome messages, these are off by default
  welcOn - Turn on Honker's welcome messages
  invite - Invite Honkers!\nserver - Get the link for the Honkers Information and Support Server (HISS)  
  info - Shows basic information about Honkers
  stats - Shows some fun stats about Honkers

 Game Commands
  honkStart - Starts the game!
  honkDaily - Gives you a random amount of coins, has a 12 hour cooldown
  honkFind - Honkers will find an object for you! Has a cooldown of 30 minutes
  honkListItems - Lists the items in your inventory
  view - Shows any item
    b!view <item> 
  honkSell - Sells whichever item you name
    b!honkSell <item>
  honkCheck - Checks your balance
  honkAttack - Pay Honkers 100 coins to attack a user
    b!honkAttack @<user>
  honkDonate - Give money to someone
    b!honkDonate <amount> <user>
  honkRob - Rob a user of their hard earned coins! Honkers only has a 1/5 chance of succeeding and will give 200-800 coins on success. This command has a 2 minute cooldown regardless of success or failure.
    b!honkRob <user>
  honkGif - Sends a random goose gif! Doesn't require any coins to activate 
  vote - Sends a voting link for Honkers, gives between 400 and 600 coins and has a 12 hour cooldown
  
Moderation Commands - These are all admin commands excluding blacklistLs. They all have to be executing by someone with an 'Admin' role
  gooseOff - Turn Honkers off in *all* channels(only turns off responding to goose, honk, and duck-the game will still work)\n   
  gooseOff\ngooseOn - Turn Honkers on if previously turned off
  b!gooseOn\ngooseIgnore - Shushes goose in *only* the channel the message is sent in
  b!gooseIgnore\nrmGooseIgnore - Un-shushes Honker's lovely messages *only* in the channel the message is sent in
  b!rmGooseIgnore\nblacklistAdd - Creates a blacklist and adds a word to it
  blacklistRm - Removes a word from the blacklist
  delBlacklist - Deletes the blacklist
  blacklistLs - Lists the blacklist
