import os
import re
import shutil

# Paths (using raw strings to handle Windows backslashes correctly)
posts_dir = r"C:\Users\tatha\workspace\projects\blog\content\blogs"
attachments_dir = r"C:\Users\tatha\OneDrive\Desktop\ObsidianStuff\MyVault\Assets"
static_images_dir = r"C:\Users\tatha\workspace\projects\blog\static\images"

# Step 1: Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Split content into frontmatter and body
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
            
            # Handle cover image in frontmatter
            frontmatter_matches = re.finditer(r'image:\s*!\[\[([^]]*\.png)\]\]', frontmatter)
            for match in frontmatter_matches:
                image = match.group(1)
                # Format for cover image (theme format)
                old_text = f"image: ![[{image}]]"
                new_text = f'image: "/images/{image.replace(" ", "%20")}"'
                frontmatter = frontmatter.replace(old_text, new_text)
                
                # Copy image if it exists
                image_source = os.path.join(attachments_dir, image)
                if os.path.exists(image_source):
                    shutil.copy(image_source, static_images_dir)
            
            # Handle images in body
            body_matches = re.finditer(r'!\[\[([^]]*\.png)\]\]', body)
            for match in body_matches:
                image = match.group(1)
                # Format for body images (regular markdown)
                old_text = f"![[{image}]]"
                new_text = f'![Image Description](/images/{image.replace(" ", "%20")})'
                body = body.replace(old_text, new_text)
                
                # Copy image if it exists
                image_source = os.path.join(attachments_dir, image)
                if os.path.exists(image_source):
                    shutil.copy(image_source, static_images_dir)
            
            # Reconstruct the content
            updated_content = f"---{frontmatter}---{body}"
            
            # Write the updated content back to the markdown file
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(updated_content)

print("Markdown files processed and images copied successfully.")