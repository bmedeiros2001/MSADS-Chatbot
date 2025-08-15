import json
import os

def fix_notebook(notebook_path):
    """Fix corrupted notebook by cleaning widget metadata"""
    
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Remove problematic widget metadata
    if 'metadata' in notebook:
        if 'widgets' in notebook['metadata']:
            del notebook['metadata']['widgets']
    
    # Clean cell metadata
    for cell in notebook.get('cells', []):
        if 'metadata' in cell:
            cell['metadata'] = {k: v for k, v in cell['metadata'].items() 
                              if not k.startswith('widget')}
    
    # Save the fixed notebook
    fixed_path = notebook_path.replace('.ipynb', '_FIXED.ipynb')
    with open(fixed_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)
    
    print(f"✅ Fixed notebook saved as: {fixed_path}")
    return fixed_path

# Check what files are in your directory first
print("Files in current directory:")
print(os.listdir('.'))

# Now try to fix the notebook
fix_notebook('PART_2_Embeddings.ipynb')