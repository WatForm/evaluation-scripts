import os
import csv
from typing import *
import re
import sys

from tqdm.auto import tqdm

BENCHMARK_LOCATION = '../benchmarks/UFNIA/'

def find_files(folder_path: os.PathLike, recursive: bool,
                              folder_filter: Optional[Callable[[Union[bytes, str]], bool]] = None,
                              file_filter: Optional[Callable[[Union[bytes, str]], bool]] = None,
                              abs_path: bool = True,
                              ) -> List[str]:
        files_kept = []
        for root, dirs, files in os.walk(folder_path):
            # Filter or keep files
            for file_name in files:
                file_name_from_root = os.path.join(root, file_name)
                if file_filter is None or file_filter(file_name_from_root):
                    if abs_path:
                        # This is the absolute path from the file system root
                        files_kept.append(os.path.abspath(file_name_from_root))
                    else:
                        files_kept.append(file_name_from_root)
                        
            # If we don't want to recurse into directories, skip them all
            if not recursive:
                dirs.clear()
            elif folder_filter is not None:
                #  Filter or keep folders for recursive calls
                dirs[:] = filter(lambda dir: folder_filter(os.path.join(root, dir)), dirs)
            
        return files_kept

regex = r"\(set-info :status ([^\)]*)\)"
info_matcher = re.compile(regex)
def file_condition(filename):
    with open(filename, 'r') as file:
        for line in file:
            attempt = info_matcher.search(line)
            if attempt is not None:
                return attempt.group(1).lower()
    print(f'WARN: unsure file {filename}', sys.stderr)
    return 'unsure'
    
print('Finding files...')
all_possible_files = find_files(BENCHMARK_LOCATION, True, file_filter=lambda x: x.endswith('.smt2'))
num_files = len(all_possible_files)
print(f'Found {num_files} files.')

sat_files = []
unsat_files = []
unknown_files = []
unsure_files = []

for file in tqdm(all_possible_files, total=num_files, desc='Finding Status'):
    condition = file_condition(file)
    file_line = file.strip() + '\n'
    if condition == 'sat':
        sat_files.append(file_line)
    elif condition == 'unsat':
        unsat_files.append(file_line)
    elif condition == 'unknown':
        unknown_files.append(file_line)
    else:
        unsure_files.append(file_line)

print('Writing output.')
with open('sat_list.txt', 'w') as sat_list:
    sat_list.writelines(sat_files)

with open('unsat_list.txt', 'w') as unsat_list:
    unsat_list.writelines(unsat_files)

with open('unknown_list.txt', 'w') as unknown_list:
    unknown_list.writelines(unknown_files)

with open('unsure_list.txt', 'w') as unsure_list:
    unsure_list.writelines(unsure_files)