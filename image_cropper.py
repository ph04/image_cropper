from PIL import Image
import os
import sys

HELP_MESSAGE = """
    Image cropper v1.0

    Commands:

        --input | -i [INPUT FILE] [INPUT FOLDER] [OUTPUT FOLDER]:
            
            Crops the pictures inside [INPUT FOLDER], as defined
            inside [INPUT FILE], and saves the cropped pictures inside [OUTPUT FOLDER].

            The format for the [INPUT FILE] is as follows:
                - it requires 4 different lines of text, each containing one different
                  piece of information
                - on one line, there must be something like "X = N", where 'N' must be an integer
                - on one line, there must be something like "Y = N", where 'N' must be an integer
                - on one line, there must be something like "Width = N", where 'N' must be an integer
                - on one line, there must be something like "Height = N", where 'N' must be an integer
            
            In particular, 'X' and 'Y' define the upper-left pixel of the region
            that will be used to crop the images, while 'Width' and 'Height' respectively define the
            width and height of the region. Empty lines are ignored, as well as spaces and tabs,
            and the order of the lines does not matter.
            Here is an example of a correctly formatted input file:

            X = 12
            Y = 16
            Width = 236
            Height = 234

        --help | -h:

            Shows this help message.
"""

INVALID_COMMAND = "Error: invalid command."
INVALID_ARGUMENT = "Error: invalid argument."
MISSING_ARGUMENT = "Error: missing argument."
MISSING_COMMAND = "Error: missing command."

def crop_images(path, coords, output_path):
    for image_path in os.listdir(path):
        full_path = path + "/" + image_path

        image = Image.open(full_path)

        cropped_image = image.crop(coords)

        output_image = output_path + "/" + image_path

        cropped_image.save(output_image)

        print(f"Image successfully saved at `{output_image}`")

def into_coordinates(data):
    x = data["X="]
    y = data["Y="]
    w = data["Width="]
    h = data["Height="]

    return (x, y, x + w, y + h)

def parse_data(data):
    parsed_data = {
        "X=": None,
        "Y=": None,
        "Width=": None,
        "Height=": None,
    }

    line_filter = str.maketrans({' ': None, '\t': None})

    for line in data:
        # filter every ' ' and '\t' character
        filtered_line = line.translate(line_filter)
        if filtered_line != "": # skip empty lines
            found = False

            # check if the current line is valid
            for k in parsed_data:
                if filtered_line.startswith(k):
                    found = True

                    split_line = filtered_line.split("=")

                    # if the length of this list is not 2,
                    # it means there are multiple '=', or no '=' at all
                    if len(split_line) == 2:
                        rhs = split_line[1]
                        
                        # check if every character of the right hand side
                        # is a digit, thus if the whole right hand side is a number
                        if all(map(lambda n: n.isdigit(), rhs)):
                            parsed_data[k] = int(split_line[1])
                        else:
                            return None
                    else:
                        return None

                    break

            # if nothing was found it means the current line is invalid data
            if not found:
                return None

    # check if every required piece of information is found
    return into_coordinates(parsed_data) if all(map(lambda v: v, parsed_data.values())) else None

def parse_args():
    args = sys.argv

    len_args = len(args)

    if len_args <= 1:
        print(MISSING_COMMAND)
        return False

    command = args[1]

    if command != "--input" and command != "-i":
        if command != "--help" and command != "-h":
            print(MISSING_COMMAND)
        else:
            print(HELP_MESSAGE)

        return False

    if len_args <= 2:
        print(MISSING_ARGUMENT)
        return False

    if not os.path.exists(args[2]) or not os.path.isfile(args[2]):
        print(INVALID_ARGUMENT)
        return False

    if len_args <= 3:
        print(MISSING_ARGUMENT)
        return False

    if not os.path.exists(args[3]) or os.path.isfile(args[3]):
        print(INVALID_ARGUMENT)
        return False

    if len_args <= 4:
        print(MISSING_ARGUMENT)
        return False

    output_folder = args[4]

    if os.path.exists(output_folder):
        return True
    else:
        print(INVALID_ARGUMENT)

        print(f"\nThe specified output folder `{output_folder}` does not exist")

        done = False

        while not done:
            print("Would you like to create `{output_folder}` and proceed? [y/n]", end=" ")

            choosen = input().lower()

            if choosen == "y":
                os.mkdir(output_folder)
                return True
            elif choosen == "n":
                return False
            else:
                print("Error: invalid choice")

def main():
    args = sys.argv

    if parse_args():
        with open(args[2]) as inputfile:
            data = inputfile.read().split("\n")

            if (coords := parse_data(data)):
                crop_images(args[3], coords, args[4])
            else:
                print("Error: data is not valid.")

if __name__ == "__main__":
    main()
