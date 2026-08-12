class WalletFundingGraph:

    def build_graph(
        self,
        transfers: list
    ):

        graph = {}

        for transfer in transfers:

            source = transfer["from"]

            destination = transfer["to"]

            if source not in graph:

                graph[source] = []

            graph[source].append(
                destination
            )

        return graph