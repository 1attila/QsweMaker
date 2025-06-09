# QsweMaker
Schematic maker &amp; guide for the QSWE

> [!NOTE]
> Currently the schematic maker can't rotate the WE.
>
> The schematics generated always have Main station in +z and Return in -z
## UI Mode

Recomended. It's: `QsweMaker-V3.exe`

### Get exact sizes
- Enter the size that you want
- Press "Calculate Sizes" button
- The program will display the new sizes at the bottom with their difference, and the values you inserted before will be updated

### Generate the schematic
- Enter the size that you want
- If you don't know if these exact size could be used, press "Calculate Sizes" first
- Then press "Generate Schematic" button
- If the initial sizes were wrong and you didnt press "Calculate Sizes" the program will calculate the rigth sizes and ask if you want to generate a schematic with them

### Get initial height
- Enter the coordinate of the highest block to remove with the WE
- Enter the coordinate of the lowest block to remove (default: Y= -59)
- Press "Calculate Height" button and use the displayed height for the schematic placement

## Console Mode

Console mode for terminal users that don't like UIs

### Get exact sizes
- Open the program in console mode by using
```bash
python3 schem_gen.py sizes <width> <length>
```
- The program will then ask if you want to generate a schematic with the correct sizes (type `y` if you want to proceed)

### Generate the schematic
- Open the program in console mode by using
```bash
python3 schem_gen.py schem <width> <length>
```
- The program will then ask if you want to know at what height you should place the WE (type `y` if you want to proceed)
- If the width or length are wrong, the program will suggest new ones and ask if you want to generate a schematic with them (type `y` if you want to proceed)

### Get initial height
- Open the program in console mode by using
```bash
python3 schem_gen.py height  <start> <end (defaults to -59)>
```
