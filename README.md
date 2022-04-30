# 2D top-down driving through racetrack - simulation

# Semestrální projekt do předmětu BI-PYT 21/22

## Ovládání
Uživatel se pohybuje pomocí `WSAD`, pro demonstraci, jak težké to mají agenti.
Pro vyčištění místnosti stačí stisknout klávesu `Del`, která urychlí process naturalní selekce.
Hráč může použít teleport pomocí stisku `pohybové klávesy + mezerníku`.
Stiskem Q hráč změní způsob vykreslování.

## Gameplay
Uživatel se může volně pohybovat pokud je program spuštěn ze souboru, `__main_movement.py`, jestli je program spuštěn ze `__main_movement.py` je třeba se ujistit, že je v konfiguraci nastavena hodnota `let_me_drive` na  `True`

Hráč může střílet (`šipky`) a teleportovat se `WSAD + mezerník`. Hlavně se vyhýbejte ohnivým polím, protože můžou hodně zabolet!

Program se dá spustit:
- jako AI simulace
- jako movement simulace


## Instalace
Stačí stáhnout adresář a je zde připraveno conda prostředí s názvem `semestral-work`, stačí tedy spustit

```shellscript
conda env create --name semestral-work --file=environment.yml
conda activate semestral-work
```

Následně stačí spustit soubor `__main_ai__.py` v kořeni adresáře.

Testy testují dle mého potřebnou funkcionalitu, ostatní testy jsou založené na otestovaných věceh. Spustíte je příkazem `pytest`.