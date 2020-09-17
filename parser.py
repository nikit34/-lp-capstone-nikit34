from functools import reduce


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
            with open(fin[0], fin[1]) as f_input:
                with open(fout[0], fout[1]) as f_prolog:
                    done = func(f_input, fin, *args, **kwargs)
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

@open_close_file(fin=('royal_gen_20_11_2002.ged', 'rb'), fout=('proc_family.pl', 'wb'))
def show_by_time(file, fin, *args, **kwargs):
    near_year = 0
    old_year = 0
    while True:
        print("  enter time interval\n  in follow format\n  [one year / 4 symb] [second year / 4 symb]")
        # interval = input().split()
        interval = ['1000', '2003']
        if len(interval) == 2:
            near_year = int(interval[0])
            old_year = int(interval[1])
            if  old_year > near_year:
                old_year, near_year = near_year, old_year
            break
        else:
            print("  invalid data format")
    select_chan = []
    with open(fin[0], fin[1]) as tmp_file:
        for i, line in enumerate(file.readlines()):
            split_line = line.split(b' ', 2)
            if len(split_line) > 2 and split_line[1] == b'DATE':
                year = ''.join(x for x in str(split_line[2].split()[-1]) if x.isdigit())
                if len(year) > 2 and int(year) > old_year and int(year) < near_year:
                    tmp_lines = []
                    for j, tmp_line in enumerate(tmp_file.readlines()):
                        k = 0
                        if j >= i - 20 and j <= i:
                            tmp_lines.append(tmp_line)
                        if j == i:
                            if j > 20:
                                k = 20
                            else:
                                k = j
                            while k >= 0 and tmp_lines[k - 1].split(b' ', 2)[1] != b'CHAN':
                                select_chan.append(tmp_lines[k - 1])
                                k -= 1
                        if j > i:
                            if tmp_line.split(b' ', 2)[1] != b'CHAN' and j <= i + 20:
                                select_chan.append(tmp_line)
                            else:
                                break
    tmp_file.close()

    for s in select_chan:
        print(s)
    # file.write(line)


@open_close_file(fin=('royal_gen_20_11_2002.ged', 'rb'), fout=('proc_family.pl', 'wb'))
def show_countries():
    print("c")







# if __name__ == "__main__":
#     act = -1
#     while act != 0:
#         act = next(menu())
#         if act == 1: show_by_time()
#         if act == 2: show_countries()


show_by_time()