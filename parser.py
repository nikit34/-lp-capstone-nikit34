

def open_close_file(*name_args, **name_kwargs):
    if len(name_kwargs) > 0:
        if 'fin' in name_kwargs.keys() and 'fout' in name_kwargs.keys():
            fin = name_kwargs['fin']
            fout = name_kwargs['fout']
        elif 'fin' in name_kwargs.keys():
            fin = name_kwargs['fin']
            fout = None
        else:
            print("invalid args of decorator")
    else:
        print("invalid args of decorator")

    def decorator(func):
        def _file(*args, **kwargs):
            with open(fin[0], fin[1], encoding='utf8', errors='ignore') as f_input:
                if fout == None:
                    file_lines = f_input.readlines()
                    done = func(file_lines, *args, **kwargs)
                else:
                    with open(fout[0], fout[1]) as f_prolog:
                        file_lines = f_input.readlines()
                        done = func(file_lines, f_prolog, *args, **kwargs)
                        f_prolog.close()
                f_input.close()
            return done
        return _file
    return decorator


def menu():
    print("1 show by DATE TIME interval         [values]")
    print("2 show all occurrences by NAME       [values]")
    print("3 show all occurrences by CONTENT    [values]")
    print("4 start proc search direct parents   [values]")
    while 1:
        act = input('input: ')
        if next(filter(lambda x: x not in ['1', '2', '3', '4'], act), False):
            print("Invalid input")
        else:
            print(f"{act} - OK")
            yield act


# def gun_by_time():

@open_close_file(fin=('kennedy.ged', 'r'))
def show_by_time(file_lines, *args, **kwargs):
    near_year = 0
    old_year = 0
    count = -1
    while 1:
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


@open_close_file(fin=('kennedy.ged', 'r'))
def show_contains_name(file_lines, *args, **kwargs):
    search = 'NAME'
    if args[len(args) - 1] == '3': search = 'CONT'
    name = input(f"  enter {search} for search: ").lower()
    print("-------------------------------------------------------------")
    for i, line in enumerate(file_lines):
        split_line = line.split(' ', 2)
        if split_line[1] == search and split_line[2].lower().count(name):
            print(line)
    print("-------------------------------------------------------------")


@open_close_file(fin=('kennedy.ged', 'r'), fout=('prolog.pl', 'w'))
def run_proc_prolog(file_lines, f_prolog, *args, **kwargs):
    f_prolog.write("parent(X,Y) :- parents(Y,X,_).\n")
    f_prolog.write("parent(X,Y) :- parents(Y,_,X).\n")
    f_prolog.write("\n")
    f_prolog.write("father(X, Y) :- parents(Y, X, _).\n")
    f_prolog.write("mother(X, Y) :- parents(Y, _, X).\n")
    f_prolog.write("\n")
    f_prolog.write("male(X) :- father(X, _).\n")
    f_prolog.write("female(X) :- mother(X, _).\n")
    f_prolog.write("\n")
    f_prolog.write("grandfather(X, Y) :- father(X, Z), father(Z, Y).\n")
    f_prolog.write("grandfather(X, Y) :- father(X, Z), mother(Z, Y).\n")
    f_prolog.write("\n")
    f_prolog.write("grandmother(X, Y) :- mother(X, Z), mother(Z, Y).\n")
    f_prolog.write("grandmother(X, Y) :- mother(X, Z), father(Z, Y).\n")
    f_prolog.write("\n")
    f_prolog.write("brother(X, Y) :- male(X), father(Z, X), father(Z, Y), X \= Y.\n")
    f_prolog.write("sister(X, Y) :- female(X), father(Z, X), father(Z, Y), X \= Y.\n")
    f_prolog.write("\n")
    f_prolog.write("aunt(X,Y) :- sister(X,Z), parent(Z,Y).\n")
    f_prolog.write("uncle(X, Y) :- brother(X, Z), parent(Z,Y).\n")
    unit = {}
    units = {}
    border = 0
    for i, line in enumerate(file_lines, start=1):
        split_line = [x.strip() for x in line.split(' ', 2)]
        if len(split_line) == 3:
            if split_line[2] == 'INDI' and 'id' in unit and 'name' in unit and unit['name']['i'] > border:
                tmp_dict_id = unit['id']
                units[tmp_dict_id] = { 'name': unit['name']['item'] }
                if 'sex' in unit and unit['sex']['i'] > border:
                    units[tmp_dict_id].update({'sex': unit['sex']['item'] })
                if 'famc' in unit and unit['famc']['i'] > border:
                    units[tmp_dict_id].update({ 'famc': unit['famc']['item'] })
                if 'fams' in unit and unit['fams']['i'] > border:
                    units[tmp_dict_id].update({ 'fams': unit['fams']['item'] })
                if 'husb' in unit and unit['husb']['i'] > border:
                    units[tmp_dict_id].update({ 'husb': unit['husb']['item'] })
                if 'chil' in unit and unit['chil']['i'] > border:
                    units[tmp_dict_id].update({ 'chil': unit['chil']['item'] })
                if 'wife' in unit and unit['wife']['i'] > border:
                    units[tmp_dict_id].update({ 'wife': unit['wife']['item'] })
                border = i
                unit = {}
            elif split_line[1] == 'NAME' and 'id' in unit:
                unit['name'] = { 'item': split_line[2], 'i': i }
            elif split_line[1] == 'SEX':
                unit['sex'] = { 'item': split_line[2], 'i': i }
            elif split_line[1] == 'FAMC':
                unit['famc'] = { 'item': split_line[2], 'i': i }
            elif split_line[1] == 'FAMS':
                unit['fams'] = { 'item': split_line[2], 'i': i }
            elif split_line[1] == 'HUSB':
                unit['husb'] = { 'item': split_line[2], 'i': i }
            elif split_line[1] == 'CHIL':
                unit['chil'] = { 'item': split_line[2], 'i': i }
            elif split_line[1] == 'WIFE':
                unit['wife'] = { 'item': split_line[2], 'i': i }
            elif split_line[2] == 'INDI':
                unit['id'] = split_line[1]
    print(units)


if __name__ == "__main__":
    act = -1
    while act != 0:
        act = next(menu())
        if act == '1':
            gun_line = show_by_time()
            try:
                while 1:
                    print(next(gun_line))
            except StopIteration:
                print("  finish")
        if act == '2' or act == '3': show_contains_name(act)
        if act == '4': run_proc_prolog()
