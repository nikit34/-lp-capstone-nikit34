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






% approvals


parents(joseph_patrick_kennedy_ii, robert_francis_kennedy, ethel_skakel).
parents(david_anthony_kennedy, robert_francis_kennedy, ethel_skakel).
parents(michael_lemoyne_kennedy, robert_francis_kennedy, ethel_skakel).
parents(christopher_george_kennedy, robert_francis_kennedy, ethel_skakel).
parents(douglas_harriman_kennedy, robert_francis_kennedy, ethel_skakel).
parents(david_lee_townsend, robert_francis_kennedy, ethel_skakel).
parents(joseph_patrick_kennedy_iii, joseph_patrick_kennedy_ii, sheila_brewster_rauch).
parents(lawrence_m_kane, philip_kane, bridget_murphy).
parents(frederick_kane, lawrence_m_kane, gertrude_margaret_kane).
parents(frederick_louis_mahoney, louis_leo_twomey, joanna_l_kennedy).
parents(charles_joseph_burke_jr, charles_joseph_burke, margaret_louise_kennedy).
parents(john_bernard_devine, charles_joseph_burke, margaret_louise_kennedy).
parents(rosanna_cox, philip_cox, ellen_wilmouth).
parents(michael_hannon, john_hannon, rosanna_cox).
parents(william_alexander_lindsay, eustache_bouvier, therese_mercier).
parents(louise_c_vernou, william_alexander_lindsay, elizabeth_clifford_lindsay).
parents(william_sergeant_bud_bouvier, william_r_sergeant, maud_frances_sergeant).
