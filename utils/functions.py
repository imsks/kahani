def is_real_value(value):
  if value is None:
    return False
  elif isinstance(value, str):
    return value.strip() != ""
  elif isinstance(value, int):
    return True
  
# Helper functions
def extract_year(text):
    if text.isdigit() and len(text) == 4:
        return text
    return None

def extract_runtime(text):
    # Check if the text has a time-related keyword (e.g., 'min')
    if 'm' in text or 'h' in text:
        return text
    return None

def get_hidef_image(img_tag):
    # Extract the srcset attribute from the img tag
    srcset = img_tag.get('srcset', '')
    
    if not srcset:  # If srcset is missing or empty, return None
        return None
    
    # Split srcset by commas to get individual entries
    srcset_items = srcset.split(', ')
    
    # Ensure there are items to process
    if srcset_items:
        # Take the last entry, strip whitespace, and split to isolate the URL
        all_items = srcset_items[-2].strip().split(' ')

        if all_items:
            return all_items[0]
    
    return None