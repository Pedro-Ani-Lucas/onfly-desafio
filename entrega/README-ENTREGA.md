# Onfly - Teste Técnico - Entrega

Entrega do relatório do teste técnico proposto pela Onfly contendo defeitos corrigidos, causa raiz em uma frase por defeito, como investigou/abordou o problema, como validar e resultado do `pytest`.

## Correção dos defeitos propostos

### Defeito corrigido 01 - Conversão incorreta para moeda BRL

- *Onde:* Na função `convert_to_brl()` em `currency_converter.py`; Violava a regra: *Use `Decimal`, nunca `float`, no dinheiro* e a forma de cálculo da taxa de câmbio. 
- *Causa raiz:* O USD ou EUR eram divididos invés de serem multiplicados pela taxa devida. 
- *Como encontrei:* O teste esperava 642.00 e encontrou 118.45; Assim, observando que eram uma reserva em BRL e outra em USD, haveria de ocorrer a conversão do dólar para reais, entretanto ocorria do jeito errado. Na função `convert_to_brl`, mostrava no código interno uma divisão do valor pela taxa, assim encontrado o defeito.
- *Como abordou:* Troca de operação pela multiplicação e, ademais, observei uma redundância no tipo de dado e conversão intermediária para o `float`. Optei na decisão de retirar a conversão intermediária e essas redundâncias quando uma vez os dados chegam no formato `Decimal` no que é correto. 
- *Como validar:* Para validar que o erro não ocorra mais, o teste `test_currency_conversion_to_brl()` em `test_currency.py` demonstra que a conversão de câmbio não é mais incorreta. 
- *Resultado do Pytest:* 
```powershell 
pytest -q
........                                                                                     [100%]
8 passed in 1.71s
```

### Defeito corrigido 02 - Cálculo incorreto de noites em virada do mês

- *Onde:* Na função `calculate_room_nights()` em `stay_calculator.py`; Violava a regra *A diferença é não inclusiva: check-in 10/01 e check-out 13/01 = 3 noites. Vale também na virada de mês/ano.*. 
- *Causa Raiz*: O atributo .day extrai apenas o dia do mês, invés de considerar a virada do mês/ano.
- *Como encontrei:* O teste esperava 3 e encontrava -28; Assim ser um número absurdo e ilógico, a primeira busca foi na função de calculo das *room_nights*, cuja função encontrada em `stay_calculator.py`. Assim, apresentava no código interno o erro de implementação de atributo. 
- *Como abordei:* Pesquisando sobre a biblioteca *timedelta*, a solução do problema seria retirar os atributos que extraíam os números de cada variável e colocasse o atributo `.days` fora do cálculo de diferença entre check-out e check-in. Assim, transformavam os dias (tipo object) em `int` e o cálculo de diferença sairiam, considerando a virada do mês.
- *Como validar:* Para validar que o erro não ocorra mais, o teste `test_nights_across_month_boundary()` em `test_nights.py` demonstra que a virada do mês não retorna os números brutos e, sim, o formato necessário para que seja considerada.
- *Resultado do Pytest:* 
```powershell 
pytest -q
........                                                                                     [100%]
8 passed in 1.71s
```

### Defeito corrigido 03 - Vazamento de contagem de status no faturamento.

- *Onde:* Na função `is_billable()` em `status_policy.py`; Violava a regra *Só `CONFIRMED` é faturável.*
- *Causa raiz:* A função proibia apenas `CANCELLED` em vez de permitir apenas `CONFIRMED` na contagem e faturamento.
- *Como encontrei:* O teste esperava 100.00 total_amount_brl e encontrava 120.00 total_amount_brl; Mostrando que a reserva com status `NO_SHOW` estava sendo considerado no faturamento. Procurando e encontrado efetivamente a função na pasta `services/`.
- *Como abordei:* Percebi que a linha lógica daquela função era de proibição, no caso, apenas `CANCELLED` era eliminado, deixando vazar as reservas com status `NO_SHOW`. Inverti essa lógica com o operador de comparação `==`, assim permitindo ser contabilizado apenas o status `CONFIRMED`. 
- *Como validar:* Para validar que o erro não ocorra mais, o teste `test_status_rules_exclude_cancelled_and_no_show()` em `test_status_rules.py` apenas as reservas com o status `CONFIRMED`são faturados, os demais são desconsiderados no faturamento.
- *Resultado do Pytest:* 
```powershell 
pytest -q
........                                                                                     [100%]
8 passed in 1.71s
```

### Defeito corrigido 04 - Ordenação incorreta no valor total de cada hotel no rankeamento

- *Onde:* Na função `ReportBuilder.build()` em `report_builder.py`; Violava a regra *`top\_hotels`: `total\_brl` decrescente; empate por `hotel\_id` ascendente.*.
- *Causa raiz:* A função fazia a ordenação do `total_brl` em ordem crescente.
- *Como encontrei:* O teste esperava ['H01', 'H02', 'H03'] e encontrava ['H04', 'H03', 'H02']. Assim demonstrando que na hora do rankeamento, a ordenação estava priorizando a ordem crescente no atributo `amount`, invés da decrescente. Com essa conclusão, procurei onde a função de rankeamento acontecia, encontrando em `report_builder.py`. 
- *Como abordei:* Pesquisando como pudesse inverter essa ordem, sem prejudicar a ordem crescente do `item[0]`que representava o `hotel_id`. Encontro o operador `-` que invertia a ordem e permanecia a outra inalterável, assim retirando a possibilidade de usar o parâmetro `reverse=True`. 
- *Como validar:* Para validar que o erro não ocorra mais, o teste `test_top_hotels_are_ranked_descending()` em `test_top_hotels.py` confirma a ordenação decrescente no item `amount`e no critério de desempate a ordenação crescente em `hotel_id`.
- *Resultado do Pytest:* 
```powershell 
pytest -q
........                                                                                     [100%]
8 passed in 1.71s
```

### Defeito corrigido 05 - Geração de Report com valores incorretos

- *Causa raiz:* Relatório gerado incorretamente em virtude dos erros dos outros defeitos.
- *Decisões conscientes:* Por sugestão do Claude, optei por consertar esse erro por último. Assim, priorizava os outros defeitos e quando chegasse nele, apenas os erros que tivessem sobrados, iria corrigir.
- *Como abordei:* Com os 4 defeitos acima sendo consertados, o report foi gerado sem erros.
- *Como validar:* Para validar que o erro não ocorra mais, o teste `test_regression_report_on_sample()` em `test_regression_report.py` gera um relatório de uma amostra pequena com os números todos em conformidade com o esperado.
- *Resultado do Pytest:* 
```powershell 
pytest -q
........                                                                                     [100%]
8 passed in 1.71s
```

### Defeito corrigido 06 - Condicional de parada para leitor das linhas do arquivo CSV

- *Onde:* Na função `read()` em `csv_reservation_repository.py`; Violava a regra *total\_reservations` = número de reservas no arquivo.*
- *Causa Raiz:* Leitor lia até a linha 200 do arquivo csv em vez de todas as linhas.
- *Como encontrei:* Por sugestão da IA, utilizei um comando no PowerShell em contar quantas linhas tinha o csv `reservas_hoteis.csv`. Assim, comparando a quantidade de linha do csv(300) e o total de reservas do relatório `report.json`(200), concluí que o leitor não estava lendo tudo. Assim encontrando a condição de parada em `csv_reservation_repository.py`.
- *Como abordei:* Analisando a melhor solução, optei por retirar a condição de parada, pois eventual uso de outro arquivo csv, podem conter mais ou menos linhas. Assim permiti o `for()` rodar todo o arquivo `reader`. 
- *Como validar:* Para validar que o erro não ocorra mais, o teste adicional `test_total_reservations_equals_rows_csv()` em `test_total_reservations.py` com uma geração de lista com 250 dicionários sobre reservas com status alternando, demonstra que a condição da parada não ocorra mais e as 3 reservas com status diferentes são contabilizados e abordando uma solidez na contabilização das reservas.
- *Resultado do Pytest:* 
```powershell 
pytest -q
........                                                                                     [100%]
8 passed in 1.71s
```

## Decisões conscientes

Enquanto os defeitos eram consertados, vieram ideias para melhorar com auxílio da (IA) nos quais são: Adição do `.upper()` no atributo `status` em `row_parser.py` e remoção do limite da condição de parada.

Na *adição do `.upper()`*, a decisão ocorreu para um tratamento de string antes de entrar em qualquer tipo de função que utiliza as contagens de status. Por isso esse tratamento ocorre no arquivo `row_parser.py` em vez de alguma função nos fluxos seguintes.

## Testes Adicionais

Por decisões deliberadas, sugeridas pelo Claude(IA), foram criados 2 novos testes para melhor validação do sistema.

### Teste Adicional 01 - Formato do status incorreto

- *O que prova:* O `test_status_format_upper_and_without_spaces()` em `test_status_format.py` prova que todos os status virão maiúsculo e sem espaços. 
- *Onde falha:* Sem o `.upper()`, dados alterados na coluna `status` no csv poderão passar despercebidos e sem tratamento adequado. 
- *Resultado no Pytest falhando:* ```FAILED tests/test_status_format.py::test_status_format_upper_and_without_spaces - assert 1 == 2```

### Teste Adicional 02 - Critério de desempate em hotel_id

- *O que prova:* O `test_tiebreaker_hotels_id()` em `test_tiebreaker_hotels.py` prova que o critério de desempate não ocorra distorções na ordem de entrada dos dicionários.
- *Onde falha:* Sem o `item[0]` colocado devidamente, a ordem de inserção de dados pode definir incorretamente a forma como o rankeamento será imprimido.
- *Resultado do Pytest falhando:* 
```FAILED tests/test_tiebreaker_hotels.py::test_tiebreaker_hotels_id - AssertionError: assert ['H03', 'H02', 'H04'] == ['H02', 'H03', 'H04']```

