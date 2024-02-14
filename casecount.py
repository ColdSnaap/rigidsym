from rigid import *
from symdata import *
from itertools import combinations, combinations_with_replacement
import collections

def rigid_wyckoff_sym(rigid_type, sym_no):
        if rigid_type == 'Tetrahedron':
            wyckoff_sym = Tetrahedron(sym_no, 2.0).wyckoff_sym()
        if rigid_type == 'GeSe':
            wyckoff_sym = GeSe(sym_no, 2.0).wyckoff_sym()
        # print(wyckoff_sym)
        return wyckoff_sym


def total_atom_number_from_wyckoff(sym_no, wyckoff_list):
    count = 0
    # print(f'wyckoff_list:{wyckoff_list}')
    for i in wyckoff_list:
        # print(f'i:{i}')
        muti = sg[f'sg_{sym_no}'][i][0]
        count = count + muti
    return count


def uniq_site(sym_no, site):
    count = 0
    for i in sg[f'sg_{sym_no}'][site][2]:
        if i != 'x' and i != 'y' and i != 'z':
            count += 1
    if count == 3:
        return 'yes'
    else:
        return 'no'


def minimum_muti(sym_no, list):
    muti_list = []
    for i in list:
        muti_list.append(sg[f'sg_{sym_no}'][i][0])
    min_mumber = min(muti_list)
    # print(muti_list)
    return min_mumber


def common_elements_check(rigid_list, single1, single2, sym_no):
    # Convert lists to sets
    set1 = set(rigid_list)
    set2 = set(single1)
    set3 = set(single2)
    # Check for common elements
    common_between_1_and_2 = list(set1.intersection(set2))
    common_between_1_and_3 = list(set1.intersection(set3))
    common_between_2_and_3 = list(set2.intersection(set3))
    common_all_list = common_between_1_and_2 + common_between_1_and_3 + common_between_2_and_3
    common_all = list(set(common_all_list))
    result = 'no'
    for elem in common_all:
        if uniq_site(sym_no, elem) == 'yes':
            result = 'yes'
            break
    # if common_between_1_and_2 or common_between_1_and_3 or common_between_2_and_3:
    #     result = 'yes'
    # else:
    #     result = 'no'
    return result


def muti_comb(sym_no, single_or_rigid, uniq_or_general, rigid_type=None, rigid_limit=None, single_number=None):
    site_list = []
    rigid_list = []
    for key in sg[f'sg_{sym_no}'].keys():
        uniq_check = uniq_site(sym_no, key)
        if uniq_or_general == 'uniq' and uniq_check == 'yes':
            site_list.append(key)
        elif uniq_or_general == 'general' and uniq_check == 'no':
            site_list.append(key)

    if single_or_rigid == 'rigid':
        for i in site_list:
            i_sym = sg[f'sg_{sym_no}'][i][1]
            if i_sym in rigid_wyckoff_sym(rigid_type, sym_no):
                rigid_list.append(i)
        final_list = rigid_list.copy()
    elif single_or_rigid == 'single':
        final_list = site_list.copy()
    
    # print(f'final_list:{final_list}')
    com_list = []
    if len(final_list) >= 1:
        muti_min = minimum_muti(sym_no, final_list)
        # print(f'muti_min:{muti_min}')
        # print(f'single_number:{single_number}')
        if single_or_rigid == 'rigid':
            range_up = rigid_limit // muti_min
        elif single_or_rigid == 'single':
            range_up = single_number // muti_min
            # print(f'range_up:{range_up}')
        for i in range(1, range_up + 1):
            if uniq_or_general == 'uniq':
                comb = list(combinations(final_list, i))
            elif uniq_or_general == 'general':
                comb = list(combinations_with_replacement(final_list, i))
                # print(f'i:{i}')
                # print(f'comb:{comb}')
            for j in comb:
                site_inter = []
                if i == 1:
                    com_list.append([j[0]])
                else:
                    for k in j:
                        site_inter.append(k)
                    com_list.append(site_inter)
                    # print(f'site_inter:{site_inter}')
    return com_list


# list1 = [1, 2, 3]
# list2 = ['a', 'b', 'c']
# combinations = [(x, y) for x in list1 for y in list2]
# ratio = [1, 2, 3]
def uniq_general_comb(sym_no, ratio, rigid_type=None, rigid_max=None):
    # prepare three lists: uniq_com, general_comb, uniq_general_comb of rigid body
    uniq_com_list_ini = muti_comb(sym_no, 'rigid', 'uniq', rigid_type=rigid_type, rigid_limit=rigid_max)
    general_com_list_ini = muti_comb(sym_no, 'rigid', 'general', rigid_type=rigid_type, rigid_limit=rigid_max)
    uniq_com_list, general_com_list, uniq_genral_comb = [], [], []
    for i in uniq_com_list_ini:
        if total_atom_number_from_wyckoff(sym_no, i) <= rigid_max:
            uniq_com_list.append(i)
    for i in general_com_list_ini:
        # print(f'general_com_list_ini:{general_com_list_ini}')
        if total_atom_number_from_wyckoff(sym_no, i) <= rigid_max:
            general_com_list.append(i)
    uniq_genral_comb_ini_inter = [(uniq, general) for uniq in uniq_com_list for general in general_com_list]
    uniq_genral_comb_ini = []
    for i in uniq_genral_comb_ini_inter:
        ele_list = i[0] + i[1]
        uniq_genral_comb_ini.append(ele_list)
    for i in uniq_genral_comb_ini:
        if total_atom_number_from_wyckoff(sym_no, i) <= rigid_max:
            uniq_genral_comb.append(i)
    result_rigid = uniq_com_list + general_com_list + uniq_genral_comb
    
    #single comb list
    if len(ratio) == 2:
        single_number = ratio[1] * rigid_max
    elif len(ratio) == 3:
        single_number = max(ratio[1], ratio[2]) * rigid_max
    uniq_com_list_ini_single = muti_comb(sym_no, 'single', 'uniq', single_number=single_number)
    general_com_list_ini_single = muti_comb(sym_no, 'single', 'general', single_number=single_number)
    
    # get sinlge comb
    # rigid_comb = [[1,2],[2,3,4]]
    # case_numb = {rigid1}
    # case_dir = {case1:{rigid:[1, 2, 3]
    #                    single1:[2, 3, 4]
    #                    single2:[2, 3, 4]},
    #             case2:{rigid:[1, 2]
    #                    single1:[3, 5]
    #                    single2:[3]}}
    # ratio = [1, 1, 1]
    
    # single_type == 1
    case_dir, case_numb = {}, 0
    single_type_numb = len(ratio)
    # print(f'result_rigid:{result_rigid}')
    for rigid_comb in result_rigid:
        uniq_com_list_single, general_com_list_single, uniq_general_comb_single = [], [], []
        rigid_number = int(total_atom_number_from_wyckoff(sym_no, rigid_comb))
        type_ratio = ratio[1] / ratio[0]
        single_number = int(rigid_number * type_ratio)
        if type_ratio.is_integer() == False:
            print('ratio is not integer')
            exit()
        else:
            for i in uniq_com_list_ini_single:
                common_elements = list(set(rigid_comb).intersection(i))
                if total_atom_number_from_wyckoff(sym_no, i) < single_number and len(common_elements) == 0:
                    uniq_com_list_single.append(i)
                elif total_atom_number_from_wyckoff(sym_no, i) == single_number and len(common_elements) == 0:
                    case_numb += 1
                    if f'case{case_numb}' not in case_dir:
                        case_dir[f'case{case_numb}'] = {}
                    case_dir[f'case{case_numb}']['rigid'] = rigid_comb
                    case_dir[f'case{case_numb}'][f'single1'] = i
            for i in general_com_list_ini_single:
                if total_atom_number_from_wyckoff(sym_no, i) < single_number:
                    general_com_list_single.append(i)
                elif total_atom_number_from_wyckoff(sym_no, i) == single_number:
                    case_numb += 1
                    if f'case{case_numb}' not in case_dir:
                        case_dir[f'case{case_numb}'] = {}
                    case_dir[f'case{case_numb}']['rigid'] = rigid_comb
                    case_dir[f'case{case_numb}'][f'single1'] = i

            # print(f'rigid_comb:{rigid_comb}')
            # print(f'uniq_com_list_single:{uniq_com_list_single}')
            # print(f'general_com_list_single:{general_com_list_single}')
            # print('---------------------------------------------------')
            if len(uniq_com_list_ini_single) != 0 and len(general_com_list_ini_single) != 0:
                uniq_general_comb_single_inter = [(uniq, general) for uniq in uniq_com_list_single for general in general_com_list_single]
                uniq_general_comb_single = []
                for i in uniq_general_comb_single_inter:
                    ele_list = i[0] + i[1]
                    uniq_general_comb_single.append(ele_list)
                # print(f'uniq_com_list_single:{uniq_com_list_single}')
                # print(f'general_com_list_single:{general_com_list_single}')
                # print(f'uniq_general_comb_single:{uniq_general_comb_single}')
                for i in uniq_general_comb_single:
                    # print(i)
                    if total_atom_number_from_wyckoff(sym_no, i) == single_number:
                        case_numb += 1
                        if f'case{case_numb}' not in case_dir:
                            case_dir[f'case{case_numb}'] = {}
                        case_dir[f'case{case_numb}']['rigid'] = rigid_comb
                        case_dir[f'case{case_numb}'][f'single1'] = i

    # single_type == 2
    case_dir_2, case_numb = {}, 0
    uniq_com_list_single, general_com_list_single, uniq_general_comb_single = [], [], []
    # print single1 dir
    # for key in case_dir.keys():
    #     print(case_dir[key])
    # print('-----------------------------')
    # print(f'uniq_com_list_ini_single:{uniq_com_list_ini_single}')
    # print(f'general_com_list_ini_single:{general_com_list_ini_single}')
    # print(case_dir)
    if single_type_numb == 3:
        type_ratio = ratio[2] / ratio[0]
        if type_ratio.is_integer() == False:
            print('ratio is not integer')
            exit()
        else:
            for key in case_dir.keys():
                rigid_comb = case_dir[key]['rigid']
                single1_list = case_dir[key]['single1']
                rigid_number = int(total_atom_number_from_wyckoff(sym_no, rigid_comb))
                single_number = int(rigid_number * type_ratio)
                for i in uniq_com_list_ini_single:
                    # common_elements = list(set(rigid_comb).intersection(i, single1_list))
                    common_elements = common_elements_check(rigid_comb, i, single1_list, sym_no)
                    # print(f'key:{key}')
                    # print(f'rigid_comb:{rigid_comb}')
                    # print(f'i:{i}')
                    # print(f'single1_list:{single1_list}')
                    # print(f'common_elements:{common_elements}')
                    # print('------------------')
                    # if total_atom_number_from_wyckoff(sym_no, i) < single_number and len(common_elements) == 0:
                    if total_atom_number_from_wyckoff(sym_no, i) < single_number and common_elements == 'no':
                        uniq_com_list_single.append(i)
                    # elif total_atom_number_from_wyckoff(sym_no, i) == single_number and len(common_elements) == 0:
                    elif total_atom_number_from_wyckoff(sym_no, i) == single_number and common_elements == 'no':
                        case_numb += 1
                        if f'case{case_numb}' not in case_dir_2:
                            case_dir_2[f'case{case_numb}'] = {}
                        case_dir_2[f'case{case_numb}']['rigid'] = rigid_comb
                        case_dir_2[f'case{case_numb}'][f'single1'] = single1_list
                        case_dir_2[f'case{case_numb}'][f'single2'] = i
                for i in general_com_list_ini_single:
                    if total_atom_number_from_wyckoff(sym_no, i) < single_number:
                        general_com_list_single.append(i)
                    elif total_atom_number_from_wyckoff(sym_no, i) == single_number:
                        case_numb += 1
                        if f'case{case_numb}' not in case_dir_2:
                            case_dir_2[f'case{case_numb}'] = {}
                        case_dir_2[f'case{case_numb}']['rigid'] = rigid_comb
                        case_dir_2[f'case{case_numb}'][f'single1'] = single1_list
                        case_dir_2[f'case{case_numb}'][f'single2'] = i

                        # print(f'rigid:{rigid_comb}')
                        # print(f'single1:{single1_list}')
                        # print(f'single2:{i}')
                        # print('yes')
                        # for key in case_dir.keys():
                        #     print(case_dir[key])
                        # print('-------------')

                if len(uniq_com_list_ini_single) != 0 and len(general_com_list_ini_single) != 0:
                    uniq_general_comb_single_inter = [(uniq, general) for uniq in uniq_com_list_single for general in general_com_list_single]
                    uniq_general_comb_single = []
                    for i in uniq_general_comb_single_inter:
                        ele_list_single = i[0] + i[1]
                        uniq_general_comb_single.append(ele_list_single)
                    for i in uniq_general_comb_single:
                        if total_atom_number_from_wyckoff(sym_no, i) == single_number:
                            case_numb += 1
                            if f'case{case_numb}' not in case_dir_2:
                                case_dir_2[f'case{case_numb}'] = {}
                            case_dir_2[f'case{case_numb}']['rigid'] = rigid_comb
                            case_dir_2[f'case{case_numb}'][f'single1'] = single1_list
                            case_dir_2[f'case{case_numb}'][f'single2'] = i

    # print('-----------------------')
    # for key in case_dir_2.keys():
    #     print(case_dir_2[key])
    # get rid of the ones without single2 or two atoms at the same uniq wyckoff
    if single_type_numb == 2:
        case_dir_final = case_dir.copy()
        # case_dir_combine = case_dir['single'] = case_dir.pop('single1')
    elif single_type_numb == 3:
        case_dir_final, case_dir_combine, case_no = {}, {}, 0
        for key in case_dir_2.keys():
            if len(case_dir_2[key]) == 3:
                # single1_list = case_dir_2[key]['single1']
                # single2_list = case_dir_2[key]['single2']
                # common_elements = list(set(single1_list).intersection(set(single2_list)))
                # for i in common_elements:
                #     uniq_check = uniq_site(sym_no, i)
                #     if uniq_check == 'yes':
                #         break
                # if uniq_check == 'no':
                case_no += 1
                if f'case{case_no}' not in case_dir_final:
                    case_dir_final[f'case{case_no}'] = {}
                # print(f'case_dir_final:{case_dir_final}')
                # print(f'case_dir:{case_dir}')
                # print(f'case_no:{case_no}')
                case_dir_final[f'case{case_no}']['rigid'] = case_dir_2[key]['rigid']
                case_dir_final[f'case{case_no}']['single1'] = case_dir_2[key]['single1']
                case_dir_final[f'case{case_no}']['single2'] = case_dir_2[key]['single2']

                # case_dir_combine[f'case{case_no}']['rigid'] = case_dir_2[key]['rigid']
                # single_new_list = case_dir_2[key]['single1'] + case_dir_2[key]['single2']
                # case_dir_final[f'case{case_no}']['single'] = single_new_list
    
    return case_dir_final
