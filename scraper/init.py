from scrape import create_peer_universe

if __name__=='__main__':
    df = create_peer_universe('LVMUY')
    print(df)