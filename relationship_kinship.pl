% степень родства

cousin(X,Y) :-
	child(X, Parents),
	child(Parents, Grandpar),
	female(Grandpar),
	child(Z, Grandpar),
	Z \= Parents,
	male(Y),
	child(Y, Z).


male(X) :- father(X, _).
female(X) :- mother(X, _).

sister(Child, X) :- child(Child, Parent), child(X, Parent), female(X), Child \= X.
brother(Child, X) :- child(Child, Parent), child(X, Parent), male(X), Child \= X.

mother(Mother, X) :- child(X, Mother), female(Mother).
father(Father, X) :- child(X, Father), male(Father).

son(X, Parent) :- child(X, Parent), male(X).
daughter(X, Parent) :- child(X, Parent), female(X).

relationship(father, Fath, Child) :- father(Fath, Child).
relationship(mother, Moth, Child) :- mother(Moth, Child).

relationship(husband, Husb, Wife) :- child(Child, Husb), child(Child, Wife), Husb \= Wife, male(Husb).
relationship(wife, Wife, Husb) :- child(Child, Husb), child(Child, Wife), Husb \= Wife, female(Wife).
relationship(brother, Bro, X) :- brother(X,Bro).
relationship(sister, Sis, Y) :- sister(Y, Sis).
relationship(parent, Parent, Child) :- child(Child, Parent).
relationship(child, Child, Parent) :- child(Child, Parent).
relationship(son, Child, Parent) :- son(Child, Parent).
relationship(daughter, Child, Parent) :- daughter(Child, Parent).

chain(X) :- member(X, [father, mother, sister, brother, son, daughter, husband, wife]).

move(X,Y) :- relationship(_, X, Y).


relationship_thread(X, Y, Res) :- width_search(X, Y, Res).
relationship(X, Y, Res) :- width_search(X, Y, Res1), !, result(Res1, Res).

result([_], []) :- !.
result([First, Second|Tail], ResList):-
    relationship(Relation, First, Second),
    ResList = [Relation|Tmp],
    result([Second|Tail], Tmp),!.

prolong([X|Tail], [New, X|Tail]) :- move(X, New), not(member(New, [X|Tail])).

width_search(X, Y, Parent) :- width([[X]], Y, L), reverse(L, Parent).
width([[X|T]|_], X, [X|T]).
width([Parent|T1], X, R) :- findall(Z, prolong(Parent,Z), T), append(T1, T, W), width(W, X, R),!.
width([_|T], Y, L) :- width(T, Y, L).



% естественно языковой интерфейс

question(W):- member(W, [who, "Who"]).

is(I):- member(I,[is, "is"]).

symbol_qestion(Q):- member(Q, ['?']).


% Пример запроса: [Who, is, *name*, mother, ?]
ask(List):-
      List = [Word, Is, Name, Rel, Q],
      question(Word),
      is(Is),
      (male(Name);female(Name)),
      nb_setval(lastName, N),
      chain(Rel),
      symbol_qestion(Q), !,
      relationship(Rel, Res, Name),
      write(Res), write(" is "), write(Name), write(Rel).


% Пример запроса: [is, *name*, *name*, father, ?]
ask(List):-
      List = [Is, Name1, Name2, Rel, Q],
      nb_setval(lastName, Name2),
      is(Is),
      (male(Name1);female(Name1)),
      (male(Name2);female(Name2)),
      chain(Rel),
      symbol_qestion(Q),
      relationship(Rel, Name1, Name2), !.