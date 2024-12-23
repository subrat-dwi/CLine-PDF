import requests
from PIL import Image
from io import BytesIO
import os
from time import sleep
from dotenv import load_dotenv
from fpdf import FPDF
from rich.console import Console
from rich.table import Table
from rich import box
from term_image.image import AutoImage

# initializing console and table from rich library
console = Console()
table = Table(title="CLine-PDF", box=box.SQUARE_DOUBLE_HEAD)

# loading .env file to retrieve access-key of Unsplash API
load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_KEY")

# initializing pdf using fpdf
pdf = FPDF()
pdf.add_page()
pdf.set_font("helvetica", size=16)

# list to capture all operations done on the PDF
done_list = []
#--------------------main--------------------#

def main():

    table.add_column("Command", justify="center", style="bold magenta")
    table.add_column("Operation", justify="center", style="cyan")
    table.add_row("/h", "Add Heading")
    table.add_row("/p", "Add Paragraph")
    table.add_row("/n", "Add New Page")
    table.add_row("/img", "Add Image File")
    table.add_row("/imgu", "Add Image from Unsplash")
    table.add_row("/font", "Modify Font")
    table.add_row("/done", "Finish and Save PDF")
    table.add_row("/exit", "Exit without Saving")

    functions = {
        "/h" : add_heading,
        "/p" : add_paragraph,
        "/img" : add_image,
        "/imgu" : get_unsplash_image,
        "/font" : font_setting,
    }

    while True:
        console.clear()
        console.print(table, justify="center")
        for i in done_list:
            console.print(i, style="bold blue", justify="center")

        command = console.input("[bold]Command : [/]").strip()
        if command == "/exit":
            print("\033[F\033[K", end="")
            console.print("[bold red][/]", justify="center")
            break
        elif command == "/done":
            f_name = console.input("[bold]File Name (without ext.) : [/]").strip()
            pdf.output(f"{f_name}.pdf")
            print("\033[F\033[K"*2, end="")
            console.print(f"[bold green]Your [bold magenta]{f_name}.pdf[/] is Ready.[/]", justify="center")
            break
        elif (command in functions):
            print("\033[F\033[K", end="")
            if command == "/img":
                path = console.input("File Path : ")
                functions[command](path)
                continue
            functions[command]()
        elif command == "/n":
            pdf.add_page()
            done_list.append("New Page Added")
        else:
            console.print("[bold red]Enter Valid Command[/]")
            sleep(2)


#-------------function-definitions--------------#

# function for adding a Heading
def add_heading():
    pdf.set_font("helvetica", style="B", size=28)
    text = console.input("Heading : ")
    pdf.cell(0, 10, text, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    pdf.set_font("helvetica", style="", size=16)
    done_list.append("Heading Added")

# function for adding a Paragraph
def add_paragraph():
    text = console.input("Paragraph : ")
    pdf.multi_cell(0, 10, text, align="J", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    done_list.append("Paragraph Added")

# function for changing Font Setings
def font_setting():
    valid_families = ["Helvetica", "Times", "Courier", "Symbol"]
    valid_styles = ["B","I","U"]
    family = console.input("[bold yellow]Font family[/] (Helvetica | Times | Courier | Symbol) : ").capitalize()
    fstyle = console.input("[bold yellow]Font style[/] (B | I | U) : ").upper()
    fsize = console.input("[bold yellow]Font size[/] : ")
    try:
        if family not in valid_families or fstyle not in valid_styles:
            raise ValueError("Invalid Font Settings")
        pdf.set_font(family, style=fstyle, size=int(fsize))
        done_list.append("Font Settings Updated")
    except Exception:
        feedback("Invalid Font Settings")

# function to get Images from Unsplash API
def get_unsplash_image():
    query = console.input("Search : ")
    url = f"https://api.unsplash.com/search/photos?query={query}"
    headers = {"Authorization" : f"Client-ID {ACCESS_KEY}"}

    response = requests.get(url, headers=headers)
    if response.status_code==200:
        results = response.json()["results"]
        select_image(results)
    else:
        feedback("Request Failed")

# function for choosing among Unsplash results
def select_image(results):
    for result in results:
        image_url = result["urls"]["regular"]
        image_response = requests.get(image_url)
        image = Image.open(BytesIO(image_response.content))

        img = AutoImage(image)
        sleep(1)
        print(img)
        print("Image Preview")

        while True:
            choice = console.input("[yellow]Select this Image[/] (y|n|x): ").lower()

            if choice == "x":
                feedback("Operation Terminated")
                return
            elif choice == "y":
                add_image(image)
                return
            elif choice == "n":
                print("\033[F\033[K"*5, end="")
                break
            else:
                console.print("[bold red]Enter valid choice[/]")

# function to add Image to the PDF
def add_image(image):
    try:
        width = int(console.input("Width : "))
    except ValueError:
        console.print("[bold red]Invalid Input. Using default width (190)[/]")
        sleep(2)
        width = 190

    try:
        pdf.image(image, w=width)
    except FileNotFoundError:
        feedback("Invalid Image Path")
        return
    except Exception as e:
        feedback(f"An unexpected Error Occurred : {e}")
        return

    pdf.ln(10)
    done_list.append("Image Added")

# function to Alert on unexpected results
def feedback(text):
    console.print(text, style="bold red")
    sleep(2)
#---------------------------------------#

if __name__ == "__main__":
    main()
