# Fundusz Hossa Procapital

System analityczny do zarządzania portfelem inwestycyjnym oparty na:
- **empirycznych miarach ryzyka (VaR, ES, Max Drawdown)**,
- **modelu Risk Parity**,
- **modelu Black–Littermana (BL)** z ograniczeniami wag.

Projekt integruje dane transakcyjne i wyceny spółek z Excela, pobiera historyczne ceny z Yahoo Finance, oblicza miary ryzyka i generuje raport w formacie Excel.



## Zawartość raportu

| Arkusz          | Opis                                                               |
| :-------------- | :----------------------------------------------------------------- |
| **Summary**     | Wartość portfela, zmienność, VaR, ES, Max Drawdown, gotówka        |
| **Weights**     | Porównanie wag: bieżące, Risk Parity, Black–Litterman, ograniczone |
| **Holdings**    | Stan posiadania akcji                                              |
| **Prices_Tail** | Ostatnie notowania (10 dni)                                        |
| **Config**      | Użyta konfiguracja i parametry sesji                               |


## Teoria

### Empiryczne ryzyko

Miary ryzyka liczone są bez założeń o rozkładzie stóp zwrotu:

* **VaR (Value-at-Risk)** – strata nieprzekraczana z prawdopodobieństwem `confidence`.
* **ES (Expected Shortfall)** – średnia strata w ogonie poniżej VaR.
* **Max Drawdown** – największy spadek wartości portfela od szczytu.

### Risk Parity

Celem jest równy udział każdej pozycji w całkowitym ryzyku:

$$
RC_i \;=\; w_i\,(\Sigma w)_i
$$

$$
RC_i \;=\; \frac{1}{n}, \quad i=1,\dots,n
$$

Rozwiązanie uzyskiwane przez optymalizację SLSQP z ograniczeniami sumy wag i przedziałami $w_{min}, w_{max}$.

### Black–Litterman (BL)

Model łączy równe wkłady ryzyka z subiektywnymi poglądami analityków:

$$
\mu_{\mathrm{BL}}
= \left[(\tau\Sigma)^{-1} + P^\top \Omega^{-1} P\right]^{-1}
  \left[(\tau\Sigma)^{-1}\pi + P^\top \Omega^{-1} Q\right]
$$

gdzie:

* $π = δΣw_{PR}$ – zwroty równowagi (priory) z modelu Risk Parity,
* $P, Q$ – macierz i wektor poglądów (oczekiwany „upside”),
* $Ω$ – wariancje błędów poglądów,
* $τ$ – niepewność priory,
* $δ$ – współczynnik awersji do ryzyka.

Wynikowe wagi to:

$$
w_{\mathrm{BL}} \;=\; \frac{1}{\delta}\,\Sigma^{-1}\,\mu_{\mathrm{BL}}
$$

W projekcie użyto wersji praktycznej z ograniczeniami `bl_box_lb, bl_box_ub`, dzięki czemu wynikowe wagi można interpretować wprost jako realistyczne udziały w portfelu.


## Struktura projektu

```
fundusz-hossa-procapital/
│
├── analytics/
│   ├── risk_metrics.py       # Empiryczne ryzyko portfela (VaR, ES, MDD)
│   └── risk_utils.py         # Zwroty, NAV, przeliczenia
│
├── data/
│   ├── portfolio_loader.py   # Wczytywanie transakcji i stanów
│   ├── prices.py             # Pobieranie cen z Yahoo Finance
│   └── valuation_loader.py   # Wczytywanie wycen spółek
│
├── optimization/
│   ├── risk_parity.py        # Risk Parity (SLSQP)
│   ├── black_litterman.py    # Model Black–Littermana (PyPortfolioOpt)
│   ├── constraints.py        # Projekcja wag na ograniczony sympleks
│   └── upside.py             # Filtrowanie spółek po „upside”
│
├── reporting/
│   └── exporter.py           # Generowanie raportu Excel
│
├── input/                    # Pliki wejściowe (transakcje, wyceny)
├── output/                   # Wyniki raportów
├── config.yaml               # Konfiguracja parametrów
├── main.py                   # Główny skrypt sterujący
└── requirements.txt          # Zależności Pythona
```


Struktura oraz kod został przygotowany przeze mnie na potrzeby Funduszu Hossa ProCapital.



