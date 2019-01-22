from google import google

top_cryptocurrencies_names = ["Bitcoin", "XRP", "Ethereum", "Stellar", "Tether", "EOS", "Litecoin", "Bitcoin Cash",
                              "Bitcoin SV", "TRON", "Cardano", "Monero", "IOTA", "Binance Coin", "NEM", "Dash",
                              "Ethereum Classic", "NEO", "Zcash", "Maker", "Dogecoin", "Waves", "Tezos", "TrueUSD",
                              "USD Coin", "Bitcoin Gold", "VeChain", "OmiseGO", "Basic Attention Token", "Qtum",
                              "Paxos Standard", "0x", "Decred", "Lisk"]


def fetch_projects_website_links():
    with open("output/crypto_projects_links.txt", "a") as projects_links:
        for project_id, project_name in enumerate(top_cryptocurrencies_names, 1):
            search_results = google.search(project_name + " project website")
            if search_results and search_results[0]:
                projects_links.write(search_results[0].link + "\n")
                print(str(project_id) + " Got " + search_results[0].link)
            else:
                print(str(project_id) + " No search results fetched for project " + project_name)


if __name__ == '__main__':
    fetch_projects_website_links()
