import tkinter as tk
from lexer import tokenize
from parser import Parser

class SyntaxHighlighter:
    def __init__(self, root):
        self.root = root
        self.root.title("Syntax Highlighter")
        self.text = tk.Text(root, bg="black", fg="white", insertbackground="white", font=("Consolas", 12))
        self.text.pack(expand=True, fill=tk.BOTH)
        self.status = tk.Label(root, text="Ready", anchor="w", bg="black", fg="white", font=("Consolas", 10))
        self.status.pack(fill=tk.X)
        
        # Renkler
        self.text.tag_configure("KEYWORD", foreground="#00BFFF")  # Mavi
        self.text.tag_configure("ID", foreground="#FFFFFF")  # Beyaz
        self.text.tag_configure("INT_VAR", foreground="#87CEFA")  # Açık mavi
        self.text.tag_configure("CHAR_VAR", foreground="#FFB6C1")  # Açık pembe
        self.text.tag_configure("NUMBER", foreground="#FFA500")  # Turuncu
        self.text.tag_configure("CHAR_LITERAL", foreground="#D2691E")  # Çikolata
        self.text.tag_configure("OPERATOR", foreground="#FF69B4")  # Pembe
        self.text.tag_configure("SYMBOL", foreground="#ADFF2F")  # Yeşil sarı
        self.text.tag_configure("COMMENT", foreground="#7FFF00")  # Açık yeşil
        self.text.tag_configure("ELSE_ERROR", foreground="#FF4500")  # Kırmızı
        self.text.tag_configure("ELSE_OK", foreground="#FFD700")  # Altın
        
        self.highlight()
        self.text.bind("<KeyRelease>", lambda event: self.highlight())

    def is_else_following_if(self, tokens, pos):
        for i in range(pos - 1, -1, -1):
            if tokens[i] == ("KEYWORD", "if"):
                return True
        return False

    def highlight(self):
        code = self.text.get("1.0", tk.END).rstrip()
        for tag in ["KEYWORD", "ID", "INT_VAR", "CHAR_VAR", "NUMBER", "CHAR_LITERAL", "OPERATOR", "SYMBOL", "COMMENT", "ELSE_ERROR", "ELSE_OK"]:
            self.text.tag_remove(tag, "1.0", tk.END)

        if not code.strip():  # Boş input kontrolü
            self.status.config(text="Ready", fg="white")
            self.root.after(100, self.highlight)
            return

        tokens = tokenize(code)
        idx = "1.0"
        for i, (token_type, value) in enumerate(tokens):
            start_idx = self.text.search(value, idx, tk.END, regexp=False)
            if not start_idx:
                continue
            end_idx = f"{start_idx}+{len(value)}c"
            if token_type == "KEYWORD" and value == "else":
                if self.is_else_following_if(tokens, i):
                    self.text.tag_add("ELSE_OK", start_idx, end_idx)
                else:
                    self.text.tag_add("ELSE_ERROR", start_idx, end_idx)
            else:
                self.text.tag_add(token_type, start_idx, end_idx)
            idx = end_idx

        # Sözdizimsel analiz
        parser = Parser(tokens)
        valid, errors = parser.parse_program()
        if valid:
            self.status.config(text="Syntax OK", fg="green")
        else:
            self.status.config(text=f"Syntax Error: {'; '.join(errors[:2])}", fg="red")

        self.root.after(100, self.highlight)

if __name__ == "__main__":
    root = tk.Tk()
    app = SyntaxHighlighter(root)
    root.mainloop()