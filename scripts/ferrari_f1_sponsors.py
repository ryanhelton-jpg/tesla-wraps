#!/usr/bin/env python3
"""
Ferrari F1 Livery with Sponsor Logos
"""

from PIL import Image, ImageDraw
import os

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), '..', 'templates', 'modely-2025-premium', 'template.png')
ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'skins')

# Official Scuderia Ferrari F1 colors
FERRARI_RED = (239, 26, 45, 255)
FERRARI_YELLOW = (255, 242, 0, 255)
FERRARI_BLACK = (0, 0, 0, 255)
FERRARI_WHITE = (255, 255, 255, 255)


def load_template():
    return Image.open(TEMPLATE_PATH).convert('RGBA')


def load_and_process_logos():
    """Load and separate the sponsor logos."""
    sponsors_img = Image.open(os.path.join(ASSETS_DIR, 'sponsors.jpg')).convert('RGBA')
    ferrari_shield = Image.open(os.path.join(ASSETS_DIR, 'ferrari_shield.jpg')).convert('RGBA')
    
    # The sponsors image has Vodafone on left, Shell on right
    # Let's crop them out
    w, h = sponsors_img.size
    
    # Vodafone is roughly left half
    vodafone = sponsors_img.crop((0, 0, w//2, h))
    
    # Shell is roughly right half  
    shell = sponsors_img.crop((w//2, 0, w, h))
    
    return vodafone, shell, ferrari_shield


def remove_background(img, bg_color=(255, 0, 0), threshold=60):
    """Remove background color from image, making it transparent."""
    img = img.convert('RGBA')
    data = img.getdata()
    
    new_data = []
    for item in data:
        r, g, b, a = item
        # Check if pixel is close to background color
        if (abs(r - bg_color[0]) < threshold and 
            abs(g - bg_color[1]) < threshold and 
            abs(b - bg_color[2]) < threshold):
            new_data.append((255, 255, 255, 0))  # Transparent
        else:
            new_data.append(item)
    
    img.putdata(new_data)
    return img


def create_ferrari_f1_sponsored(output_name='Ferrari_F1_Sponsored'):
    """Create Ferrari F1 wrap with sponsor logos."""
    template = load_template()
    width, height = template.size
    
    # Load logos
    vodafone, shell, ferrari_shield = load_and_process_logos()
    
    # Create base Ferrari red wrap
    result = Image.new('RGBA', (width, height), FERRARI_RED)
    draw = ImageDraw.Draw(result)
    
    # Add black lower section
    for y in range(int(height * 0.75), height):
        ratio = (y - height * 0.75) / (height * 0.25)
        alpha = int(200 * ratio)
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
    
    # Add yellow accent stripe
    draw.rectangle([0, int(height * 0.42), width, int(height * 0.44)], fill=FERRARI_YELLOW)
    
    # Process and place Ferrari shield on the hood area (center-top)
    # Remove white/light background from shield
    ferrari_shield_clean = remove_background(ferrari_shield, bg_color=(255, 255, 255), threshold=40)
    shield_size = (80, 100)
    ferrari_shield_resized = ferrari_shield_clean.resize(shield_size, Image.Resampling.LANCZOS)
    
    # Place shield on hood (center of image, upper area)
    shield_x = (width - shield_size[0]) // 2
    shield_y = int(height * 0.05)
    result.paste(ferrari_shield_resized, (shield_x, shield_y), ferrari_shield_resized)
    
    # Process Shell logo - remove red background
    shell_clean = remove_background(shell, bg_color=(239, 26, 45), threshold=80)
    shell_clean = remove_background(shell_clean, bg_color=(255, 0, 0), threshold=80)
    shell_size = (70, 70)
    shell_resized = shell_clean.resize(shell_size, Image.Resampling.LANCZOS)
    
    # Place Shell logos on sides (like sidepods)
    # Left side
    result.paste(shell_resized, (int(width * 0.08), int(height * 0.5)), shell_resized)
    # Right side
    result.paste(shell_resized, (int(width * 0.82), int(height * 0.5)), shell_resized)
    
    # Process Vodafone logo - remove red background
    vodafone_clean = remove_background(vodafone, bg_color=(239, 26, 45), threshold=80)
    vodafone_clean = remove_background(vodafone_clean, bg_color=(255, 0, 0), threshold=80)
    vodafone_size = (90, 60)
    vodafone_resized = vodafone_clean.resize(vodafone_size, Image.Resampling.LANCZOS)
    
    # Place Vodafone on rear area
    vodafone_x = (width - vodafone_size[0]) // 2
    result.paste(vodafone_resized, (vodafone_x, int(height * 0.82)), vodafone_resized)
    
    # Also add smaller Shell on front bumper area
    small_shell = shell_clean.resize((50, 50), Image.Resampling.LANCZOS)
    result.paste(small_shell, (int(width * 0.45), int(height * 0.25)), small_shell)
    
    # Mask with template
    final = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    final.paste(result, mask=template.convert('L'))
    
    output_path = os.path.join(OUTPUT_DIR, f'{output_name}.png')
    final.save(output_path, 'PNG')
    print(f'Created: {output_path}')
    return output_path


def create_ferrari_f1_sponsored_v2(output_name='Ferrari_F1_Sponsored_v2'):
    """Alternative layout - more aggressive styling."""
    template = load_template()
    width, height = template.size
    
    vodafone, shell, ferrari_shield = load_and_process_logos()
    
    # Base with gradient
    result = Image.new('RGBA', (width, height), FERRARI_RED)
    draw = ImageDraw.Draw(result)
    
    # Black angular sections on sides (like modern F1)
    points_left = [(0, height * 0.35), (width * 0.3, height * 0.45), 
                   (width * 0.3, height * 0.85), (0, height * 0.95)]
    draw.polygon(points_left, fill=FERRARI_BLACK)
    
    points_right = [(width, height * 0.35), (width * 0.7, height * 0.45),
                    (width * 0.7, height * 0.85), (width, height * 0.95)]
    draw.polygon(points_right, fill=FERRARI_BLACK)
    
    # Yellow racing stripe through center
    draw.rectangle([width * 0.47, 0, width * 0.53, height], fill=FERRARI_YELLOW)
    
    # Process logos
    ferrari_shield_clean = remove_background(ferrari_shield, bg_color=(255, 255, 255), threshold=40)
    shell_clean = remove_background(shell, bg_color=(255, 0, 0), threshold=80)
    shell_clean = remove_background(shell_clean, bg_color=(239, 26, 45), threshold=80)
    vodafone_clean = remove_background(vodafone, bg_color=(255, 0, 0), threshold=80)
    vodafone_clean = remove_background(vodafone_clean, bg_color=(239, 26, 45), threshold=80)
    
    # Place Ferrari shield - larger, on hood
    shield_size = (100, 120)
    ferrari_shield_resized = ferrari_shield_clean.resize(shield_size, Image.Resampling.LANCZOS)
    shield_x = (width - shield_size[0]) // 2
    result.paste(ferrari_shield_resized, (shield_x, int(height * 0.02)), ferrari_shield_resized)
    
    # Shell logos on black sidepods
    shell_size = (60, 60)
    shell_resized = shell_clean.resize(shell_size, Image.Resampling.LANCZOS)
    result.paste(shell_resized, (int(width * 0.05), int(height * 0.55)), shell_resized)
    result.paste(shell_resized, (int(width * 0.85), int(height * 0.55)), shell_resized)
    
    # Vodafone on rear
    vodafone_size = (80, 55)
    vodafone_resized = vodafone_clean.resize(vodafone_size, Image.Resampling.LANCZOS)
    result.paste(vodafone_resized, ((width - vodafone_size[0]) // 2, int(height * 0.88)), vodafone_resized)
    
    # Mask with template
    final = Image.new('RGBA', (width, height), (255, 255, 255, 255))
    final.paste(result, mask=template.convert('L'))
    
    output_path = os.path.join(OUTPUT_DIR, f'{output_name}.png')
    final.save(output_path, 'PNG')
    print(f'Created: {output_path}')
    return output_path


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("Generating Ferrari F1 skins with sponsors...")
    create_ferrari_f1_sponsored()
    create_ferrari_f1_sponsored_v2()
    print("\nDone!")
