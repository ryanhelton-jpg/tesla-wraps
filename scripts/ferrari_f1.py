#!/usr/bin/env python3
"""
Ferrari F1 Livery Generator for Tesla Model Y
"""

from PIL import Image, ImageDraw
import os

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'templates', 'modely-2025-premium', 'template.png')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'skins')

# Official Scuderia Ferrari F1 colors
FERRARI_RED = (239, 26, 45, 255)      # #EF1A2D - Rosso Corsa
FERRARI_YELLOW = (255, 242, 0, 255)   # #FFF200
FERRARI_BLACK = (0, 0, 0, 255)        # #000000
FERRARI_WHITE = (255, 255, 255, 255)  # #FFFFFF
FERRARI_GREEN = (0, 165, 81, 255)     # #00A551 - Italian flag green


def load_template():
    return Image.open(TEMPLATE_PATH).convert('RGBA')


def create_ferrari_f1_classic(output_name='Ferrari_F1_Classic'):
    """Classic Ferrari F1 - dominant red with black accents and Italian flag stripe."""
    template = load_template()
    width, height = template.size
    
    # Create base red
    result = Image.new('RGBA', (width, height), FERRARI_RED)
    draw = ImageDraw.Draw(result)
    
    # Add black lower section (gradient fade)
    for y in range(int(height * 0.7), height):
        ratio = (y - height * 0.7) / (height * 0.3)
        alpha = int(255 * ratio * 0.8)
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
    
    # Italian flag stripe across the top (thin horizontal stripe)
    stripe_height = 15
    stripe_y = int(height * 0.15)
    draw.rectangle([0, stripe_y, width, stripe_y + stripe_height], fill=FERRARI_GREEN)
    draw.rectangle([0, stripe_y + stripe_height, width, stripe_y + stripe_height * 2], fill=FERRARI_WHITE)
    draw.rectangle([0, stripe_y + stripe_height * 2, width, stripe_y + stripe_height * 3], fill=FERRARI_RED)
    
    # Yellow accent lines
    draw.rectangle([0, stripe_y - 3, width, stripe_y], fill=FERRARI_YELLOW)
    draw.rectangle([0, stripe_y + stripe_height * 3, width, stripe_y + stripe_height * 3 + 3], fill=FERRARI_YELLOW)
    
    # Mask with template
    final = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    final.paste(result, mask=template.convert('L'))
    
    output_path = os.path.join(OUTPUT_DIR, f'{output_name}.png')
    final.save(output_path, 'PNG')
    print(f'Created: {output_path}')
    return output_path


def create_ferrari_f1_modern(output_name='Ferrari_F1_Modern'):
    """Modern Ferrari F1 - red with black side pods and dynamic angles."""
    template = load_template()
    width, height = template.size
    
    result = Image.new('RGBA', (width, height), FERRARI_RED)
    draw = ImageDraw.Draw(result)
    
    # Black angular sections on sides
    # Left side black accent
    points_left = [(0, height * 0.3), (width * 0.35, height * 0.4), 
                   (width * 0.35, height * 0.8), (0, height * 0.9)]
    draw.polygon(points_left, fill=FERRARI_BLACK)
    
    # Right side black accent
    points_right = [(width, height * 0.3), (width * 0.65, height * 0.4),
                    (width * 0.65, height * 0.8), (width, height * 0.9)]
    draw.polygon(points_right, fill=FERRARI_BLACK)
    
    # Yellow racing number area (center rectangle)
    draw.rectangle([width * 0.4, height * 0.35, width * 0.6, height * 0.55], fill=FERRARI_YELLOW)
    
    # Red outline inside yellow
    draw.rectangle([width * 0.42, height * 0.37, width * 0.58, height * 0.53], fill=FERRARI_RED)
    
    # Black bottom
    draw.rectangle([0, height * 0.85, width, height], fill=FERRARI_BLACK)
    
    # Mask with template
    final = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    final.paste(result, mask=template.convert('L'))
    
    output_path = os.path.join(OUTPUT_DIR, f'{output_name}.png')
    final.save(output_path, 'PNG')
    print(f'Created: {output_path}')
    return output_path


def create_ferrari_f1_racing(output_name='Ferrari_F1_Racing'):
    """Racing Ferrari - aggressive red with yellow stripes."""
    template = load_template()
    width, height = template.size
    
    result = Image.new('RGBA', (width, height), FERRARI_RED)
    draw = ImageDraw.Draw(result)
    
    # Center yellow racing stripes
    center = width // 2
    stripe_width = 25
    gap = 8
    
    # Outer yellow stripes
    draw.rectangle([center - stripe_width * 2 - gap * 1.5, 0, 
                    center - stripe_width - gap * 1.5, height], fill=FERRARI_YELLOW)
    draw.rectangle([center + stripe_width + gap * 1.5, 0,
                    center + stripe_width * 2 + gap * 1.5, height], fill=FERRARI_YELLOW)
    
    # Inner black stripes
    draw.rectangle([center - stripe_width - gap * 0.5, 0,
                    center - gap * 0.5, height], fill=FERRARI_BLACK)
    draw.rectangle([center + gap * 0.5, 0,
                    center + stripe_width + gap * 0.5, height], fill=FERRARI_BLACK)
    
    # Mask with template
    final = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    final.paste(result, mask=template.convert('L'))
    
    output_path = os.path.join(OUTPUT_DIR, f'{output_name}.png')
    final.save(output_path, 'PNG')
    print(f'Created: {output_path}')
    return output_path


def create_ferrari_f1_gradient(output_name='Ferrari_F1_Gradient'):
    """Ferrari with dramatic dark-to-red gradient."""
    template = load_template()
    width, height = template.size
    
    gradient = Image.new('RGBA', (width, height))
    draw = ImageDraw.Draw(gradient)
    
    # Dark (almost black) at bottom, Ferrari red at top
    r1, g1, b1 = 239, 26, 45   # Ferrari red
    r2, g2, b2 = 30, 5, 8      # Very dark red/black
    
    for y in range(height):
        ratio = y / height
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    
    # Add yellow accent stripe
    draw.rectangle([0, int(height * 0.45), width, int(height * 0.47)], fill=FERRARI_YELLOW)
    
    # Mask with template
    result = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    result.paste(gradient, mask=template.convert('L'))
    
    output_path = os.path.join(OUTPUT_DIR, f'{output_name}.png')
    result.save(output_path, 'PNG')
    print(f'Created: {output_path}')
    return output_path


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Generating Ferrari F1 skins...")
    create_ferrari_f1_classic()
    create_ferrari_f1_modern()
    create_ferrari_f1_racing()
    create_ferrari_f1_gradient()
    print("\nDone! Ferrari F1 skins ready in skins/")
