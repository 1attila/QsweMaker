# QsweMaker
Schematic maker &amp; [smooth floor guide](https://github.com/1attila/QsweMaker/tree/main#smooth-floor) for the QSWE

> [!NOTE]
> Currently the schematic maker can't rotate the WE.
>
> The schematics generated always have Main station in -z and Return in +z
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

## Smooth floor

> [!NOTE]
> To get the smooth floor you must place the schematic at the rigth y given by the program!

First of all download the `SmoothFloorSteps` litematic present in this repository.

Each region of the litematic contains the steps you have to take. Enable just 1 region per time.

This is the list of all the regions and what you have to do at each step:

### Steps
- Step0: Run the World Eater normally.
- Step1: Stop the World Eater when only 4 layers of the perimeter are left.
- Step2: Remove the AND-gate on the main side and some parts of the logic of both main and return, as shown in the schematic.
  - Place the 3 redstone blocks at the main side, as shown in the schematic.
  - Place 2 redstone blocks at the return side, as shown in the schematic.
  - Remove the AND-gate on the return side.
- Step3: Remove the first redstone block at the main side to start the World Eater again.
  - Wait for the sweepers to launch and remove the second redstone block at the main side.
- Step4: Remove the first redstone block at the return side to start the World Eater.
  - Build the flying machine at the top of the main side, as shown in the schematic.
- Step5: Launch the flying machine built in the precedent step to run the dupers.
  - Build the other flying machine to launch the dupers at the return side. Don't run it yet!
  - Replace the normal piston at the bottom of the sweepers with sticky pistons.
  - Build the flying machine at the bottom of the main side to start the sweepers.
- Step6: Run the machine to start the sweepers.
- Step7: Launch the flying machine to launch the dupers to the main side.

What is left to do is clear the last layer from liquids. You can do that by hand or with the classic 2x World Eater sweepers.

Congratulations! You have now got a perfect smooth floor!
