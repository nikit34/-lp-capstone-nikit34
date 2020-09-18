

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
    print("1 show by DATE TIME interval    [count]")
    print("2 show all COUNTRIES            [count]")
    while True:
        print("input:", end = ' ')
        act = input()
        if next(filter(lambda x: x not in ['1', '2'], act), False):
            print("Invalid input")
        else:
            print(f"{act} - OK")
            yield act

@open_close_file(fin=('royal_gen_20_11_2002.ged', 'r'), fout=('proc_family.pl', 'wb'))
def show_by_time(file_lines, fin, *args, **kwargs):
    near_year = 0
    old_year = 0
    while True:
        print("  enter time interval\n  in follow format\n  [one year / 4 symb] [second year / 4 symb]")
        # interval = input().split()
        interval = ['2000', '2003']
        if len(interval) == 2:
            near_year = int(interval[0])
            old_year = int(interval[1])
            if  old_year > near_year:
                old_year, near_year = near_year, old_year
            break
        else:
            print("  invalid data format")
    for i, line in enumerate(file_lines):
        split_line = line.split(' ', 2)
        if len(split_line) > 2 and split_line[1] == 'DATE':
            year = ''.join(x for x in str(split_line[2].split()[-1]) if x.isdigit())
            if len(year) > 2 and int(year) > old_year and int(year) < near_year:
                select_chan = []
                tmp_lines = []
                for j, tmp_line in enumerate(file_lines):
                    if j >= i - 3 and j < i:
                        tmp_lines.append(tmp_line)
                    elif j == i:
                        tmp_lines.append(tmp_line)
                        if j > 3:
                            k = 3
                        else:
                            k = j
                        while k >= 0 and tmp_line.split(' ', 2)[1] != 'CHAN':
                            select_chan.append(tmp_lines[k])
                            k -= 1
                    elif j > i:
                        if tmp_line.split(' ', 2)[1] != 'CHAN' and j <= i + 3:
                            select_chan.append(tmp_line)
                        else:
                            yield select_chan
                            break



@open_close_file(fin=('royal_gen_20_11_2002.ged', 'r'), fout=('proc_family.pl', 'wb'))
def show_countries():
    print("c")







# if __name__ == "__main__":
#     act = -1
#     while act != 0:
#         act = next(menu())
#         if act == 1: show_by_time()
#         if act == 2: show_countries()

g = show_by_time()
for i in range(1000):
    print(next(g))