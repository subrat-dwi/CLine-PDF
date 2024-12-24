# CLine-PDF
My CS50p Final Project

CLine-PDF is a command-line-based PDF generator that allows you to create and customize PDFs interactively. This tool leverages libraries like `FPDF` for PDF generation, `Rich` for a visually appealing CLI, and `Pillow` for handling images. You can add text, headings, images, and modify font settings dynamically. Additionally, it supports fetching images directly from the Unsplash API.

## Video Demo : [YouTube Video](https://youtu.be/CfeziOt0MRQ?si=VP7gahT7kqcl28Uj)
---

## Features

- **Add Headings**: Insert headings to your PDF.
- **Add Paragraphs**: Add paragraphs with customizable font.
- **Add Images**: Add images from your local system or fetch them from Unsplash.
- **Modify Fonts**: Change font family, style, and size during PDF creation.
- **Dynamic Commands**: Execute commands to add new pages or finalize the PDF interactively.

---

## Requirements

- Python 3.7 or later
- Installed libraries: 
  - `requests`
  - `Pillow`
  - `fpdf`
  - `rich`
  - `python-dotenv`
  - `term-image`

---

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/subrat-dwi/CLine-PDF.git
   cd CLine-PDF

--- 

### Detailed explaination of code  
- **project.py** : This is the main program file that contains all the functions/code of this project.

  - main() : This is the main function and entry point to the program.
This consists of the command input, based ono which different functions are called to perform their respective functionalities.
The user can choose between *adding heading*, *adding paragraph*, *inserting image*, *adding new page*, *changing font settings*, *finishing/saving the pdf* or *exit without saving*.

  - add_heading() : This function is responsible for inserting a heading in the PDF.
It uses font family=Helvetica, style=Bold, size=28 as Default.

  - add_paragraph() : This functions adds text ot paragraph in the PDF.

  - font_setting() : This function is called in order to change font family, style and size for the text.
Available font families - Helvetica, Times, Courier, Symbol
Available font styles - B **(bold)**, I *(italic)*, U <ins>(underline)</ins>

  - get_unsplash_images() : When called, this functions prompts user for a search term, and requests Unsplash API to get images and image-data against the search query.
The ACCESS_KEY required to make the query request to the API is loaded from .env file.
If the request is successful, it calls the select_image() function, passing the result as argument.

  - select_image(results) : All result images are previewed one by one, with the help of *pillow* and *term-image* libraries, until the user chooses an image to add, or cancels the operation overall.
The selected image is passed to add_image() function to finally insert it into the pdf.

  - add_image() : This function prompts the user to enter the desired width of the image.
If no valid width is entered, image is added to pdf with default width of 190.

  - feedback() : This function is called from within other functions to give the feedback of an operation incase of undesired outcome.

- **requirements.txt** : This text file conatains all the required libraries that are required for proper functioning of this program.

--- 

### How I came up with this project idea?
On the 9th week of cs50 python course, I learnt about woking with pdf using fpdf2 library. It was in mind since then that, what if we can make this process of creating pdf using this library a little fun and dynamic, by allowing user to create simple pdfs directly from command line. Then i decided to work on this as my final project for cs50p.

--- 

### Design Choices
I decided that I'll add a feature to preview image on the command line when user tries to download and  add an image directly from Unsplash. This gives the user more control on which image to add in the pdf. For this, I used **term-image** library, that allows to show image in the terminal itself.

When it comes to appearence of my project, I decided I'll need to use a library in order to enhance and beautify the command-line interface, so i decided to use **rich** library for it. It provided me with methods to improve the overall user experience from the command line.

During creating the tests for my functions, I realized I cannot use simple unit test functions in my project. So I had to learn about *mocking* built-in objects using pytest-mock.

---

### Final Note
Overall, this final project was an awesome learning experince for me, while providing me the opportunity to implement the learnings of this CS50 Python course, from making simple functions to writing unit test, working with APIs, Images, Files, and different libraries.

---

#### Who Am I?
Name : Subrat Dwivedi  
Country : India  
GitHub : [subrat-dwi](https://github.com/subrat-dwi)  
edX : subrat-dwivedi  
