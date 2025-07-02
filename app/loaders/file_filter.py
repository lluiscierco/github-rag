import magic

def is_text_file(filepath):
    mime = magic.Magic(mime=True)
    filetype = mime.from_file(filepath)
    return filetype.startswith("text")
