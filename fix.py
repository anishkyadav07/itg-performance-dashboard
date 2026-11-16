p = r"C:\Users\ASUS\OneDrive\Desktop\Indian tech Data science\dashboard.py"
text = open(p, encoding="utf-8").read()

while "](http" in text:
    i = text.find("](http")
    start = text.rfind("[", 0, i)
    end = text.find(")", i)
    text = text[:start] + text[start + 1:i] + text[end + 1:]

open(p, "w", encoding="utf-8", newline="\n").write(text)
print("Done")