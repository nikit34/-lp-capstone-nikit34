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
