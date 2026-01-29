#!/usr/bin/env python3
"""
Tesla Model Y Wrap Skin Generator

Generates custom wrap skins by filling the template with colors, gradients, or patterns.
"""

from PIL import Image, ImageDraw
import os
import sys
import math
import random

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'templates', 'modely-2025-premium', 'template.png')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'skins')


def load_template():
    """Load the template and create a mask from it."""
    template = Image.open(TEMPLATE_PATH).convert('RGBA')
    # The template has black lines on white - we want to fill the white areas
    return template


def create_solid_color(color, output_name):
    """Create a solid color wrap."""
    template = load_template()
    width, height = template.size
    
    # Create a new image with the solid color
    result = Image.new('RGBA', (width, height), color)
    
    # Composite with template to preserve the panel outlines
    # The template white areas become our color, black lines stay
    result = Image.composite(result, template, template.split()[0])
    
    output_path = os.path.join(OUTPUT_DIR, f'{output_name}.png')
    result.save(output_path, 'PNG')
    print(f'Created: {output_path}')
    return output_path


def create_gradient(color1, color2, direction='vertical', output_name='gradient'):
    """Create a gradient wrap (vertical or horizontal)."""
    template = load_template()
    width, height = template.size
    
    gradient = Image.new('RGBA', (width, height))
    draw = ImageDraw.Draw(gradient)
    
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    
    if direction == 'vertical':
        for y in range(height):
            ratio = y / height
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
    else:  # horizontal
        for x in range(width):
            ratio = x / width
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            draw.line([(x, 0), (x, height)], fill=(r, g, b, 255))
    
    # Mask with template
    result = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    result.paste(gradient, mask=template.convert('L'))
    
    output_path = os.path.join(OUTPUT_DIR, f'{output_name}.png')
    result.save(output_path, 'PNG')
    print(f'Created: {output_path}')
    return output_path


def create_stripes(colors, stripe_width=50, direction='horizontal', output_name='stripes'):
    """Create a striped wrap."""
    template = load_template()
    width, height = template.size
    
    stripes = Image.new('RGBA', (width, height))
    draw = ImageDraw.Draw(stripes)
    
    if direction == 'horizontal':
        for y in range(0, height, stripe_width):
            color_idx = (y // stripe_width) % len(colors)
            draw.rectangle([(0, y), (width, y + stripe_width)], fill=colors[color_idx])
    else:  # vertical
        for x in range(0, width, stripe_width):
            color_idx = (x // stripe_width) % len(colors)
            draw.rectangle([(x, 0), (x + stripe_width, height)], fill=colors[color_idx])
    
    # Mask with template
    result = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    result.paste(stripes, mask=template.convert('L'))
    
    output_path = os.path.join(OUTPUT_DIR, f'{output_name}.png')
    result.save(output_path, 'PNG')
    print(f'Created: {output_path}')
    return output_path


def create_carbon_fiber(output_name='carbon_fiber'):
    """Create a carbon fiber pattern wrap."""
    template = load_template()
    width, height = template.size
    
    pattern = Image.new('RGBA', (width, height), (30, 30, 30, 255))
    draw = ImageDraw.Draw(pattern)
    
    # Create diagonal weave pattern
    for i in range(-height, width + height, 8):
        draw.line([(i, 0), (i + height, height)], fill=(50, 50, 50, 255), width=2)
        draw.line([(i + 4, 0), (i + 4 + height, height)], fill=(20, 20, 20, 255), width=2)
    
    for i in range(-height, width + height, 8):
        draw.line([(i + height, 0), (i, height)], fill=(40, 40, 40, 255), width=2)
    
    # Mask with template
    result = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    result.paste(pattern, mask=template.convert('L'))
    
    output_path = os.path.join(OUTPUT_DIR, f'{output_name}.png')
    result.save(output_path, 'PNG')
    print(f'Created: {output_path}')
    return output_path


def create_matte_black(output_name='matte_black'):
    """Create a matte black wrap."""
    return create_solid_color((25, 25, 25, 255), output_name)


def create_racing_stripes(base_color, stripe_color, output_name='racing_stripes'):
    """Create a wrap with racing stripes down the center."""
    template = load_template()
    width, height = template.size
    
    result = Image.new('RGBA', (width, height), base_color)
    draw = ImageDraw.Draw(result)
    
    # Draw center racing stripes
    center = width // 2
    stripe_width = 30
    gap = 10
    
    draw.rectangle([center - stripe_width - gap//2, 0, center - gap//2, height], fill=stripe_color)
    draw.rectangle([center + gap//2, 0, center + stripe_width + gap//2, height], fill=stripe_color)
    
    # Mask with template
    final = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    final.paste(result, mask=template.convert('L'))
    
    output_path = os.path.join(OUTPUT_DIR, f'{output_name}.png')
    final.save(output_path, 'PNG')
    print(f'Created: {output_path}')
    return output_path


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate some sample skins
    print("Generating sample skins...")
    
    create_matte_black()
    create_carbon_fiber()
    create_gradient((0, 100, 200), (100, 0, 150), 'vertical', 'blue_purple_gradient')
    create_gradient((200, 50, 50), (50, 50, 50), 'vertical', 'red_fade')
    create_stripes([(255, 0, 0, 255), (255, 255, 255, 255), (0, 0, 255, 255)], 60, 'horizontal', 'usa_stripes')
    create_racing_stripes((30, 30, 30, 255), (255, 255, 255, 255), 'racing_stripes_white')
    create_racing_stripes((255, 255, 255, 255), (255, 0, 0, 255), 'racing_stripes_red')
    
    print("\nDone! Skins saved to skins/ folder")
