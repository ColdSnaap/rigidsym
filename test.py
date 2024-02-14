from casecount import *
from readinginput import *
from pymatgen.io.vasp import Poscar
from pymatgen.io.cif import CifWriter
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# Load the structure from the POSCAR file
poscar = Poscar.from_file("CONTCAR")
structure = poscar.structure

# Analyze the structure to find the space group
space_group_analyzer = SpacegroupAnalyzer(structure, 1)
space_group_symbol = space_group_analyzer.get_space_group_symbol()
space_group_number = space_group_analyzer.get_space_group_number()

print(f"Space Group Symbol: {space_group_symbol}")
print(f"Space Group Number: {space_group_number}")

# Create a CIF writer object
cif_writer = CifWriter(structure, 0.1)

# Write the CIF file
cif_writer.write_file("output.cif")
# print(ratio)
# for x in ratio:
#     print(type(x))
# rigid_comb = ['s1']
# single1_comb = ['s1']
# i = ['s2']

# x = common_elements_check(rigid_comb, i, single1_comb, 62)
# print(x)
# for sym_no in range(80, 200):
#     if f'sg_{sym_no}' in sg:
#         y = uniq_general_comb(sym_no, ratio, rigid_type, rigid_max)
#         print(f'{sym_no} {len(y)}')
#         # print(y)

