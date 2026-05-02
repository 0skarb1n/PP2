import pygame
from collections import deque

def draw_pencil(surface, start, end, color, size):
    pygame.draw.line(surface, color, start, end, size)

def draw_line(surface, start, end, color, size):
    pygame.draw.line(surface, color, start, end, size)

def draw_rectangle(surface, start, end, color, size):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(end[0] - start[0])
    h = abs(end[1] - start[1])
    pygame.draw.rect(surface, color, (x, y, w, h), size)

def draw_circle(surface, start, end, color, size):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    r = int(((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5 // 2)
    if r > 0:
        pygame.draw.circle(surface, color, (cx, cy), r, size)

def draw_right_triangle(surface, start, end, color, size):
    p1 = start
    p2 = (start[0], end[1])
    p3 = end
    pygame.draw.polygon(surface, color, [p1, p2, p3], size)

def draw_rhombus(surface, start, end, color, size):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    p1 = (cx, start[1])
    p2 = (end[0], cy)
    p3 = (cx, end[1])
    p4 = (start[0], cy)
    pygame.draw.polygon(surface, color, [p1, p2, p3, p4], size)

def flood_fill(surface, pos, fill_color):
    x, y = pos
    w, h = surface.get_size()
    if x < 0 or x >= w or y < 0 or y >= h:
        return
    target_color = surface.get_at((x, y))[:3]
    if target_color == fill_color[:3]:
        return
    queue = deque()
    queue.append((x, y))
    visited = set()
    visited.add((x, y))
    while queue:
        cx, cy = queue.popleft()
        if surface.get_at((cx, cy))[:3] != target_color:
            continue
        surface.set_at((cx, cy), fill_color)
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = cx+dx, cy+dy
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))