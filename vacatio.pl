:- dynamic
    xodrzucona/1.

% Baza ofert
% oferta(Id, Od, Do, Lokalizacja, Inne) - Inne jako lista, i zostają do określenia TODO
% np.
% oferta (oferta1, '2021-11-12', '2021-12-12', lokalizacja(magagaskar), cena(wartosc), [ tutaj inne cechy jeszcze ])

oferta(oferta1, '2022-06-12', '2022-06-18', lokalizacja(rodos), cena(3000), [wyspa, morze, cieplo, relaks]).

% Predykaty zapytań
% Wybierane i wykorzystywane przez zewnętrzne API, po zadaniu odpowiednich pytań, po przecinku z oferta

klimat(lokalizacja(rodos), srodziemnomorski).
klimat(lokalizacja(ateny), srodziemnomorski).

cenowo(cena(C), tania) :- C < 1500.
cenowo(cena(C), budzetowa) :- C < 3500.

morsko(X) :- member(morze, X), member(wyspa, X).

odrzucona(X) :- xodrzucona(X).

% API

odrzuc(X) :- not(odrzucona(X)), assertz(xodrzucona(X)).

zapomnij :- retractall(xodrzucona(_)).

% Testy

% not(odrzucona(Id)), oferta(Id, Od, Do, lokalizacja(X), cena(C), T), klimat(lokalizacja(X), srodziemnomorski), cenowo(cena(C), budzetowa), morsko(T).