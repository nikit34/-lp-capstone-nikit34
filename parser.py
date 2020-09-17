from functools import reduce

def menu():
    print("1 show all email     [count]")
    print("2 show all countries [count]")
    while True:
        print("input:", end = ' ')
        act = input()
        if next(filter(lambda x: x not in ['1', '2'], act), False):
            print("Invalid input")
        else:
            print(f"{act} - OK")
            yield act

# @open_close_file('royal_gen_20_11_2002.ged', 'rb')
def show_email():
    print("e")

# @open_close_file('royal_gen_20_11_2002.ged', 'rb')
def show_countries():
    print("c")

def open_close_file(*name, **kwargs):
    if len(name) == 2 and len(kwargs) == 1 or len(kwargs) == 2:
        if 'fin' in kwargs.keys() and 'fout' in kwargs.keys():
            fin = kwargs['fin']
            fout = kwargs['fout']
        elif 'fin' in kwargs.keys():
            fin = kwargs['fin']
            fout = (name)
        elif 'fout' in kwargs.keys():
            fout = kwargs['fout']
            fin = (name)
        else:
            print("invalid args of decorator")
    else:
        print("invalid args of decorator")

    def decorator(func):
        def _file(*args, **kwargs):
            with open(fin[0], fin[1]) as f_input:
                with open(fout[0], fout[1]) as f_prolog:
                    done = func(*args, **kwargs)
                    for i, line in enumerate(f_input.readlines()):
                        if i == 10000:
                            break
                        split_line = line.split(b" ", 2)
                        if split_line[1] == b'EMAIL':
                            print(line.split(b" ", 2))
                        # f_prolog.write(line)
                    f_prolog.close()
                f_input.close()
            return done
        return _file
    return decorator





# if __name__ == "__main__":
#     act = -1
#     while act != 0:
#         act = next(menu())
#         if act == 1: show_email()
#         if act == 2: show_countries()
@open_close_file(fin=('royal_gen_20_11_2002.ged', 'rb'), fout=('proc_family.pl', 'wb'))
def test():
    print(2)
    return 3

print(test())