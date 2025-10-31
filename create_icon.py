#!/usr/bin/env python3
"""
Utility script to convert PNG logo to ICO format for Windows executable.
"""

from pathlib import Path
try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is required. Install it with: pip install Pillow")
    exit(1)

def create_ico():
    """Convert PNG logo to ICO format."""
    script_dir = Path(__file__).parent.resolve()
    png_path = script_dir / "assets" / "logo_x1.png"
    ico_path = script_dir / "assets" / "logo_x1.ico"
    
    if not png_path.exists():
        print(f"Error: {png_path} not found!")
        return False
    
    try:
        # Open PNG image
        img = Image.open(png_path)
        
        # Convert to RGBA if not already (for transparency support)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # ICO format typically includes multiple sizes for better Windows compatibility
        # Windows uses sizes like 16x16, 32x32, 48x48, 256x256
        # Create multiple sizes from the original image
        ico_sizes = [(16, 16), (32, 32), (48, 48), (256, 256)]
        original_width, original_height = img.size
        
        # Create a list of images at different sizes
        ico_images = []
        for width, height in ico_sizes:
            if original_width >= width and original_height >= height:
                resized = img.resize((width, height), Image.Resampling.LANCZOS)
                ico_images.append(resized)
        
        # Add the original if it's a reasonable size (not too large)
        if original_width <= 512 and original_height <= 512:
            ico_images.append(img)
        
        # Save as ICO with multiple sizes
        # Pillow supports saving ICO with multiple sizes using a list of images
        if len(ico_images) > 1:
            # Save the largest image with sizes parameter
            largest = ico_images[-1]
            largest.save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in ico_images])
        else:
            # Fallback: save single image
            img.save(ico_path, format='ICO')
        
        # Verify the file was created and has reasonable size
        if ico_path.exists() and ico_path.stat().st_size > 100:
            print(f"✓ Successfully created {ico_path} ({ico_path.stat().st_size} bytes)")
            return True
        else:
            print(f"Error: ICO file creation failed or file is too small")
            return False
    except Exception as e:
        print(f"Error converting to ICO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_ico()
    exit(0 if success else 1)

