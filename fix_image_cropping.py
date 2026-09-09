import os
import glob

def fix_cropping():
    template_dir = os.path.join("d:\\dbmss", "templates")
    html_files = glob.glob(os.path.join(template_dir, "*.html"))
    
    fixed_count = 0
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'object-top' in content:
            # Replace object-top with object-center
            new_content = content.replace('object-top', 'object-center')
            
            # Also ensure opacity is good
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixed_count += 1
            print(f"Fixed cropping in {os.path.basename(file)}")

    print(f"Successfully fixed image cropping in {fixed_count} templates.")

if __name__ == "__main__":
    fix_cropping()
