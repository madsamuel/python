
from pdfreader import SimplePDFViewer
import pyttsx3

def take_filename(file_name = "cd.pdf"):
    input_from_user = input(f"Type path and file (e.g. c:\\temp\\file1.pdf):")
    return input_from_user if (len(input_from_user) > 0) else file_name

def take_pagenumber(page_count: int):
    print("Type 'exit' to exit the program.")
    input_from_user = input(f"Enter page # (1 to {page_count}): ")
    return input_from_user

def convert_list_to_string(list_of_strings):
    string = ""
    for string_item in list_of_strings:
        string += string_item
    return string

def speak(convertPage):
    if len(convertPage) > 0:
        print(convertPage)

        # reading the text
        speak = pyttsx3.init()
        speak.say(convert_list_to_string(convertPage))
        speak.runAndWait()


def main():
    page_count = 0

    # read file name
    file_name = take_filename()
    print("Loading PDF...")
    # read pdf 
    path = open(file_name, "rb")
    viewer = SimplePDFViewer(path)

    for canvas in viewer:
        #page_images = canvas.images
        #page_forms = canvas.forms
        #page_text = canvas.text_content
        #page_inline_images = canvas.inline_images
        page_strings = canvas.strings
        page_count += 1

    print("Loaded.")

    while True:
        input_from_user = take_pagenumber(page_count)
       
        if input_from_user == "exit":
            break
        print("You entered:", input_from_user)

        page_number = int(input_from_user)
        if page_number is not None:                
            viewer.navigate(page_number)
            viewer.render()
            convert_page = viewer.canvas.strings

            speak(convert_page)

if __name__ == "__main__":
  main()