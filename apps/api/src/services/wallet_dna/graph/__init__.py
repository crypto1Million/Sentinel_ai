Wallet DNA Graph Engine

Contains:

• Graph Engine
• Storage
• Cache
• Indexes
• Statistics
• Modelsclass DeployerGraph:

    def __init__(...):

        self._initialize_configuration(config)

        self._initialize_logger()

        self._initialize_graph()

        self._initialize_database(wallet_db, token_db, cache_manager)

        self._initialize_core_state()

        self._initialize_node_storage()

        self._initialize_edge_storage()

        self._initialize_indexes()

        self._initialize_caches()

        self._initialize_statistics()

        self._initialize_synchronization()

        self._initialize_workers()

        self._initialize_runtime()

        self.config = GraphConfig()

self.indexes = GraphIndexes()

self.cache = GraphCache()

self.statistics = GraphStatistics()

self.runtime = GraphRuntime()

self.graph = nx.MultiDiGraph()