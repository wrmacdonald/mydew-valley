import pygame
from settings import *
from spritesheet import SpriteSheet


class Overlay:
    def __init__(self, player):
        """HUD for user to show selected seed/tool"""
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # import images & convert to surfaces
        ss_path = '../art/objects_ss.png'
        objects_ss = SpriteSheet(ss_path)
        ss_tool_coords = {
            'hoe': (0, 0, 52, 60),
            'water': (52, 0, 64, 40)
        }
        self.tools_surf = {tool: objects_ss.image_at(ss_tool_coords[tool]) for tool in player.tools}
        ss_seed_coords = {
            'corn': (48, 60, 56, 56),
            'tomato': (0, 60, 52, 48)
        }
        self.seeds_surf = {seed: objects_ss.image_at(ss_seed_coords[seed]) for seed in player.seeds}

    def display(self):
        # show selected tool
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom=OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf, tool_rect)

        # show selected seed
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom=OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surf, seed_rect)

