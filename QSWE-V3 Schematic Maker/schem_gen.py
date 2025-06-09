from typing import Tuple
import argparse
import sys
import os

from litemapy import Schematic, Region, BlockState


MIN_SIZE_X = 18
MIN_SIZE_Z = 29


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for PyInstaller"""

    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    
    return os.path.join(os.path.abspath("."), relative_path)


def concatenate_regions(reg1: Region, reg2: Region, x: int=0, y: int=0, z: int=0) -> Region:
    """
    Utility method to paste reg2 into reg2 at the given coordinates.
    Resizes the region if needed
    """

    w = max(reg2.width  + x, reg1.width)
    h = max(reg2.height + y, reg1.height)
    l = max(reg2.length + z, reg1.length)

    if w != reg1.width or h != reg1.height or l != reg1.length:

        reg = Region(reg1.x, reg1.y, reg1.z, w, h, l)
    
        for bx, by, bz in reg1.block_positions():
            reg[bx, by, bz] = reg1[bx, by, bz]
        
    else:
        reg = reg1

    for bx, by, bz in reg2.block_positions():
        reg[bx + x, by + y, bz + z] = reg2[bx, by, bz]

    return reg


class QsweMaker:
    """
    Tiles the schematic for the QSWE and calculates the rigth sizes and height
    """

    _main_logic: Region
    _main_dupers_stack: Region
    _main_sweepers_stack: Region
    _main_sweepers_end: Region
    _return_logic: Region
    _return_dupers_stack: Region
    _return_sweepers_stack: Region
    _return_sweepers_end: Region


    def __init__(self, schem_to_load: str="SM.litematic") -> "QsweMaker":

        sm_litematic = Schematic.load(resource_path(schem_to_load))

        self._main_logic = sm_litematic.regions["MainLogic"]
        self._main_dupers_stack = sm_litematic.regions["MainDupersStack"]
        self._main_sweepers_stack = sm_litematic.regions["MainSweepersStack"]
        self._main_sweepers_end = sm_litematic.regions["MainSweepersEnd"]

        self._return_logic = sm_litematic.regions["ReturnLogic"]
        self._return_dupers_stack = sm_litematic.regions["ReturnDupersStack"]
        self._return_sweepers_stack = sm_litematic.regions["ReturnSweepersStack"]
        self._return_sweepers_end = sm_litematic.regions["ReturnSweepersEnd"]


    @classmethod
    def calculate_sizes(self, x: int, z: int) -> Tuple[int]:
        """
        Calculate the rigth sizes for the world eater
        """

        if x % 6 != 0:
            x = 6 + (x // 6) * 6

        return max(x, MIN_SIZE_X) , max(MIN_SIZE_Z, z)


    @classmethod
    def calculate_initial_height(self, start: int, end: int) -> int:
        """
        Given the max terrain height and the point where the WE should stop, calculates the exact WE y
        """

        return start + (start - end) % 4


    def generate_trenches_outline(self, size_x: int, size_z: int) -> Region:
        """
        Builds the trenches outline with leaves
        """

        trenches_outline_region = Region(0, 0, 0, size_x, 1, size_z)

        for x in range(size_x):
            trenches_outline_region[x, 0, 0]          = BlockState("minecraft:spruce_leaves")
            trenches_outline_region[x, 0, size_z - 1] = BlockState("minecraft:spruce_leaves")

        for z in range(size_z):
            trenches_outline_region[         0, 0, z] = BlockState("minecraft:spruce_leaves")
            trenches_outline_region[size_x - 1, 0, z] = BlockState("minecraft:spruce_leaves")

        for x in range(1, size_x - 2):
            trenches_outline_region[x, 0, 1]          = BlockState("minecraft:oak_leaves")
            trenches_outline_region[x, 0, size_z - 2] = BlockState("minecraft:oak_leaves")

        for z in range(1, size_z - 2):
            trenches_outline_region[         1, 0, z] = BlockState("minecraft:oak_leaves")
            trenches_outline_region[size_x - 2, 0, z] = BlockState("minecraft:oak_leaves")
    
        for x in range(4, size_x - 4):
            trenches_outline_region[x, 0, 13]          = BlockState("minecraft:spruce_leaves")
            trenches_outline_region[x, 0, size_z - 14] = BlockState("minecraft:spruce_leaves")

        for x in range(3, size_x - 3):
            trenches_outline_region[x, 0, 12]          = BlockState("minecraft:oak_leaves")
            trenches_outline_region[x, 0, size_z - 13] = BlockState("minecraft:oak_leaves")
    
        for z in range(14, size_z - 14):
            trenches_outline_region[4,          0, z] = BlockState("minecraft:spruce_leaves")
            trenches_outline_region[size_x - 5, 0, z] = BlockState("minecraft:spruce_leaves")

        for z in range(13, size_z - 13):
            trenches_outline_region[3,          0, z] = BlockState("minecraft:oak_leaves")
            trenches_outline_region[size_x - 4, 0, z] = BlockState("minecraft:oak_leaves")

        return trenches_outline_region


    def generate_main_side(self, size_x: int) -> Region:
        """
        Generates the main side of the WE
        """
    
        main_side = Region(1, 2, 1, size_x - 4, 88, 11)
        main_side = concatenate_regions(main_side, self._main_logic, 0, 0, 0)

        for x in range(9, size_x - 14, 6):
            main_side = concatenate_regions(main_side, self._main_sweepers_stack, x, 1, 0)
            main_side = concatenate_regions(main_side, self._main_dupers_stack, x, 82, 6)

        main_side = concatenate_regions(main_side, self._main_sweepers_end, size_x - 11, 1, 0)
        main_side = concatenate_regions(main_side, self._main_dupers_stack, size_x - 11, 82, 6)
    
        return main_side


    def generate_return_side(self, size_x: int, size_z: int) -> Region:
        """
        Generates the return side of the WE
        """

        return_side = Region(1, 4, size_z - 17, size_x - 4, 84, 16)
        return_side = concatenate_regions(return_side, self._return_logic, 0, 0, -1)

        for x in range(9, size_x - 14, 6):
            return_side = concatenate_regions(return_side, self._return_sweepers_stack, x, 0, -1)
            return_side = concatenate_regions(return_side, self._return_dupers_stack, x, 81, 4)

        return_side = concatenate_regions(return_side, self._return_sweepers_end, size_x - 11, 0, -1)
        return_side = concatenate_regions(return_side, self._return_dupers_stack, size_x - 11, 81, 4)

        return return_side


    def generate_schematic(self, size_x: int, size_z: int) -> Schematic:
        """
        Generate a schematic of the WE with the given sizes
        """

        trenches_outline = self.generate_trenches_outline(size_x + 2, size_z + 2)
        main_side = self.generate_main_side(size_x + 2)
        return_side = self.generate_return_side(size_x + 2, size_z + 2)

        schematic = Schematic(
            name=f"QSWE-V3 {size_x}x{size_z}",
            author="QSWE-MakerByAttila",
            regions={
                "Trenches": trenches_outline,
                "Main": main_side,
                "Return": return_side
            }
        )

        schematic.save(f"QSWE-V3 {size_x}x{size_z}.litematic")


def sizes(args):

    x, z = QsweMaker.calculate_sizes(args.x, args.z)
    dx = x - args.x
    dz = z - args.z
    xs = str(x)
    zs = str(z)

    if dx > 0:
        xs += f" (+{dx})"
        
    if dz > 0:
        zs += f" (+{dz})"

    print(f"Suggested sizes: {xs}, {zs}")

    inp = input(f"Want to generate a {x}x{z} WE schematic? (y/n) ") or "n"

    if inp.strip().lower() == "y":
        
        schem(argparse.Namespace(x=x, z=z))


def schem(args):

    schem_maker = QsweMaker()

    x, z = schem_maker.calculate_sizes(args.x, args.z)

    if x != args.x or z != args.z:
        
        sizes(args)
        return

    print("Making the schematic...")
    schem_maker.generate_schematic(x, z)
    print("Done!")

    inp = input(f"Want to know at what height place the WE? (y/n) ") or "n"

    if inp.strip().lower() == "y":
        
        start = int(input("Start y: "))
        end = int(input("End y: (default=-59) ") or -59)

        args.start = start
        args.end = end
        height(args)


def height(args):

    y = QsweMaker.calculate_initial_height(args.start, args.end)

    print(f"Right height: Y={y}")


def main():

    parser = argparse.ArgumentParser(description="QSWE Schematic Maker")
    subparsers = parser.add_subparsers(dest="command")

    # sizes command
    parser_sizes = subparsers.add_parser("sizes", help="Get valid WE sizes")
    parser_sizes.add_argument("x", type=int, help="X (width) of the perimeter")
    parser_sizes.add_argument("z", type=int, help="Z (length) of the perimeter")

    # height command
    parser_height = subparsers.add_parser("height", help="Suggest rigth build height")
    parser_height.add_argument("start", type=int, help="Start YEnd location or target Y")
    parser_height.add_argument("end", type=int, nargs="?", help="End location or target Y (defaults to -59)", default=-59)

    # schem command
    parser_schem = subparsers.add_parser("schem", help="Generate QSWE schematic")
    parser_schem.add_argument("x", type=int, help="Width of the perimeter")
    parser_schem.add_argument("z", type=int, help="Length of the perimeter")

    args = parser.parse_args()
    {
        "sizes": sizes,
        "height": height,
        "schem": schem
    }.get(
        args.command, lambda a: parser.print_help()
    )(args)


if __name__ == "__main__":
    main()