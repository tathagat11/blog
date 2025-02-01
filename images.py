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
        
        # Split frontmatter and content
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            main_content = parts[2]
        else:
            continue  # Skip files without proper frontmatter

        # Process images in main content
        images = re.findall(r'!\[\[([^]]*\.png)\]\]', main_content)
        
        # Process images in main content
        for image in images:
            # Prepare the Markdown-compatible link with %20 replacing spaces
            markdown_image = f"![Image Description](/images/{image.replace(' ', '%20')})"
            main_content = main_content.replace(f"![[{image}]]", markdown_image)
            
            # Copy image to Hugo static directory
            image_source = os.path.join(attachments_dir, image)
            if os.path.exists(image_source):
                shutil.copy(image_source, static_images_dir)

        # Process cover image in frontmatter
        cover_image_match = re.search(r'cover:\s*\n\s*image:\s*"?\[\[([^]]*\.(?:png|jpg|jpeg))\]\]"?', frontmatter)
        if cover_image_match:
            cover_image = cover_image_match.group(1)
            # Update frontmatter with proper Hugo path
            frontmatter = frontmatter.replace(
                f"[[{cover_image}]]",
                f"/images/{cover_image.replace(' ', '%20')}"
            )
            
            # Copy cover image to Hugo static directory
            cover_image_source = os.path.join(attachments_dir, cover_image)
            if os.path.exists(cover_image_source):
                shutil.copy(cover_image_source, static_images_dir)

        # Reconstruct the file content
        updated_content = f"---{frontmatter}---{main_content}"
        
        # Write the updated content back to the markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(updated_content)

print("Markdown files processed and images copied successfully.")