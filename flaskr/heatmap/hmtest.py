import cgi

def main():
    form = cgi.FieldStorage()
    if(form.has_key("filename").value):
        return form

main()