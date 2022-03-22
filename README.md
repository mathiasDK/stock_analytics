# stock_analytics
A pack of code used to ease fundamental stock analysis. 

## Method
You choose a ticker you want to focus on. Then it scrapes yahoo finance for tickers that are similar. This is done in a couple of iterations to build a peer universe.

The assumption is that it is easier to asses if the valuation is fair, when comparing it to its peers. The multiples might differ much across sectors therefore it is tickers that are similar.

When the peer universe is created, then key statistics are extracted from yahoo finance. This is information like `Gross Margin`, `Beta` etc. These values can then be compared to each other to see how the ticker in focus is placed among its peers.

## Output
The output of the analysis is a plot which compares the main ticker with its peers.

There are two types of plots - a percentage plot (mainly for margins) and a normalized plot.
The normalized plot can be used for metrics which aren't necessarily comperable, but where you would like to know if your ticker is placed high or low among its peers.

The plots can be seen below and they are generated from the following code
``` python
data = create_peer_universe('LVMUY', 5)
create_fig(data, 'LVMUY', ['gross_margin', 'ebitda_margin', 'operating_margin'], title='Margins by company')
create_fig(data, 'LVMUY', ['enterprise_to_ebitda', 'beta', 'forward_pe', 'price_to_book'], title='Normalized ratios by company', normalize=True)
```
![plot](/images/Margins_by_company_20220322.png)
![plot](/images/Normalized_ratios_by_company_20220322.png)