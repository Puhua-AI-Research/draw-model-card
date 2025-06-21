import os
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageOps


def create_model_card(
    background_path: str,
    logo_path: str,
    title: str,
    output_path: str,
    circle_center_x: int = 140,
    circle_radius: int = 100,
    logo_border_width: int = 0,
    logo_border_color: str = "white",
    logo_bg_color: str = None,
    title_position_x: int = 300,
    title_font_size: int = 70,
    title_font_weight: str = "normal",
    font_path: str = None,
):
    """
    Creates a model card image by pasting a logo into a circle on a background image and adding a title.

    Args:
        background_path (str): Path to the background image.
        logo_path (str): Path to the logo image.
        title (str): The title text to add.
        output_path (str): Path to save the resulting image.
        circle_center_x (int): The x-coordinate of the center of the circle for the logo.
        circle_radius (int): The radius of the circle for the logo.
        logo_border_width (int): The width of the border around the logo.
        logo_border_color (str): The color of the border around the logo.
        logo_bg_color (str, optional): The background color of the logo circle. Defaults to None (transparent).
        title_position_x (int): The x-coordinate for the title's starting position.
        title_font_size (int): The font size for the title.
        title_font_weight (str): The font weight for the title ('normal' or 'bold').
        font_path (str): Optional path to a .ttf font file.
    """
    # Load background image
    try:
        background = Image.open(background_path).convert("RGBA")
    except FileNotFoundError:
        print(f"Error: Background image not found at {background_path}")
        return

    # Load logo image
    try:
        logo = Image.open(logo_path).convert("RGBA")
    except FileNotFoundError:
        print(f"Error: Logo image not found at {logo_path}")
        return

    # --- Logo Processing ---
    # Create a new canvas for the final circular logo.
    final_logo_size = (circle_radius * 2, circle_radius * 2)
    final_logo_canvas = Image.new("RGBA", final_logo_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(final_logo_canvas)

    # Draw the background circle fill
    if logo_bg_color:
        draw.ellipse((0, 0) + final_logo_size, fill=logo_bg_color)

    # Process logo to fit perfectly in circle
    logo_for_sizing = logo.copy()
    
    # For square or near-square logos, crop to square first
    logo_width, logo_height = logo_for_sizing.size
    min_dimension = min(logo_width, logo_height)
    
    # Crop to center square if not already square
    if logo_width != logo_height:
        left = (logo_width - min_dimension) // 2
        top = (logo_height - min_dimension) // 2
        right = left + min_dimension
        bottom = top + min_dimension
        logo_for_sizing = logo_for_sizing.crop((left, top, right, bottom))
    
    # Resize the square logo to fit the circle perfectly
    logo_for_sizing = logo_for_sizing.resize(final_logo_size, Image.Resampling.LANCZOS)
    
    # Create a white background for the logo to avoid transparency issues
    white_bg = Image.new("RGBA", final_logo_size, (255, 255, 255, 255))
    if logo_for_sizing.mode == "RGBA":
        # Composite logo onto white background to handle transparency
        white_bg.paste(logo_for_sizing, (0, 0), logo_for_sizing)
    else:
        # If logo doesn't have alpha channel, paste directly
        white_bg.paste(logo_for_sizing, (0, 0))
    logo_for_sizing = white_bg
    
    # Create circular mask
    mask = Image.new("L", final_logo_size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0) + final_logo_size, fill=255)
    
    # Create final circular logo with white background
    circular_logo = Image.new("RGBA", final_logo_size, (0, 0, 0, 0))
    circular_logo.paste(logo_for_sizing, (0, 0))
    circular_logo.putalpha(mask)
    
    # Paste the circular logo onto the canvas (which already has white background if specified)
    final_logo_canvas.paste(circular_logo, (0, 0), circular_logo)

    # Draw the border on top
    if logo_border_width > 0:
        border_box = (0, 0) + final_logo_size
        draw.ellipse(border_box, outline=logo_border_color, width=logo_border_width)

    # --- Pasting Logo ---
    # Calculate logo position (top-left corner)
    paste_x = circle_center_x - circle_radius
    paste_y = background.height // 2 - circle_radius

    # Composite the final logo canvas onto the background
    background.paste(final_logo_canvas, (paste_x, paste_y), final_logo_canvas)

    # --- Text Drawing ---
    draw = ImageDraw.Draw(background)

    # Load font
    try:
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, title_font_size)
        else:
            # Fallback to common fonts
            if title_font_weight == "bold":
                font_names = [
                    "arialbd.ttf",
                    "Arial Bold.ttf",
                    "DejaVuSans-Bold.ttf",
                    "arial.ttf",
                    "DejaVuSans.ttf",
                ]
            else:
                font_names = ["arial.ttf", "DejaVuSans.ttf"]

            font = None
            for name in font_names:
                try:
                    font = ImageFont.truetype(name, title_font_size)
                    break
                except IOError:
                    continue

            if not font:
                if title_font_weight == "bold":
                    print("Common bold fonts not found. Using default font.")
                else:
                    print("Common fonts not found. Using default font.")
                font = ImageFont.load_default()
    except Exception as e:
        print(f"Error loading font: {e}")
        font = ImageFont.load_default()

    # Calculate text position for perfect vertical centering
    # Use textbbox for more accurate text measurements
    if hasattr(draw, "textbbox"):
        # textbbox returns (left, top, right, bottom) relative to the text position
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        # For proper vertical centering, we need to consider the actual text bounds
        # bbox[1] is the top offset (often negative for ascenders)
        # bbox[3] is the bottom offset (positive for descenders)
        text_top = bbox[1]
        text_bottom = bbox[3]
        text_height = text_bottom - text_top
        
        # Calculate the center position considering the text's actual bounds
        title_position_y = background.height // 2 - text_height // 2 - text_top
    else:
        # Fallback for older PIL versions
        try:
            text_width, text_height = draw.textsize(title, font=font)
            title_position_y = background.height // 2 - text_height // 2
        except AttributeError:
            # If textsize is also not available, use font metrics
            if hasattr(font, "getbbox"):
                bbox = font.getbbox(title)
                text_height = bbox[3] - bbox[1]
                title_position_y = background.height // 2 - text_height // 2
            else:
                # Ultimate fallback - approximate positioning
                title_position_y = background.height // 2 - title_font_size // 2

    # Draw title
    draw.text((title_position_x, title_position_y), title, font=font, fill="black")

    # Save the final image
    # Convert back to RGB if saving as JPEG
    if output_path.lower().endswith((".jpg", ".jpeg")):
        background = background.convert("RGB")

    background.save(output_path)
    print(f"Image saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Create a model card image with logo and title",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python draw-model.py --title "My Model" --background bg.png --logo logo.png
  python draw-model.py --title "Qwen Model" --background bg.png --logo qwen.png --circle-radius 50
  python draw-model.py --title "GPT Model" --background bg.png --logo gpt.png --title-font-size 60 --bold
        """
    )
    
    # Required arguments
    parser.add_argument("--title", "-t", required=True, help="Title text for the model card")
    parser.add_argument("--background", "-b", required=True, help="Path to background image")
    parser.add_argument("--logo", "-l", required=True, help="Path to logo image")
    
    # Optional arguments with default values
    parser.add_argument("--output", "-o", help="Output file path (default: title.png)")
    parser.add_argument("--circle-center-x", type=int, default=83, help="X coordinate of circle center (default: 83)")
    parser.add_argument("--circle-radius", type=int, default=45, help="Radius of logo circle (default: 45)")
    parser.add_argument("--logo-border-width", type=int, default=0, help="Width of logo border (default: 0)")
    parser.add_argument("--logo-border-color", default="white", help="Color of logo border (default: white)")
    parser.add_argument("--logo-bg-color", default="white", help="Background color of logo circle (default: white)")
    parser.add_argument("--title-position-x", type=int, help="X position of title (default: circle_center_x + circle_radius + 50)")
    parser.add_argument("--title-font-size", type=int, default=50, help="Font size of title (default: 50)")
    parser.add_argument("--font-path", help="Path to custom font file (.ttf)")
    
    args = parser.parse_args()
    
    # Set default output filename based on title
    if not args.output:
        # Clean title for filename (remove special characters, replace spaces with underscores)
        clean_title = "".join(c for c in args.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_title = clean_title.replace(' ', '_')
        args.output = f"./results/{clean_title}.png"
    
    # Set default title position if not specified
    if not args.title_position_x:
        args.title_position_x = args.circle_center_x + args.circle_radius + 30
    
    # Set font weight
    title_font_weight = "bold"
    
    # Check if input files exist
    if not os.path.exists(args.background):
        print(f"Error: Background image '{args.background}' not found.")
        return 1
    elif not os.path.exists(args.logo):
        print(f"Error: Logo image '{args.logo}' not found.")
        return 1
    
    # Create the model card
    create_model_card(
        background_path=args.background,
        logo_path=args.logo,
        title=args.title,
        output_path=args.output,
        circle_center_x=args.circle_center_x,
        circle_radius=args.circle_radius,
        logo_border_width=args.logo_border_width,
        logo_border_color=args.logo_border_color,
        logo_bg_color=args.logo_bg_color,
        title_position_x=args.title_position_x,
        title_font_size=args.title_font_size,
        title_font_weight=title_font_weight,
        font_path=args.font_path,
    )
    
    return 0


if __name__ == "__main__":
    exit(main())
