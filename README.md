# Projekt
Projekt: System ADMS, będący w stanie na bieżąco reagować na sygnały 
otrzymywane od operatora sieci elektrycznej umożliwiający ładowanie 
samochodów elektrycznych na parkingu.

Struktura projektu:
* algorithm - folder dla programu z algorytmem balansującym energię elektryczną
> Uruchomienie: 

* database - folder ze schematami bazy danych
* application - folder z backendem oraz frontendem aplikacji
> Uruchomienie: 
> 1. Z głównego folderu repozytorium należy przejść do folderu application\frontend: 
>> cd .\application\frontend\
> 2. Przy pierwszym uruchomieniu po pobraniu należy zacząć od pobrania zależności: 
>> npm install
> 3. Uruchomienie Reacta: 
>> npm start
> 4. Uruchomienie Flaska (w drugim terminalu, również w folderze application\frontend): 
>> npm run start-api