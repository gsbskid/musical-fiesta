import fitz 
import json


def extract_headings_and_contents(
    pdf_paths, red_color = 14176347) :
    '''
    Function to extract headings and contents from a PDF

    Args :
        1) pdf_paths : list : list of paths to PDFs
        2) red_color : int : red color to extract headings

    Returns :
        1) dict : headings and contents
    '''

    headings_contents = {}
    current_heading = None
    current_content = ''

    # Loop through the PDFs

    for path in pdf_paths : 

        # Open the PDF

        doc = fitz.open(path)

        for page in doc : 

            # Get the blocks

            blocks = page.get_text('dict')['blocks']

            for block in blocks :

                # Get the lines

                try :  

                    for line in block['lines'] : 

                        # Get the spans

                        try :

                            for span in line['spans'] : 

                                # Extract the text

                                try : 

                                    # Extract the color, text and size

                                    color = span['color']
                                    text = span['text']
                                    size = span['flags']

                                    # Check if the color is red or the size is bold, if so, then it is a heading

                                    if color == red_color or size & 1 << 5 : 

                                        # If there is a current heading, then add the content to the dictionary

                                        if current_heading : 

                                            # Add the content to the dictionary

                                            if current_heading in headings_contents : headings_contents[current_heading] += current_content.strip() + '\n' 
                                            else : headings_contents[current_heading] = current_content.strip()

                                        # Update the current heading and content

                                        current_heading = text
                                        current_content = ''

                                    else : current_content += text + ''

                                except : pass
                        except : pass
                except : pass

        # Add the last content to the dictionary

        if current_heading : 

            if current_heading in headings_contents : headings_contents[current_heading] += current_content.strip() 
            else : headings_contents[current_heading] = current_content.strip()

    return headings_contents

sections = extract_headings_and_contents([
    'Assets/PDFs/input_pdf_20.pdf' , 
    'Assets/PDFs/pzuw- 1 column.pdf' , 
    'Assets/PDFs/SWU_WDCiR_2014_02 - 1 column.pdf'
])


json_data = json.dumps(sections)

with open('Assets/JSONs/data.json' , 'w') as fil : json.dump(json_data, fil)