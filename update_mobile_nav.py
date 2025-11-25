#!/usr/bin/env python3
"""
Update mobile navigation to center logo on all HTML pages
"""

import os
import glob
import re

# Find all HTML files
html_files = glob.glob('**/*.html', recursive=True)

# Exclude certain files
exclude_patterns = ['node_modules', '.bak', 'googlef24fe0a0e8ba99b6.html']
html_files = [f for f in html_files if not any(ex in f for ex in exclude_patterns)]

updated_count = 0

for filepath in html_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Change 1: Update flex justify-between to justify-center md:justify-between
        content = content.replace(
            'class="flex justify-between items-center h-16"',
            'class="flex justify-center md:justify-between items-center h-16"'
        )

        # Change 2: Add absolute right-4 to mobile menu button container
        # Look for the md:hidden div that contains the hamburger button
        content = re.sub(
            r'<div class="md:hidden">(\s*<button class="hamburger")',
            r'<div class="md:hidden absolute right-4">\1',
            content
        )

        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated: {filepath}")
            updated_count += 1
        else:
            print(f"- No changes needed: {filepath}")

    except Exception as e:
        print(f"✗ Error updating {filepath}: {e}")

print(f"\n{updated_count} files updated successfully!")
