parents(david, george, noreen).
parents(jennifer, george, noreen).
parents(georgejr, george, noreen).
parents(scott, george, noreen).
parents(joanne, george, noreen).
parents(jessica, david, edel).
parents(clara, david, edel).
parents(michael, david, edel).
parents(laura, georgejr, susan).
parents(anna, scott, siobhan).


/* Relationships */

parent(X,Y) :- parents(Y,X,_).
parent(X,Y) :- parents(Y,_,X).

father(X, Y) :- parents(Y, X, _).

male(michael).
male(X) :- father(X, _).

mother(X, Y) :- parents(Y, _, X).

female(joanne).
female(jessica).
female(jennifer).
female(clara).
female(laura).
female(anna).
female(X) :- mother(X, _).

grandfather(X, Y) :- father(X, Z), father(Z, Y).
grandfather(X, Y) :- father(X, Z), mother(Z, Y).

grandmother(X, Y) :- mother(X, Z), mother(Z, Y).
grandmother(X, Y) :- mother(X, Z), father(Z, Y).

brother(X, Y) :- male(X), father(Z, X), father(Z, Y), X \= Y.
sister(X, Y) :- female(X), father(Z, X), father(Z, Y), X \= Y.

aunt(X,Y) :- sister(X,Z), parent(Z,Y).
uncle(X, Y) :- brother(X, Z), parent(Z,Y).