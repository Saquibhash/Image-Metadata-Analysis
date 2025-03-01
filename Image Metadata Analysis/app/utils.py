from PIL import Image
from PIL.ExifTags import TAGS
import json
from datetime import datetime
import os

def extract_metadata(image_path):
    try:
        image = Image.open(image_path)
        
        # Fetch image size and format
        width, height = image.size
        file_size = os.path.getsize(image_path)
        format_type = image.format
        
        exif_data = image._getexif()
        metadata = {
            "Format": format_type,
            "File Size": f"{file_size / 1024:.2f} KB",  # Convert to KB
            "Dimensions": f"{width}x{height}",
            "Type": image.format,
            "Proportions": f"{width / height:.2f}" if height != 0 else "N/A",  # Proportions (width/height ratio)
            "Megapixels": f"{(width * height) / 1_000_000:.2f} MP"  # Calculate megapixels
        }

        # Default values
        metadata["Device"] = "N/A"
        metadata["GPS Coordinates"] = "N/A"
        metadata["Date and Time"] = "N/A"
        metadata["Description"] = "N/A"
        
        # Extract Exif data for more fields
        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = TAGS.get(tag_id, tag_id)
                
                # Camera model
                if tag_name == "Model":
                    metadata["Device"] = str(value)

                # Date and Time
                if tag_name == "DateTimeOriginal" or tag_name == "CreateDate":
                    try:
                        # Try to parse the datetime in the format: "YYYY:MM:DD HH:MM:SS"
                        metadata["Date and Time"] = str(value)
                        datetime_object = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                        metadata["Date and Time"] = datetime_object.strftime("%Y-%m-%d %H:%M:%S")  # Standard format
                    except ValueError:
                        metadata["Date and Time"] = "N/A"  # If parsing fails, set to N/A

                # GPS coordinates
                if tag_name == "GPSLatitude" and tag_name == "GPSLongitude":
                    metadata["GPS Coordinates"] = f"{value}"

        # Return metadata in JSON format
        return json.dumps(metadata, indent=4)

    except Exception as e:
        return json.dumps({"error": str(e)})
