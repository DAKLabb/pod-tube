import xml.etree.ElementTree as ET
import argparse
from email.utils import formatdate

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update the provided RSS feed with a new episode.")
    parser.add_argument("path", type=str, help="Path to RSS feed being updated")
    parser.add_argument("--title", type=str, required=True, help="Title of episode being added")
    parser.add_argument("--url", type=str, required=True, help="URL of the episode being added")
    parser.add_argument("--bytes", type=int, required=True, help="Size of the file (in bytes)")
    parser.add_argument("--guid", type=str, required=True, help="guid for the episode)")
    parser.add_argument("--timestamp", type=int, required=True, help="Publish date for the episode)")
    parser.add_argument("--thumbnail", type=str, required=True, help="Thumbnail for this episode)")

    args = parser.parse_args()

    tree = ET.parse(args.path)
    root = tree.getroot()
    channel = root.find("channel")

    new_item = ET.SubElement(channel, "item")
    title_element = ET.SubElement(new_item, 'title')
    title_element.text = args.title
    enclosure_element = ET.SubElement(new_item, 'enclosure')
    enclosure_element.set("url", args.url)
    enclosure_element.set("type", "audio/mpeg")
    enclosure_element.set("length", str(args.bytes))
    guid_element = ET.SubElement(new_item, 'guid')
    guid_element.text = args.guid
    date_element = ET.SubElement(new_item, 'pubDate')
    date_element.text = formatdate(args.timestamp, usegmt=True) 
    img_element = ET.SubElement(new_item, 'itunes:image')
    img_element.set("href", args.thumbnail)

    # Save the changes
    tree.write(args.path)
