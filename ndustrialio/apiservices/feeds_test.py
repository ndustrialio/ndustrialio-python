from feeds import FeedsService

if __name__ == 'main':
    service = FeedsService(client_id='hcICuGIbxMd24J32Bdiw9moTaUb7ZQcG', client_secret='ctc8TUaYuGBa7Tc7mazEtRI1IHTsbM58Q9kFuWxV00pGNHZOoyl2IQ4tpnIpSBHB')
    print service.getHourlyMetrics()