# QsweMaker
Schematic maker &amp; guide for the QSWE

> [!NOTE]
> Currently the schematic maker can't rotate the WE.
>
> The schematics generated always have Main station in +z and Return in -z

## Get exact sizes
- Open the program in console mode by using
```bash
python3 schem_gen.py sizes <width> <length>
```
- The program will then ask if you want to generate a schematic with the correct sizes (type `y` if you want to proceed)

## How to tile the schematic
- Decide the width and length of the perimeter
- Open the program in console mode by using
```bash
python3 schem_gen.py schem <width> <length>
```
- The program will then ask if you want to know at what height you should place the WE (type `y` if you want to proceed)
- If the width or length are wrong, the program will suggest new ones and ask if you want to generate a schematic with them (type `y` if you want to proceed)

## Get initial height
- Open the program in console mode by using
```bash
python3 schem_gen.py height  <start> <end (defaults to -59)>
```
