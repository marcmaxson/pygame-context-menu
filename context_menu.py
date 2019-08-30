# python 3.7
## TODO
# add option to show icons next to menu items
# pass in kwargs to action-functions somehow

if __name__ == '__main__':
    # TESTING ONLY -- not used if imported
    # globals
    import pygame
    pygame.init()
    clock = pygame.time.Clock()

    # COLORS
    BLACK = (0,0,0)
    WHITE = (222,222,222)
    GREY = (23,23,23)
    BORDER = (190, 190, 190)
    LIGHT_GREY = (220,220,220)
    GREEN_TEXT = (110,180,110)
    GREEN = (60,160,60)
    # SCREEN RESOLUTIONS
    SCREEN_RES = (480, 512)

    # screen = pygame.display.set_mode((500, 500), HWSURFACE | DOUBLEBUF | RESIZABLE)
    screen = pygame.display.set_mode(SCREEN_RES, 0, 32, pygame.RESIZABLE)
    pygame.display.set_caption('Box Test')
    image = pygame.image.load("stellar-nebulae/stellar-black-hole-1.jpg")
    SIZE = image.get_rect().size
    print(SIZE)
    screen.blit(image, (0,0), image.get_rect())
    pygame.display.flip()

    # font
    FONT20 = pygame.font.Font('Candara.ttf', 20)
    MARGIN = 0 # BUGGY PART! -- should control the whitespace around menu items but doesn't work with highlighter

    ## DEMO parameters
    def dummy_action():
        print('1')
    menu = [('test test test', dummy_action),
            ('more more more', dummy_action),
            ('third', dummy_action)]
    panel = None


class ContextMenu(object):
    """ creates the list, then removes the list and replaces what was on screen previously. """
    def __init__(self, screen, event_pos, menu_obj, font=None):
        if not font:
            self.font = pygame.font.SysFont('Arial', 25)
        else:
            self.font = font
        self.screen = screen
        self.x = event_pos[0]
        self.y = event_pos[1]
        self.menu = menu_obj # a list of tuples: ('text', event_or_function_to_call)
        self.height = 0
        self.width = []
        for (text, action) in self.menu:
            text_width, text_height = self.font.size(text)
            self.width.append( text_width )
            self.height += text_height
        self.width = max(self.width) + 2 * self.font.size('  ')[0]
        #self.height = len(self.menu) * FONT20.size("Tg")[1] # estimated
        #self.width = max([len(item) for item in self.menu]) *  # estimated
        ## SAVE original screen stuff - to restore later.
        self.orig = pygame.image.tostring(self.screen, 'RGBA')
        self.events_map = []
        self.draw_menu()
        self.highlighted_item = None
        
    def draw_menu(self):
        self.menu_width = self.width + MARGIN
        self.menu_height = self.height + MARGIN
        self.menu_size = (self.menu_width, self.menu_height)
        this_surface = pygame.Surface(self.menu_size)
        this_surface.fill(LIGHT_GREY)
        pygame.draw.rect(this_surface, BORDER, (0, 0, self.menu_width, self.menu_height), 3)
        self.this = this_surface

        new_event_map = [] # (box) list
        for lindex, (text, action) in enumerate(self.menu):
            textSurface = self.font.render('  '+text, True, GREY)
            (topleftx, toplefty, width, height) = textSurface.get_rect()
            #toplefty += (lindex * self.font.size("Tg")[1])
            topleftx += MARGIN
            toplefty += MARGIN + (lindex * height)
            self.this.blit(textSurface, (topleftx, toplefty, width, height))
            ### here, clicking this region now triggers the action:
            ### update event map, with absolute screen borders for this text.
            #print(self.x, self.y, (self.x + topleftx, self.y + toplefty, self.x + width, self.y + toplefty + height))
            new_event_map.append((action,(self.x + topleftx,
                                          self.y + toplefty,
                                          self.x + topleftx + width,
                                          self.y + toplefty + height)))
        self.screen.blit(self.this, (self.x, self.y))
        pygame.display.update()
        self.events_map = new_event_map

    def draw_carrot_menu_item(self, menu_obj_index, highlightit=True):
        """ highlightit: True turns on; False turns off """
        text = self.menu[menu_obj_index][0]
        textSurface = self.font.render('  '+text, True, GREY)
        (topleftx, toplefty, width, height) = textSurface.get_rect()
        # assuming one line per menu item; no wrap yet
        
        #highlight = pygame.Surface((10,10)) #(width, height))
        #COPY = pygame.Surface((10,10)) #(width, height))
        if highlightit:
            pygame.draw.polygon(textSurface, GREEN_TEXT, [(0,5), (5,10), (0,15)], 3)
            #highlight.fill(BORDER)
            #COPY.fill(BORDER)
        else:
            pygame.draw.polygon(textSurface, LIGHT_GREY, [(0,3), (5,10), (0,15)], 3)
            #highlight.fill(LIGHT_GREY)
            #COPY.fill(LIGHT_GREY)
        topleftx += MARGIN
        toplefty += MARGIN + (menu_obj_index * height)        
        self.this.blit(textSurface, (topleftx, toplefty, width, height))
        self.screen.blit(self.this, (self.x, self.y))

        pygame.display.update()
        #return (action, (self.x + topleftx, self.y + toplefty, self.x + width, self.y + toplefty + height))

    def draw_highlight_menu_item(self, menu_obj_index, highlightit=True):
        """ highlightit: True turns on; False turns off.
        assuming one line per menu item; no wrap yet.
        BUGGY -- won't redraw the text after unhighlighting."""
        text = self.menu[menu_obj_index][0]
        textSurface = self.font.render('  '+text, True, GREY)
        (topleftx, toplefty, width, height) = textSurface.get_rect()
        highlight = pygame.Surface((width, height))
        if highlightit:
            highlight.fill(BORDER)
        else:
            highlight.fill(LIGHT_GREY)
        topleftx += MARGIN/2
        toplefty += MARGIN/2 + (menu_obj_index * height)
        highlight.blit(textSurface, (topleftx, toplefty, width, height))
        self.this.blit(highlight, (topleftx, toplefty, width, height))
        self.this.blit(textSurface, (topleftx, toplefty, width, height))        
        self.screen.blit(self.this, (self.x, self.y))
        pygame.display.update()

    def clear(self):
        """ DEBUG just puts a black box where menu used to be"""
        self.this = pygame.Surface((self.width, self.height))
        self.this.fill((BLACK))
        self.screen.blit(self.this, (self.x, self.y))
        pygame.display.update()
        
    def close(self):
        """ restores the image under the menu by restoring the whole screen """
        surf = pygame.image.fromstring(self.orig, self.screen.get_size(), 'RGBA')
        screen.blit(surf, (0,0), surf.get_rect())
        pygame.display.update()

    def check_menu_events(self, event_pos):
        (x,y) = event_pos
        print((x,y))
        for action, (minx, miny, maxx, maxy) in self.events_map:
            if minx <= x <= maxx and miny <= y <= maxy:
                return action

    def mouseover_highlight(self):
        (x,y) = pygame.mouse.get_pos()
        for lindex, (action, (minx, miny, maxx, maxy)) in enumerate(self.events_map):
            # IF mouse outside a box, and that box is highlighted, off it.
            if (self.highlighted_item == lindex and
                ((x < minx or x > maxx) or
                (y < miny or y > maxy))):
                self.highlighted_item = None
                #print ( ('outside', x, y, (minx, miny, maxx, maxy)) )
                self.draw_highlight_menu_item(lindex, highlightit=False)
            # if mouse inside a box, highlight it.
            if minx <= x <= maxx and miny <= y <= maxy:
                # if another index is highlighted, turn that off now.
                if self.highlighted_item and self.highlighted_item != lindex:
                    self.draw_highlight_menu_item(self.highlighted_item, highlightit=False)
                    self.draw_carrot_menu_item(self.highlighted_item, highlightit=False) 
                elif self.highlighted_item == lindex:
                    # still in bounds of box
                    #print ( ('pass', (minx, miny, maxx, maxy)) )
                    return
                # in bounds of a new box            
                self.draw_highlight_menu_item(lindex)
                self.draw_carrot_menu_item(lindex)
                self.highlighted_item = lindex


def menu_controller(panel, event):
    """ pass in game loop events and this should parse/route them.
    has to be a function outside of ContextMenu class, because it creates/destroys instances of panel."""
    if event.type == pygame.MOUSEBUTTONUP:
        # prints on the console the button released and its position at that moment
        print( u'button {} released in the position {}'.format(event.button, event.pos) )
        if event.button == 3: # right click -- creates a new menu
            if panel:
                panel.close()
                panel = None
            panel = ContextMenu(screen, event.pos, menu, FONT20)                
        if event.button == 1: # left click chooses option, or erases menu.
            if panel != None:
                if panel.events_map:
                    action = panel.check_menu_events(event.pos)
                    if action:                    
                        action() # menus have the functions they call
                        panel.close()
                        panel = None
                    else: # left click anywhere else cancels the right-click ContextMenu.
                        panel.close()
                        panel = None
    if panel: # and panel.this.get_rect().collidepoint(pygame.mouse.get_pos()):
        #mouseover_highlight(panel)
        panel.mouseover_highlight()
        

# GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONUP:
            # prints on the console the button released and its position at that moment
            print( u'button {} released in the position {}'.format(event.button, event.pos) )
            if event.button == 3: # right click
                if panel:
                    panel.close()
                    panel = None
                panel = ContextMenu(screen, event.pos, menu, FONT20)                
            if event.button == 1:
                if panel != None:
                    if panel.events_map:
                        action = panel.check_menu_events(event.pos)
                        if action:                    
                            action()
                            panel.close()
                            panel = None
                        else: # left click anywhere else cancels the right-click ContextMenu.
                            panel.close()
                            panel = None

        if panel: # and panel.this.get_rect().collidepoint(pygame.mouse.get_pos()):
            #mouseover_highlight(panel)
            panel.mouseover_highlight()

    # systems_test
    clock.tick() # slow it to 30 FPS

pygame.quit()
