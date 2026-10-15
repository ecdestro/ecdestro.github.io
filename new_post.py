#!/usr/bin/env python3
import os
import json
import shutil
from datetime import datetime

POSTS_DIR = "posts"
TEMPLATE_FILE = os.path.join(POSTS_DIR, "entry-00.html")
MANIFEST_FILE = os.path.join(POSTS_DIR, "post-list.json")

def main():
    print("--- New Post Generator ---")
    title = input("Enter post title: ").strip()
    if not title:
        print("Error: Title cannot be empty.")
        return
    
    tag = input("Enter post tag (default: System): ").strip()
    if not tag:
        tag = "System"
        
    excerpt = input("Enter a short excerpt/summary: ").strip()
    if not excerpt:
        excerpt = "No excerpt provided."

    # Generate timestamps and slugs
    now = datetime.now()
    slug_time = now.strftime("%Y%m%d_%H%M")
    iso_date = now.strftime("%Y-%m-%d")
    readable_date = now.strftime("%b %d, %Y") # e.g., Oct 14, 2026
    
    filename = f"{slug_time}.html"
    target_path = os.path.join(POSTS_DIR, filename)

    # 1. Check if template exists
    if not os.path.exists(TEMPLATE_FILE):
        print(f"Error: Template file not found at {TEMPLATE_FILE}")
        return

    # 2. Read template and replace placeholders
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("{{TITLE}}", title)
    content = content.replace("{{ISO_DATE}}", iso_date)
    content = content.replace("{{READABLE_DATE}}", readable_date)
    content = content.replace("{{TAG}}", tag)

    # 3. Write new post file
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created new post file: {target_path}")

    # 4. Update post-list.json manifest
    if os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            try:
                posts = json.load(f)
            except json.JSONDecodeError:
                posts = []
    else:
        posts = []

    # New post entry structure
    new_entry = {
        "slug": filename,
        "title": title,
        "date": iso_date,
        "tag": tag,
        "excerpt": excerpt
    }

    # Prepend to array so newest is first
    posts.insert(0, new_entry)

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4)
        
    print(f"Updated manifest: {MANIFEST_FILE}")
    print("\nSuccess! Ready to write your post.")

if __name__ == "__main__":
    main()
