﻿# Отчет по курсовому проекту
## по курсу "Логическое программирование"

### студент: Пермяков Н.А.

## Результат проверки

| Преподаватель     | Дата         |  Оценка       |
|-------------------|--------------|---------------|
| Сошников Д.В. |              |               |
| Левинская М.А.|              |               |



## Введение

В результате выполнения курсового проекта будут получены и применены навыки логического и функционального программирования при решении реалистичной задачи. Курсовой проект содержит построенное и проанализированное родословное дерево Кеннеди, 35-го президента США с семью поколениями.

## Задание

 1. Создать родословное дерево своего рода на несколько поколений (3-4) назад в стандартном формате GEDCOM с использованием сервиса MyHeritage.com 
 2. Преобразовать файл в формате GEDCOM в набор утверждений на языке Prolog, используя следующее представление: parents(потомок, отец, мать).
 3. Реализовать предикат проверки/поиска шурина 
 4. Реализовать программу на языке Prolog, которая позволит определять степень родства двух произвольных индивидуумов в дереве
 5. [На оценки хорошо и отлично] Реализовать естественно-языковый интерфейс к системе, позволяющий задавать вопросы относительно степеней родства, и получать осмысленные ответы. 

## Получение родословного дерева

С помощью программы "My Family Tree" и открытых источников данных было составленно неполное родословное дерево глубиной в 7 поколений. Генеалогическое древо покрывает временной промежуток с 1984г. по 1858г. (крайние известные даты рождения).  
Ссылка на ресурс: https://www.microsoft.com/ru-ru/p/my-family-tree/9nblggh2k2xc

## Конвертация родословного дерева

Для преобразования файла в словарь утверждений использовался Python 3.6. Для реализации предиката проверки и поиска с целью определения степени родства двух произвольных индивидуумов в дереве использовался Prolog.

> Декоратор открытия - закрытия файла

    def  open_close_file(*name_args, **name_kwargs):
	    if  len(name_kwargs) > 0:
		    if  'fin'  in name_kwargs.keys() and  'fout'  in name_kwargs.keys():
			    fin = name_kwargs['fin']
			    fout = name_kwargs['fout']
		    elif  'fin'  in name_kwargs.keys():
			    fin = name_kwargs['fin']
			    fout = None
		    else:
			    print("invalid args of decorator")
	    else:
		    print("invalid args of decorator")
	    def  decorator(func):
		    def  _file(*args, **kwargs):
			    with  open(fin[0], fin[1], encoding='utf8', errors='ignore') as f_input:
				    if fout == None:
					    file_lines = f_input.readlines()
					    done = func(file_lines, *args, **kwargs)
					else:
						with  open(fout[0], fout[1]) as f_prolog:
						    file_lines = f_input.readlines()
						    done = func(file_lines, f_prolog, *args, **kwargs)
					    f_prolog.close()
				    f_input.close()
			    return done
		    return _file
    return decorator

	Декоратор нужен для безопасной работы с файлом, при выходе из исполняемой функции "func" оба файла закрываются в контекстном менеджере, что позволяет избежать утечек памяти. Аргументы "func" передаются в переменных "*args" "**kwargs" с последующей распаковкой.

## Предикат поиска родственника

Приведенный ниже фрагмент генератора необходим для  поиска родственника в заданным пользователем временном окне.
На вход функции передается список строк файла, по которым в цикле прверяем на совпадения условий фильтра и одной из колонок файла. Как только находим крайнюю дату - запускается еще один цикл для сбора ранних строк и последующих, относящихся к крайней дате. Затем это повторяется до следующей границы временного промежутка. Собранная информация по одному человеку передается на выход генератору. Осуществляются "ленивые запросы".

    if  len(year) > 2  and  int(year) >= old_year \
        and  int(year) < near_year:
	    select_chan = []
	    tmp_lines = []
	    c += 1
	    for j, tmp_line in  enumerate(file_lines):
		    if j >= i - 10  and j < i:
			    tmp_lines.append(tmp_line.replace('//', '').replace('/-/', '').strip())
		    elif j == i:
			    tmp_lines.append(tmp_line.replace('//', '').replace('/-/', '').strip())
			    if j > 10:
				    k = 10
			    else:
				    k = j
				    while k >= 0  and tmp_line.split(' ', 2)[0] != '0':
					    select_chan.append(tmp_lines[k].replace('//', '').replace('/-/', '').strip())
					    k -= 1
			elif j > i:
				if tmp_line.split(' ', 2)[0] != '0'  and j <= i + 10:
					select_chan.append(tmp_line.replace('//', '').replace('/-/', '').strip())
				else:
					yield select_chan
				break

## Определение степени родства

`file_lines` содержит итерируемый объект списка строк
`split_line` получает на вход очищенные столбцы от символов разделения (т.к. файл читаем в `urf-8` без "encoding to decoding".
валидируем по количеству столбцов, так как исходный набор содержит пропущенные значения
Блок с условием формирует словарь для записи об одном человеке и присоединяет к общему набору
Блок с проверкой `split_line[2] == 'FAM'` обрабатывает нижнюю часть файла с правками пользователей о составе семей.
Данные взятые из справок составляют 1/3 от общего объема сгенерированных выражений.

Второй цикл `for` 
словарь`family` будет являться буффером для каждой семьи. 
переменная `other` - второй экземпляр члена родословни, по условиям сравнивается с первым экземпляром, если поля не совпадают по `id` , что показывает что человек сам себе не брат, но совпадают по `INDI` с определенными полями - то, `other` может быть матерью либо отцом для `unit`.

Следующий блок делает то же самое но с другим набором полей, столбцов и условий.
  
Функция не делима по причине большого количества связанных переменных. Можно разделить только путем создания еще одного цикла на первом уровне, что понизит производительность. Измерено с помощью `cProfilling` и `pref_counter`.

Завершающий `for` заменяет символы из набора в списке для установки в prolog файл в виде переменных.

    for i, line in enumerate(file_lines, start=1):
        split_line = [x.strip() for x in line.split(' ', 2)]
        if len(split_line) == 3:
            if split_line[2] == 'INDI' and 'id_unit' in unit and 'name' in unit and unit['name']['i'] > border:
                tmp = { 'id_unit':  unit['id_unit'] }
                tmp.update({ 'name': unit['name']['item'] })
                for tag in ['sex', 'famc', 'fams',]:
                    if tag in unit and unit[tag]['i'] > border:
                        tmp.update({ tag: unit[tag]['item'] })
                units.append(tmp)
                border = i
                unit = {}
            elif split_line[2] == 'INDI':
                unit['id_unit'] = split_line[1]
            else:
                for tag in ['NAME', 'SEX', 'FAMC', 'FAMS']:
                    if split_line[1] == tag:
                        unit[tag.lower()] = { 'item': split_line[2], 'i': i }
            if split_line[2] == 'FAM' and 'id_source' in source or split_line[1] == 'TRLR':
                tmp = { 'id_source': source['id_source'] }
                for tag in ['chil', 'husb', 'wife']:
                    if tag in source and source[tag]['i'] > border:
                        tmp.update({ tag: source[tag]['item'] })
                sources.append(tmp)
                border = i
                source = {}
            elif split_line[2] == 'FAM':
                source['id_source'] = split_line[1]
            else:
                for tag in ['CHIL', 'HUSB', 'WIFE']:
                    if split_line[1] == tag:
                        source[tag.lower()] = { 'item': split_line[2], 'i': i }

    for unit in units:
        family = {}
        for other in units:
            if unit['id_unit'] != other['id_unit']:
                if 'famc' in unit and 'fams' in other and unit['famc'] == other['fams'] \
                    and 'famc' in other and other['famc'] != other['fams']:
                    if 'sex' in other:
                        if other['sex'] == 'F':
                            family.update({'mother': other['name']})
                        else:
                            family.update({'father': other['name']})
            if len(family) == 2:
                if 'famc' in unit:
                    ids_full_families.append(unit['famc'])
                if 'fams' in unit:
                    ids_full_families.append(unit['fams'])
                family.update({ 'child': unit['name']})
                full_families.append(family)
                break

        for source in sources:
            if unit['id_unit'] in source.values() and source['id_source'] not in ids_full_families and 'chil' in source and 'wife' in source and 'husb' in source:
                if unit['id_unit'] == source['chil']:
                    family.update({ 'child': unit['name'] })
                    for source_unit in units:
                        if source_unit['id_unit'] == source['wife']:
                            family.update({ 'mother': source_unit['name'] })
                        elif source_unit['id_unit'] == source['husb']:
                            family.update({ 'father': source_unit['name'] })
                        if len(family) == 3:
                            ids_full_families.append(source['id_source'])
                            full_families.append(family)
                            break

                elif unit['id_unit'] == source['wife']:
                    family.update({ 'mother': unit['name'] })
                    for source_unit in units:
                        if source_unit['id_unit'] == source['chil']:
                            family.update({ 'child': source_unit['name'] })
                        elif source_unit['id_unit'] == source['husb']:
                            family.update({ 'father': source_unit['name'] })
                        if len(family) == 3:
                            ids_full_families.append(source['id_source'])
                            full_families.append(family)
                            break

                elif unit['id_unit'] == source['husb']:
                    family.update({ 'father': unit['name'] })
                    for source_unit in units:
                        if source_unit['id_unit'] == source['chil']:
                            family.update({ 'child': source_unit['name'] })
                        elif source_unit['id_unit'] == source['wife']:
                            family.update({ 'mother': source_unit['name'] })
                        if len(family) == 3:
                            ids_full_families.append(source['id_source'])
                            full_families.append(family)
                            break

    for family in full_families:
        child = family['child'].lower().replace(' ', '_')
        mother = family['mother'].lower().replace(' ', '_')
        father = family['father'].lower().replace(' ', '_')
        for warn in [';', '/', '.', ',', '(', ')']:
            child = child.replace(warn, '')
            mother = mother.replace(warn, '')
            father = father.replace(warn, '')
        f_prolog.write(f"parents({child}, {father}, {mother}).\n")


Набор правил для Prolog

    parent(X,Y) :- parents(Y,X,_).
    parent(X,Y) :- parents(Y,_,X).
    father(X, Y) :- parents(Y, X, _).
    mother(X, Y) :- parents(Y, _, X).
    male(X) :- father(X, _).
    female(X) :- mother(X, _).
    grandfather(X, Y) :- father(X, Z), father(Z, Y).
    grandfather(X, Y) :- father(X, Z), mother(Z, Y).
    grandmother(X, Y) :- mother(X, Z), mother(Z, Y).
    grandmother(X, Y) :- mother(X, Z), father(Z, Y).
    brother(X, Y) :- male(X), father(Z, X), father(Z, Y), X \= Y.
    sister(X, Y) :- female(X), father(Z, X), father(Z, Y), X \= Y.
    aunt(X,Y) :- sister(X,Z), parent(Z,Y).
    uncle(X, Y) :- brother(X, Z), parent(Z,Y).

## Естественно-языковый интерфейс

    1 show by DATE TIME interval         [values]
    2 show all occurrences by NAME       [values]
    3 show all occurrences by CONTENT    [values]
    4 start proc search direct parents   [values]
    5 run Prolog
    6 exit
    input: 5
    5 - OK



## Выводы

В процессе выполнения курсового проекта были получены и применены навыки логического и функционального программирования. Использовались декораторы и лямбда выражения для получения информации из файла и регулярные выражения для очистки данных. Курсовой проект содержит построенное и проанализированное родословное дерево. 

