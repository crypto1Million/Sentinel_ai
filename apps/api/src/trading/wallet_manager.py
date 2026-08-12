class WalletManager:

    def connect(
        self,
        wallet_address: str
    ):

        return {

            "wallet":
            wallet_address,

            "status":
            "connected"
        }

    def disconnect(
        self
    ):

        return {

            "status":
            "disconnected"
        }