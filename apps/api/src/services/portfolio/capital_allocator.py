class CapitalAllocator:

    def allocate(
        self,
        balance,
        conviction
    ):

        if conviction >= 90:

            return balance * 0.15

        if conviction >= 80:

            return balance * 0.10

        if conviction >= 70:

            return balance * 0.05

        return balance * 0.02