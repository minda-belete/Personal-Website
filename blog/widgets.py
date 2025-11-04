from django import forms
from django.utils.safestring import mark_safe


class CodeEditorWidget(forms.Textarea):
    """Custom widget for code editing with syntax highlighting"""
    
    def __init__(self, attrs=None, language='python'):
        default_attrs = {
            'class': 'code-editor',
            'rows': 20,
            'style': 'font-family: monospace; width: 100%;'
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
        self.language = language
    
    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.css',
                'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/theme/monokai.min.css',
            )
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/codemirror.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/python/python.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/javascript/javascript.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/clike/clike.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/php/php.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/ruby/ruby.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/go/go.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/rust/rust.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/sql/sql.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/htmlmixed/htmlmixed.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/css/css.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/shell/shell.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.2/mode/r/r.min.js',
        )
    
    def render(self, name, value, attrs=None, renderer=None):
        textarea = super().render(name, value, attrs, renderer)
        
        # Get the textarea ID
        textarea_id = attrs.get('id', f'id_{name}') if attrs else f'id_{name}'
        
        # Language mode mapping
        mode_map = {
            'python': 'python',
            'javascript': 'javascript',
            'java': 'text/x-java',
            'cpp': 'text/x-c++src',
            'csharp': 'text/x-csharp',
            'php': 'php',
            'ruby': 'ruby',
            'go': 'go',
            'rust': 'rust',
            'sql': 'sql',
            'html': 'htmlmixed',
            'css': 'css',
            'bash': 'shell',
            'r': 'r',
        }
        
        mode = mode_map.get(self.language, 'python')
        
        script = f"""
        <script>
        (function() {{
            var textarea = document.getElementById('{textarea_id}');
            if (textarea && typeof CodeMirror !== 'undefined') {{
                var editor = CodeMirror.fromTextArea(textarea, {{
                    mode: '{mode}',
                    theme: 'monokai',
                    lineNumbers: true,
                    indentUnit: 4,
                    indentWithTabs: false,
                    lineWrapping: true,
                    autoCloseBrackets: true,
                    matchBrackets: true,
                    extraKeys: {{
                        "Tab": function(cm) {{
                            if (cm.somethingSelected()) {{
                                cm.indentSelection("add");
                            }} else {{
                                cm.replaceSelection("    ", "end");
                            }}
                        }},
                        "Shift-Tab": function(cm) {{
                            cm.indentSelection("subtract");
                        }},
                        "Enter": function(cm) {{
                            var cursor = cm.getCursor();
                            var line = cm.getLine(cursor.line);
                            var indent = line.match(/^\\s*/)[0];
                            
                            // Auto-indent after colons (Python, etc.)
                            if (line.trim().endsWith(':')) {{
                                indent += '    ';
                            }}
                            
                            cm.replaceSelection('\\n' + indent, 'end');
                        }}
                    }}
                }});
                
                // Update textarea on change
                editor.on('change', function() {{
                    textarea.value = editor.getValue();
                }});
            }}
        }})();
        </script>
        """
        
        return mark_safe(textarea + script)
