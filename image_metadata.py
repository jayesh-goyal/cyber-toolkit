from PIL import Image
from PIL.ExifTags import TAGS
import os

def extract_metadata(image_path):
    print(f"\n=== IMAGE METADATA EXTRACTOR ===")
    print(f"By Jayesh Goyal")
    print(f"File: {image_path}")
    print("="*40)

    try:
        img = Image.open(image_path)

        # Basic info
        print(f"\n[1] BASIC INFO:")
        print(f"    Format: {img.format}")
        print(f"    Size: {img.size}")
        print(f"    Mode: {img.mode}")
        print(f"    File size: "
        f"{os.path.getsize(image_path)} bytes")

        # EXIF data
        print(f"\n[2] EXIF DATA (Hidden metadata):")
        exif_data = img._getexif()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag in ['DateTime','Make','Model',
                'GPSInfo','Software','Artist',
                'Copyright','ImageDescription',
                'UserComment','XPComment',
                'CameraOwnerName']:
                    print(f"    {tag}: {value}")
        else:
            print("    No EXIF data found")
            print("    (Image may have been stripped"
            " of metadata)")

        # GPS
        print(f"\n[3] GPS LOCATION:")
        if exif_data:
            gps = exif_data.get(34853)
            if gps:
                print(f"    GPS Data found: {gps}")
                print("    ⚠️  This image contains"
                " location data!")
            else:
                print("    No GPS data found")
        else:
            print("    No GPS data found")

        print("\n" + "="*40)
        print("ANALYSIS COMPLETE!")
        print("="*40)

    except Exception as e:
        print(f"Error: {e}")

while True:
    path = input("\nEnter image path or 'quit': ")
    if path == 'quit':
        break
    extract_metadata(path)
