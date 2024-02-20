:- dynamic visited_state/5.

min(X, Y, K) :- X > Y, K is Y.
min(X, Y, K) :- X =< Y, K is X.

input(Vx, Vy, Z) :-
    X = 0, Y = 0,
	retractall(visited_state(_,_,_,_,_)),
	state(X, Y, Vx, Vy, Z).

/* Neu Z lon hon the tich binh X va Y thi không co cach do */
state(_, _, Vx, Vy, Z) :-
	Z > Vx, Z > Vy,
	write('Khong co cach do!').

/* Neu luong nuoc trong binh X hoac binh Y = Z thi da tim duoc cach do */
state(Z, _, _, _, Z) :- write('Da tim duoc cach do').
state(_, Z, _, _, Z) :- write('Da tim duoc cach do').

/* Truong hop binh Y khong co nuoc thi do day nuoc vao binh Y */
state(X, Y, Vx, Vy, Z) :-
	Y = 0,
	New_Y is Vy,
	not(visited_state(X, New_Y, Vx, Vy, Z)),
	assertz(visited_state(X, Y, Vx, Vy, Z)),
	format('Do ~d lit nuoc vao binh Y: (~d, ~d).', [Vy, X, New_Y]),
    nl,
	state(X, New_Y, Vx, Vy, Z).

/* Truong hop binh X day thi do het nuoc ra */
state(X, Y, Vx, Vy, Z) :-
	X = Vx,
	New_X is 0,
	not(visited_state(New_X, Y, Vx, Vy, Z)),
	assertz(visited_state(X, Y, Vx, Vy, Z)),
	format('Do ~d lit nuoc ra khoi binh X: (~d, ~d).', [Vx, New_X, Y]),
	nl,
	state(New_X, Y, Vx, Vy, Z).

/* Truong hop con lai */
state(X, Y, Vx, Vy, Z) :-
	not(Y = 0), X < Vx,
	min(Y, Vx - X, K), New_X is X + K, New_Y is Y - K,
	not(visited_state(New_X, New_Y, Vx, Vy, Z)),
	assertz(visited_state(X, Y, Vx, Vy, Z)),
	format('Do ~d lit nuoc tu binh Y vao binh X: (~d, ~d)', [K, New_X, New_Y]),
	nl,
	state(New_X, New_Y, Vx, Vy, Z).








