

def open_close_file(*name_args, **name_kwargs):
    if len(name_args) == 2 and len(name_kwargs) == 1 or len(name_kwargs) == 2:
        if 'fin' in name_kwargs.keys() and 'fout' in name_kwargs.keys():
            fin = name_kwargs['fin']
            fout = name_kwargs['fout']
        elif 'fin' in name_kwargs.keys():
            fin = name_kwargs['fin']
            fout = (name_args)
        elif 'fout' in name_kwargs.keys():
            fout = name_kwargs['fout']
            fin = (name_args)
        else:
            print("invalid args of decorator")
    else:
        print("invalid args of decorator")

    def decorator(func):
        def _file(*args, **kwargs):
            with open(fin[0], fin[1], encoding='utf8', errors='ignore') as f_input:
                with open(fout[0], fout[1]) as f_prolog:
                    file_lines = f_input.readlines()
                    done = func(file_lines, *args, **kwargs)
                    f_prolog.close()
                f_input.close()
            return done
        return _file
    return decorator


def menu():
    print("1 show by DATE TIME interval         [values]")
    print("2 show all occurrences by NAME       [values]")
    print("3 show all occurrences by NIKNAME    [values]")
    while True:
        act = input('input: ')
        if next(filter(lambda x: x not in ['1', '2', '3'], act), False):
            print("Invalid input")
        else:
            print(f"{act} - OK")
            yield act

@open_close_file(fin=('Ragusan.ged', 'r'), fout=('proc_family.pl', 'wb'))
def show_by_time(file_lines, *args, **kwargs):
    near_year = 0
    old_year = 0
    count = -1
    while True:
        print("  enter time interval\n  in follow format\n  [one year / 4 symb] [second year / 4 symb] [count or 'all']")
        interval = input().split()
        if len(interval) > 1:
            near_year = int(interval[0])
            old_year = int(interval[1])
            if len(interval) == 3 and interval[2].lower() != 'all':
                count = int(interval[2])
            if old_year > near_year:
                old_year, near_year = near_year, old_year
            break
        else:
            print("  invalid data format")

    c = 0
    for i, line in enumerate(file_lines):
        if count > c or count == -1:
            split_line = line.split(' ', 2)
            if len(split_line) > 2 and split_line[1] == 'DATE' and len(split_line[2]) > 2:
                year = ''.join(x for x in str(split_line[2].strip().split()[-1].lstrip()) if x.isdigit())
                if len(year) > 2 and int(year) >= old_year and int(year) < near_year:
                    select_chan = []
                    tmp_lines = []
                    c += 1
                    for j, tmp_line in enumerate(file_lines):
                        if j >= i - 10 and j < i:
                            tmp_lines.append(tmp_line.replace('//', '').replace('/-/', '').strip())
                        elif j == i:
                            tmp_lines.append(tmp_line.replace('//', '').replace('/-/', '').strip())
                            if j > 10:
                                k = 10
                            else:
                                k = j
                            while k >= 0 and tmp_line.split(' ', 2)[0] != '0':
                                select_chan.append(tmp_lines[k].replace('//', '').replace('/-/', '').strip())
                                k -= 1
                        elif j > i:
                            if tmp_line.split(' ', 2)[0] != '0' and j <= i + 10:
                                select_chan.append(tmp_line.replace('//', '').replace('/-/', '').strip())
                            else:
                                yield select_chan
                                break
        else:
            break



@open_close_file(fin=('Ragusan.ged', 'r'), fout=('proc_family.pl', 'wb'))
def show_contains_name(file_lines, *args, **kwargs):
    search = 'NAME'
    if args[0] == '3': search = 'CONT'
    name = input(f"  enter {search} for search: ").lower()
    print("-------------------------------------------------------------")
    for i, line in enumerate(file_lines):
        split_line = line.split(' ', 2)
        if split_line[1] == search and split_line[2].lower().count(name):
            print(line)
    print("-------------------------------------------------------------")




if __name__ == "__main__":
    act = -1
    while act != 0:
        act = next(menu())
        if act == '1':
            g = show_by_time()
            try:
                while True:
                    print(next(g))
            except StopIteration:
                print("  finish")
        if act == '2' or act == '3': show_contains_name(act)
