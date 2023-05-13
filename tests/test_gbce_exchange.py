def test_calc_gbce_all_share_index(gbce_exchange):
    # Record some sample Trades
    gbce_exchange.get_stock("TEA").record_trade(10, "BUY", 100)
    gbce_exchange.get_stock("POP").record_trade(5, "SELL", 100)
    gbce_exchange.get_stock("ALE").record_trade(20, "BUY", 60)
    gbce_exchange.get_stock("GIN").record_trade(2, "SELL", 100)
    gbce_exchange.get_stock("JOE").record_trade(10, "BUY", 250)

    assert gbce_exchange.calc_gbce_all_share_index() == 108.447
