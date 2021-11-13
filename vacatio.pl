:- dynamic
    xpozytywne/1,
    xodrzucona/1.

% Baza ofert
% ofertaX - zlozona zawsze z atomow dla predykatow poziomu nizej np. oferta1 -> gory, niska itd. 
% ofertaX - czesciowa to kombinacja predykatow oferty

oferta_jest(oferta1) :- not(odrzucona(oferta1)),
                        lokalizacja_docelowa(gory),
                        cena(niska),
                        kuchnia(syta),
                        atrakcja(spa),
                        atrakcja(wycieczka),
                        zakwaterowanie(hotel).

oferta_czesciowo_jest(oferta1) :- not(odrzucona(oferta1)),
                                  lokalizacja_docelowa(gory),
                                  cena(niska).

oferta_czesciowo_jest(oferta1) :- not(odrzucona(oferta1)),
                                  kuchnia(syta),
                                  atrakcja(spa).

oferta_czesciowo_jest(oferta1) :- not(odrzucona(oferta1)),
                                  atrakcja(wycieczka),
                                  zakwaterowanie(hotel).

% Predykaty niższego stopnia

lokalizacja_docelowa(gory) :- pozytywne(wysilek_fizyczny),
                              pozytywne(piekne_widoki),
                              pozytywne(las),
                              pozytywne(swieze_powietrze).

cena(niska) :- pozytywne(camping),
               pozytywne(bary_mleczne),
               pozytywne(brak_pamiatek).

cena(niska) :- pozytywne(tani_hotel),
               pozytywne(bary_mleczne),
               pozytywne(brak_pamiatek).

kuchnia(syta) :- pozytywne(tlusta),
                 pozytywne(karczma),
                 pozytywne(obfita).

kuchnia(miejska) :- pozytywne(zbilansowana),
                    pozytywne(bary_mleczne).

atrakcja(spa) :- pozytywne(relaks),
                 pozytywne(odnowa_biologiczna),
                 pozytywne(basen),
                 pozytywne(masaz).

atrakcja(wycieczka) :- pozytywne(wysilek_fizyczny),
                       pozytywne(zorganizowane),
                       pozytywne(gromadnie).

atrakcja(wycieczka) :- pozytywne(wysilek_fizyczny),
                       pozytywne(niezorganizowane),
                       pozytywne(samotnie).

zakwaterowanie(hotel) :- pozytywne(male_bagaze),
                         pozytywne(mala_swoboda),
                         pozytywne(bezpieczenstwo).

pozytywne(X) :- xpozytywne(X).

odrzucona(X) :- xodrzucona(X).

% API

pamietaj(X) :- not(pozytywne(X)), assertz(xpozytywne(X)).

odrzuc(X) :- not(odrzucona(X)), assertz(xodrzucona(X)).

zapomnij :- retractall(xpozytywne(_)),
            retractall(xodrzucona(_)).

% Testy

pamietaj_sym :- pamietaj(camping),
                pamietaj(bary_mleczne),
                pamietaj(brak_pamiatek),
                pamietaj(wysilek_fizyczny),
                pamietaj(piekne_widoki),
                pamietaj(las),
                pamietaj(swieze_powietrze),
                pamietaj(tlusta),
                pamietaj(karczma),
                pamietaj(obfita),
                pamietaj(relaks),
                pamietaj(odnowa_biologiczna),
                pamietaj(basen),
                pamietaj(masaz),
                pamietaj(zorganizowane),
                pamietaj(gromadnie),
                pamietaj(male_bagaze),
                pamietaj(mala_swoboda),
                pamietaj(bezpieczenstwo).

pamietaj_czesciowo_sym :- pamietaj(camping),
                pamietaj(bary_mleczne),
                pamietaj(brak_pamiatek),
                pamietaj(wysilek_fizyczny),
                pamietaj(las),
                pamietaj(tlusta),
                pamietaj(karczma),
                pamietaj(obfita),
                pamietaj(relaks),
                pamietaj(odnowa_biologiczna),
                pamietaj(basen),
                pamietaj(masaz),
                pamietaj(zorganizowane),
                pamietaj(gromadnie),
                pamietaj(male_bagaze),
                pamietaj(mala_swoboda),
                pamietaj(bezpieczenstwo).

% oferta_jest(X) oraz oferta_czesciowo_jest(X)
