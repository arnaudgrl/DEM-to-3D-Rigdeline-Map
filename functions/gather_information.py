# File: gather_information.py

def get_information(file_path):
    with open(file_path, 'r') as file:
        # Read the maximum_map_size from the first line of the file
        first_line = file.readline().strip()
        if first_line.startswith('maximum_map_size='):
            maximum_map_size = int(first_line.split('=')[1])
        else:
            # Handle the case where the first line format is not as expected
            print("Error: Incorrect format in the first line of info.txt")
            return None

        # Read the width from the second line of the file
        second_line = file.readline().strip()
        if second_line.startswith('width='):
            width = int(second_line.split('=')[1])
        else:
            # Handle the case where the second line format is not as expected
            print("Error: Incorrect format in the second line of info.txt")
            return None

        # Return the extracted values
        return maximum_map_size, width