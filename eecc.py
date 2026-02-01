"""
EE Component Calculator

Published on February 1, 2026.

MIT License

Copyright (c) 2026 CantisW

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

abbr_to_color_map = {
    "BL": "black",
    "BR": "brown",
    "R": "red",
    "O": "orange",
    "Y": "yellow",
    "G": "green",
    "B": "blue",
    "V": "violet",
    "W": "white",
    "GD": "gold",
    "S": "silver"
}

color_to_value_map = {
    "black": 0,
    "brown": 1,
    "red": 2,
    "orange": 3,
    "yellow": 4,
    "green": 5,
    "blue": 6,
    "violet": 7,
    "grey": 8,
    "white": 9,
    "gold": -1,
    "silver": -2
}

color_to_tolerance_map = {
    "brown": "1%",
    "red": "2%",
    "green": "0.5%",
    "blue": "0.25%",
    "violet": "0.1%",
    "grey": "0.05%",
    "gold": "5%",
    "silver": "10%"
}

color_to_ppm_map = {
    "brown": "100 PPM/°C",
    "red": "50 PPM/°C",
    "orange": "15 PPM/°C",
    "yellow": "25 PPM/°C",
    "blue": "10 PPM/°C",
    "violet": "5 PPM/°C"
}

alphabet = "abcdefghijklmnopqrstuvwxyz"

# https://github.com/so1der/smd-resistors-calc/blob/main/EIA96.py
# didn't want to manually type this...

EIA96_index = {"01": 100, "02": 102, "03": 105, "04": 107, "05": 110, "06": 113,
         "07": 115, "08": 118, "09": 121, "10": 124, "11": 127, "12": 130,
         "13": 133, "14": 137, "15": 140, "16": 143, "17": 147, "18": 150,
         "19": 154, "20": 158, "21": 162, "22": 165, "23": 169, "24": 174,
         "25": 178, "26": 182, "27": 187, "28": 191, "29": 169, "30": 200,
         "31": 205, "32": 210, "33": 215, "34": 221, "35": 226, "36": 232,
         "37": 237, "38": 243, "39": 249, "40": 255, "41": 261, "42": 267,
         "43": 274, "44": 280, "45": 287, "46": 294, "47": 301, "48": 309,
         "49": 316, "50": 324, "51": 332, "52": 340, "53": 348, "54": 357,
         "55": 365, "56": 374, "57": 383, "58": 392, "59": 402, "60": 412,
         "61": 422, "62": 432, "63": 442, "64": 453, "65": 464, "66": 475,
         "67": 487, "68": 499, "69": 511, "70": 523, "71": 536, "72": 549,
         "73": 562, "74": 576, "75": 590, "76": 604, "77": 619, "78": 634,
         "79": 649, "80": 665, "81": 681, "82": 698, "83": 715, "84": 732,
         "85": 750, "86": 768, "87": 787, "88": 806, "89": 825, "90": 845,
         "91": 866, "92": 887, "93": 909, "94": 931, "95": 953, "96": 976,
         "97": 0, "98": 0, "99": 0}

EIA96_mult = {"Z": 0.001, "Y": 0.01, "R": 0.01, "X": 0.1, "S": 0.1, "A": 1,
             "B": 10, "H": 10, "C": 100, "С": 100, "D": 1000, "E": 10000,
             "F": 100000}

def validate_input(input, len=3):
    """
    Returns `True` if each character in a string is a number. Otherwise, return `False`.
    
    :param input: The string to validate
    :param len: Length to validate to
    """
    try:
        int(input[:len])
    except ValueError:
        return False
    return True

def validate_colors(input):
    """
    Returns the mapped colors if each value in the list is a valid color. Otherwise, return `False`.
    
    :param input: The list to validate
    """
    output = []

    for color in input:
        if color in abbr_to_color_map:
            output.append(abbr_to_color_map[color])
        else:
            return False
    return output

def colors_to_value(input, len):
    """
    Converts a list of colors into a numerical value.
    
    :param input: The list to convert to a value
    :param len: The length to check up to
    """
    output = ""

    for color in input[:len]:
        output += str((color_to_value_map[color]))
    return int(output)

def value_to_str(input, multiplier):
    """
    Given a value and multiplier, gets the string (value with units).
    """
    num = input * 10**color_to_value_map[multiplier]
    if num >= 1000000:
        return f"{num/1000000} MΩ"
    elif num >= 1000:
        return f"{num/1000} kΩ"
    elif num >= 0:
        return f"{num} Ω"
    elif num >= 0.001:
        return f"{num*1000} mΩ"

def calculate():
    string = input("input: ")
    tokens = string.split(" ")
    if len(tokens) < 2:
        return "invalid number of arguments. must be at least 2."
    component_type = tokens[0]
    to_calculate = tokens[1:]
    if component_type not in ("RST", "CAP"):
        return "second argument must be 'RST' (resistor) or 'CAP' (capacitor)"
    if len(to_calculate) == 1:
        digits = list(to_calculate[0])
        if component_type == "RST":
            # we can assume an EIA code
            if len(digits) > 4:
                return "invalid number of digits."
            if len(digits) == 3:
                # assume 3 digit EIA or EIA-96
                if digits[-1].lower() in alphabet:
                    # definitely intended to be EIA-96
                    if digits[-1] not in EIA96_mult:
                        return "invalid EIA-96 color code. last digit is not a valid letter multiplier."
                    if not validate_input(to_calculate[0], 2):
                        return "invalid types."
                    index = digits[0] + digits[1]
                    return EIA96_index[index] * EIA96_mult[digits[-1]]
                # else just assume regular EIA
                if not validate_input(to_calculate[0]):
                    return "invalid types."
                value = digits[0] + digits[1]
            else:
                value = digits[0] + digits[1] + digits[2]
            return int(value) * 10**int(digits[-1])
        else:
            if len(digits) < 3:
                return to_calculate[0] + " pF"
            if digits[-1] in ("7", "8", "9"):
                return "final digit must not exceed 6."
            if not validate_input(to_calculate[0]):
                return "invalid types."
            value = digits[0] + digits[1]
            output = int(value) * 10**int(digits[-1])
            if output > 1000000:
                return f"{output/1000000} uF"
            if output > 1000:
                return f"{output/1000} nF"
            return f"{output} pF"
        
    # assume we have a resistor color code
    list_of_colors = validate_colors(to_calculate)
    if not list_of_colors:
            return "invalid colors."
    third = list_of_colors[-3]
    penultimate = list_of_colors[-2]
    final = list_of_colors[-1]
    if len(to_calculate) == 3:
        value = colors_to_value(list_of_colors, 2)
        return f"{value_to_str(value, final)}"
    elif len(to_calculate) == 6:
        value = colors_to_value(list_of_colors, 3)
        return f"{value_to_str(value, third)}, tolerance {color_to_tolerance_map[penultimate]}, {color_to_ppm_map[final]}"

    elif len(to_calculate) == 4:
        # we have a 4 band
        value = colors_to_value(list_of_colors, 2)
        if final not in color_to_tolerance_map:
            return "invalid final tolerance color."
    elif len(to_calculate) == 5:
        # we have a 5 band
        value = colors_to_value(list_of_colors, 3)
        if final not in color_to_tolerance_map:
            return "invalid final tolerance color."
    return f"{value_to_str(value, penultimate)}, tolerance {color_to_tolerance_map[final]}"
        
    

if __name__ == "__main__":
    print(r"""  ______ ______    _____      _            _       _             
 |  ____|  ____|  / ____|    | |          | |     | |            
 | |__  | |__    | |     __ _| | ___ _   _| | __ _| |_ ___  _ __ 
 |  __| |  __|   | |    / _` | |/ __| | | | |/ _` | __/ _ \| '__|
 | |____| |____  | |___| (_| | | (__| |_| | | (_| | || (_) | |   
 |______|______|  \_____\__,_|_|\___|\__,_|_|\__,_|\__\___/|_|   
                                                                 
                                                                 """)
    print("created by: santiago vega\n")
    print(f"""
    USAGE
          
    to use this CLI tool, you input a string with two components:
          1. type of passive component (RST or CAP)
          2. value
    for instance, you would type "RST 010" to calculate the resistance of an SMD resistor with EIA value 010.
    for colors, use this example: "RST R R R GD" (red, red, red, gold)
          
    SUPPORTED CODES
          * ceramic capacitor codes
          * resistor color codes
          * resistor EIA codes (3 and 4 digit)
          * resistor EIA-96 codes

    type checking is included...mostly! if you find a bug, please report an issue to the github at https://github.com/CantisW/ee-component-calculator
          
    COLOR REFERENCE\n
    """)
    for i, v in abbr_to_color_map.items():
        print(i, "-", v)
    print("\n")

    while True:
        print(calculate())
        print("\n")