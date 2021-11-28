:- dynamic
    xodrzucona/1.

% Core predicates

klimat(lokalizacja(rodos), srodziemnomorski).
klimat(lokalizacja(kreta), srodziemnomorski).
klimat(lokalizacja(ateny), srodziemnomorski).
klimat(lokalizacja(zakopane), gorski).
klimat(lokalizacja(karpacz), gorski).
klimat(lokalizacja(krakow), umiarkowany).
klimat(lokalizacja(warszawa), umiarkowany).
klimat(lokalizacja(widacz), umiarkowany).

cenowo(cena(C), tania) :- C < 1500.
cenowo(cena(C), budzetowa) :- C < 3500.
cenowo(cena(C), droga) :- C > 3500.

morsko(X) :- member(morze, X), member(wyspa, X).
gorsko(X) :- member(trekking, X), member(szlaki, X).
miejsko(X) :- member(galerie, X), member(muzea, X).
wiejsko(X) :- member(agroturystyka, X), member(swieze_powietrze, X), member(zwierzeta, X).
starozytno(X) :- member(kolumny, X), member(swiatynie, X).

odrzucona(X) :- xodrzucona(X).

% API

odrzuc(X) :- not(odrzucona(X)), assertz(xodrzucona(X)).

zapomnij :- retractall(xodrzucona(_)).
