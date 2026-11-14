import math
import pygame
import auth

# Initialize Pygame and set up the window
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Clicker")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 64)

# Create a login/signup screen and get the userna
#username = auth.run_login(screen, clock)
#if username is None:     
#    pygame.quit()
#    raise SystemExit
#pygame.display.set_caption(f"Space Idle - {username}")


# Initialize game variables
score = 0
center = (400, 300)
radius = 100
currency_per_click = 1
upgrade_cost = 10
upgrade_idle_cost = 10
level = 1
idle_rate = 0


# Used to create the buttons for updates and tabs
upgrade_rect = pygame.Rect(50, 450, 200, 60)
upgrade_idle_rect = pygame.Rect(50, 600, 200, 60)

tab1_rect = pygame.Rect(800, 100, 200, 60)
tab2_rect = pygame.Rect(800, 200, 200, 60)
tab3_rect = pygame.Rect(800, 300, 200, 60)

tab4_rect = pygame.Rect(800, 400, 200, 60)
tab5_rect = pygame.Rect(800, 500, 200, 60)
tab6_rect = pygame.Rect(800, 600, 200, 60)




class Space_Idle:
    def __init__(self, name):
        
        self.name = name;
        self.curency = 0
        self.isGameOn = False
        self.tabvalue = 0

        self.currency_per_click = 1

        self.upgrade_cost = 10
        self.upgrade_idle_cost = 10

        self.idle_rate = 0

    def Run(self, IsGameRunning):
        self.isGameOn = IsGameRunning

        while self.isGameOn:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.isGameOn = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        
                        mx, my = event.pos
                        # Check if the click is inside the circle
                        if math.hypot(mx - center[0], my - center[1]) <= radius and self.tabvalue == 0:
                             self.curency += self.currency_per_click
            
                            # Check if the click is inside the upgrade button
                        elif upgrade_rect.collidepoint(event.pos) and self.tabvalue == 1:
                            if  self.curency >= self.upgrade_cost:
                                self.curency -= self.upgrade_cost
                                self.currency_per_click += 1
                                self.upgrade_cost *= 2
            
                        elif upgrade_idle_rect.collidepoint(event.pos) and self.tabvalue == 1:
                            if  self.curency >= self.upgrade_idle_cost:
                                self.curency -= self.upgrade_idle_cost
                                idle_rate += 1   
                                level += 1
                                self.upgrade_idle_cost *= 2
            
                        elif tab1_rect.collidepoint(event.pos):
                            self.tabvalue = 0
            
                        elif tab2_rect.collidepoint(event.pos):
                            self.tabvalue = 1  
            
                        elif tab3_rect.collidepoint(event.pos):
                            self.tabvalue = 2    
            
                        elif tab4_rect.collidepoint(event.pos):
                            self.tabvalue = 3
            
                        elif tab5_rect.collidepoint(event.pos):
                            self.tabvalue = 4
                            
                        elif tab6_rect.collidepoint(event.pos):
                            self.tabvalue = 5 
                            
                    # Update the game state based on the current tab
        
                if self.tabvalue == 0:
                      
                    screen.fill((10, 10, 30))
            
                    # Draw the circle and score
                    pygame.draw.circle(screen, (80, 140, 255), center, radius)
                    text = font.render(f"Score: {int(self.curency)}", True, (255, 255, 255))
                    screen.blit(text, (400 - text.get_width() // 2, 100))
            
                elif self.tabvalue == 1:
                  
                    screen.fill((10, 10, 30))
            
                    upgrades_text = font.render("Upgrades", True, (255, 255, 255))
                    screen.blit(upgrades_text, (400 - upgrades_text.get_width() // 2, 100))
            
                    # Draw the upgrade buttons
                    pygame.draw.rect(screen, (70, 70, 200), upgrade_rect)
                    uprade_text = font.render(f"Upgrade ({self.upgrade_cost})", True, (255, 255, 255))
                    screen.blit(uprade_text, (upgrade_rect.x + 10, upgrade_rect.y + 10))
            
                    # Draw the idle upgrade button
                    pygame.draw.rect(screen, (100, 100, 255), upgrade_idle_rect)
                    idle_text = font.render(f"Upgrade (Idle) ({self.upgrade_idle_cost})", True, (255, 255, 255))
                    screen.blit(idle_text, (upgrade_idle_rect.x + 10, upgrade_idle_rect.y + 10))
            
                elif self.tabvalue == 2:
                        
                    screen.fill((10, 10, 30))
            
                    # Draw the settings text
                    achievements_text = font.render("Achievments/Milestones", True, (255, 255, 255))
                    screen.blit(achievements_text, (400 - achievements_text.get_width() // 2, 100))
            
                elif self.tabvalue == 3:
            
                    screen.fill((10, 10, 30))
            
                    # Draw the settings text
                    account_text = font.render("Account", True, (255, 255, 255))
                    screen.blit(account_text, (400 - account_text.get_width() // 2, 100))
                        
                elif self.tabvalue == 4:
            
                    screen.fill((10, 10, 30))
            
                     # Draw the settings text
                    setting_text = font.render("Settings", True, (255, 255, 255))
                    screen.blit(setting_text, (400 - setting_text.get_width() // 2, 100))           
            
                elif self.tabvalue == 5:
            
                    screen.fill((10, 10, 30))
            
                    # Draw the settings text
                    Statiscs_text = font.render("Statistics", True, (255, 255, 255))
                    screen.blit(Statiscs_text, (400 - Statiscs_text.get_width() // 2, 100))  

                dt = clock.tick(60) / 1000   # the / 1000 is the important part
                self.curency += self.idle_rate * dt  # Add the idle rate to the score based on the time elapsed

                #Draw the tabs
                pygame.draw.rect(screen, (70, 70, 200), tab1_rect)
                tab1_text = font.render("Player", True, (255, 255, 255))
                screen.blit(tab1_text, (tab1_rect.x + 10, tab1_rect.y + 10))

                pygame.draw.rect(screen, (70, 70, 200), tab2_rect)
                tab2_text = font.render("Shop", True, (255, 255, 255))
                screen.blit(tab2_text, (tab2_rect.x + 10, tab2_rect.y + 10))

                pygame.draw.rect(screen, (70, 70, 200), tab3_rect)
                tab3_text = font.render("Achievments", True, (255, 255, 255))
                screen.blit(tab3_text, (tab3_rect.x + 10, tab3_rect.y + 10))

                pygame.draw.rect(screen, (70, 70, 200), tab4_rect)
                tab1_text = font.render("Account", True, (255, 255, 255))
                screen.blit(tab1_text, (tab4_rect.x + 10, tab4_rect.y + 10))

                pygame.draw.rect(screen, (70, 70, 200), tab5_rect)
                tab2_text = font.render("Setting", True, (255, 255, 255))
                screen.blit(tab2_text, (tab5_rect.x + 10, tab5_rect.y + 10))

                pygame.draw.rect(screen, (70, 70, 200), tab6_rect)
                tab3_text = font.render("Statistics", True, (255, 255, 255))
                screen.blit(tab3_text, (tab6_rect.x + 10, tab6_rect.y + 10))

                # Update the display and tick the clock
                pygame.display.flip()
                clock.tick(60)


# Set up the main game loop

SpaceIdleGame = Space_Idle("spaceIdle")
SpaceIdleGame.Run(True)


pygame.quit()