parent(marry,bill).
parent(tom,bill).
parent(tom,liz).
parent(bill,ann).
parent(bill,sue).
parent(sue,jim).

/* Cau 1
 *  a. false.
 *  b. X=sue.
 *  c. false.
 *  d. false.
 * Cau 2
 *  a. parent(X,bill).
 *  b. parent(marry,X).
 *  c. parent(X,Y),parent(Y,sue).
*/
