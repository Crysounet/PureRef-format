import os
from purformat import PurFile, PurReader, PurWriter

def reorganize_pureref(input_file, output_file):
    """
    Read a PureRef file, reorganize its images in a grid pattern, and save as a new file.
    
    Args:
        input_file (str): Path to input .pur file
        output_file (str): Path to save the reorganized .pur file
    """
    # Read the input file
    reader = PurReader()
    with open(input_file, 'rb') as f:
        pur_file = reader.read(f.read())
    
    # Get all images
    images = pur_file.images
    if not images:
        print("No images found in PureRef file")
        return
    
    # Calculate grid dimensions
    num_images = len(images)
    grid_cols = int(num_images ** 0.5)  # Square root for roughly square grid
    grid_rows = (num_images + grid_cols - 1) // grid_cols
    
    # Calculate grid cell size based on average image dimensions
    avg_width = sum(img.width for img in images) / num_images
    avg_height = sum(img.height for img in images) / num_images
    cell_width = avg_width * 1.1  # Add 10% padding
    cell_height = avg_height * 1.1
    
    # Reorganize images in grid pattern
    for i, image in enumerate(images):
        row = i // grid_cols
        col = i % grid_cols
        
        # Calculate new position
        image.x = col * cell_width
        image.y = row * cell_height
        
        # Reset rotation and scale
        image.rotation = 0
        image.scale = 1.0
    
    # Write the reorganized file
    writer = PurWriter()
    with open(output_file, 'wb') as f:
        f.write(writer.write(pur_file))
    
    print(f"Successfully reorganized {num_images} images into a {grid_rows}x{grid_cols} grid")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python pureref_reorganize.py input.pur output.pur")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    try:
        reorganize_pureref(input_file, output_file)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)