import pygame

def fade_to(screen: pygame.Surface, color: tuple[int,int,int], duration: int = 1000):   # duration in ms
    '''Fades to a solid color and then back to transparent.'''
    overlay = pygame.Surface(screen.get_size()).convert_alpha()
    clock = pygame.time.Clock()
    steps = 30
    delay = duration // (steps * 2)
    r,g,b = color

    for alpha in range(256):
        pygame.event.pump()
        overlay.fill((r,g,b,alpha))
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(1000 // delay)

    pygame.time.delay(delay)

    for alpha in range(255, -1, -1):
        pygame.event.pump()
        overlay.fill((r,g,b,alpha))
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(1000 // delay)
