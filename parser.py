

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
                    done = func(file_lines, fin, *args, **kwargs)
                    f_prolog.close()
                f_input.close()
            return done
        return _file
    return decorator


def menu():
    print("1 show by DATE TIME interval    [values]")
    print("2 show all COUNTRIES            [values]")
    while True:
        print("input:", end = ' ')
        act = input()
        #act = '1'
        if next(filter(lambda x: x not in ['1', '2'], act), False):
            print("Invalid input")
        else:
            print(f"{act} - OK")
            yield act

@open_close_file(fin=('royal_gen_20_11_2002.ged', 'r'), fout=('proc_family.pl', 'wb'))
def show_by_time(file_lines, fin, *args, **kwargs):
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
                        if j >= i - 3 and j < i:
                            tmp_lines.append(tmp_line.replace('//', '').replace('/-/', '').strip())
                        elif j == i:
                            tmp_lines.append(tmp_line.replace('//', '').replace('/-/', '').strip())
                            if j > 3:
                                k = 3
                            else:
                                k = j
                            while k >= 0 and tmp_line.split(' ', 2)[1] != 'CHAN':
                                select_chan.append(tmp_lines[k].replace('//', '').replace('/-/', '').strip())
                                k -= 1
                        elif j > i:
                            if tmp_line.split(' ', 2)[1] != 'CHAN' and j <= i + 3:
                                select_chan.append(tmp_line.replace('//', '').replace('/-/', '').strip())
                            else:
                                yield select_chan
                                break
        else:
            break



@open_close_file(fin=('royal_gen_20_11_2002.ged', 'r'), fout=('proc_family.pl', 'wb'))
def show_countries():
    print("c")







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
        if act == '2': show_countries()
