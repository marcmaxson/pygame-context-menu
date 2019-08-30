# pygame-context-menu
Adds a class to provide right-click "Context Menus" to pygame. This is the menu which appears when you right-click on the desktop or a file or folder in Windows. It gives you added functionality by offering you actions you can take with the clicked item. Most programs like to stuff their commands in this menu, and pygame didn't provide one.

## features
- includes a demo of how this integrates into pygame
- doesn't require any other imports besides `pygame` itself
- creates a Windows style menu at the spot on Surface where user right-clicks, filled in by menu items you supply
- Menu is a list of tuples `[("text to show", function_to_call),...]` 
- Mouseover on menu highlights the options
- Left clicking menu items will run those functions/actions
- clicking anywhere else will close the menu and restore the underlying image to the Surface.
- Ideal for turn-based games where there is no dynamic animation underneath the menu that pops up.
- For the menu_controller to manage mouse, there is a piece of code to insert into your game loop. So you supply a menu object and add this game loop stuff, and that's it.
