# AVID Shot Renaming Utility
A utility script that can be used to modify shot names in an AVID bin in bulk. Given an ALE file, it will let you enter a search RegEx, and then modify the matches by substituting them with text, another expression, or by converting it to uppercase or lowercase.
## Usage
`python avid_renamer_utility.py path/to/input [path/to/output]`

If the output path is not specified, the input file will be overwritten.

### Examples
![Screenshot 2022-02-11 160139](https://user-images.githubusercontent.com/3130987/153670574-330ca7f8-f11c-4291-831d-ffb10ac435d3.png)
![Screenshot 2022-02-11 160932](https://user-images.githubusercontent.com/3130987/153670584-4ce32318-44fa-49d5-bf12-5d2e4ef77c3a.png)

## Author
* Zal Machado (zalmachado@gmail.com)

## Next Steps
* Allow modifying other columns
* Test cases
* GUI
