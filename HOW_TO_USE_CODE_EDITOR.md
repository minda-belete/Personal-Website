# How to Add Code Snippets in Blog Posts

## Two Ways to Add Code:

### 1. **IN THE TEXT (Recommended)** - Insert Code Snippet Button
Look in the CKEditor toolbar for a button that says **"Insert Code Snippet"** or has a `</>` icon.
- It's in the toolbar, usually in the 3rd or 4th row
- NOT the "Source" button (that's for HTML)
- Click it to open a code editor dialog

### 2. **SEPARATE SECTION (Bottom)** - "Add another Code snippet"
The section at the bottom with "Add another Code snippet" is for standalone code blocks.
- Uses the enhanced CodeMirror editor
- Good for very long code
- But less convenient for mixing with text

## Using Method 1: Integrated Code Editor in CKEditor

### Step-by-Step Guide:

1. **Go to Blog Post Editor**
   - Admin → Blog → Blog Posts → Add Blog Post (or edit existing)

2. **Write Your First Paragraph**
   ```
   Type your normal text here. This is my introduction paragraph...
   ```

3. **Insert Code Snippet**
   - Place your cursor where you want the code
   - Click the **"Code Snippet"** button in the toolbar (looks like `</>`)
   - A dialog will open

4. **In the Code Snippet Dialog:**
   - **Select Language**: Choose from dropdown (Python, JavaScript, Java, C++, etc.)
   - **Type or Paste Your Code**: The editor has:
     - ✅ Syntax highlighting
     - ✅ Line numbers
     - ✅ Auto-indentation
     - ✅ Tab support (press Tab to indent)
     - ✅ Auto-indent after colons (for Python)
   
   Example:
   ```python
   def hello_world():
       print("Hello, World!")
       return True
   ```

5. **Click OK** - The code snippet is inserted!

6. **Continue Writing**
   - Press Enter to move to the next line
   - Type your next paragraph
   - Add another code snippet whenever you want

### Example Blog Post Structure:

```
This is my introduction paragraph about Python functions.

[CODE SNIPPET - Python]
def greet(name):
    return f"Hello, {name}!"

Here I explain what the function does...

[CODE SNIPPET - Python]
result = greet("World")
print(result)

And here's my conclusion paragraph.
```

### Features:

✅ **Seamless Integration**: Code snippets appear inline with your text
✅ **Multiple Languages**: 18+ programming languages supported
✅ **Syntax Highlighting**: Automatic color coding based on language
✅ **Professional Look**: Uses Monokai theme (dark background)
✅ **Auto-Indentation**: Press Tab or Enter after `:` for auto-indent
✅ **Copy Button**: Readers can copy code with one click on the frontend

### Tips:

- You can add as many code snippets as you want in a single post
- Mix text, images, videos, and code freely
- Edit code snippets by double-clicking them in the editor
- The code will be beautifully formatted on your blog automatically

### Alternative: Separate Code Snippets Section

If you prefer, you can also add code snippets in the separate "Code Snippets" section below the main editor:
- These use the enhanced CodeMirror editor
- Better for very long code blocks
- Can be reordered independently

But for most use cases, the **integrated Code Snippet button** in the main editor is the easiest way!
