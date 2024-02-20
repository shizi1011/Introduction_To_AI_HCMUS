/* Cau 1 */
la(de,dv_anco).
la(soi,dv_anthit).
la(X,dv_hungdu):-la(X,dv_anthit).
dv(X):-la(X,dv_anco);la(X,dv_anthit).
an(X,co):-la(X,dv_anco).
an(X,thit):-la(X,dv_anthit).
an(X,Y):-la(Y,dv_anco),la(X,dv_anthit).

uong(X,nuoc):-dv(X).


tieuthu(X,Y):-an(X,Y);uong(X,Y).

/* Cau 2
 *  Co dong vat dung du khong :
 *  la(X,dv_hungdu).
 *  No tieu thu gi :
 *  la(X,dv_hungdu),tieuthu(X,Y).
 */
