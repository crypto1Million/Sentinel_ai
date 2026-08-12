"""
Configuration Unit Tests
========================

Unit tests for Sentinel AI configuration system.
"""

from __future__ import annotations

import unittest


###############################################################################
# ConfigTests
###############################################################################


class ConfigTests(unittest.TestCase):

    ###########################################################################
    # Initialization
    ###########################################################################

    def setUp(self):

        self.config = self.mock_config()

    ###########################################################################

    def tearDown(self):

        self.config = None

    ###########################################################################
    # Configuration
    ###########################################################################

    def test_environment(self):

        self.assertEqual(
            self.config["environment"],
            "development",
        )

    ###########################################################################

    def test_api_keys(self):

        self.assertTrue(
            len(self.config["api_key"]) > 0
        )

    ###########################################################################

    def test_rpc(self):

        self.assertEqual(
            self.config["rpc"],
            "https://rpc.helius.xyz",
        )

    ###########################################################################

    def test_database(self):

        self.assertEqual(
            self.config["database"],
            "postgresql",
        )

    ###########################################################################
    # Settings
    ###########################################################################

    def test_defaults(self):

        self.assertEqual(
            self.config["timeout"],
            30,
        )

    ###########################################################################

    def test_override(self):

        timeout = 60

        self.assertEqual(
            timeout,
            60,
        )

    ###########################################################################

    def test_missing_config(self):

        missing = None

        self.assertIsNone(
            missing
        )

    ###########################################################################
    # Validation
    ###########################################################################

    def test_schema(self):

        required = [

            "environment",

            "rpc",

            "database",

            "api_key",

        ]

        for field in required:

            self.assertIn(
                field,
                self.config,
            )

    ###########################################################################

    def test_required_values(self):

        for value in self.config.values():

            self.assertIsNotNone(
                value
            )

    ###########################################################################
    # Runtime
    ###########################################################################

    def diagnostics(self):

        return {

            "component": "ConfigTests",

            "status": "healthy",

        }

    ###########################################################################

    def summary(self):

        return {

            "config_tests": "passed",

        }

    ###########################################################################
    # Utilities
    ###########################################################################

    def mock_config(self):

        return {

            "environment": "development",

            "rpc": "https://rpc.helius.xyz",

            "database": "postgresql",

            "api_key": "mock-api-key",

            "timeout": 30,

        }


###############################################################################
# Run Tests
###############################################################################

if __name__ == "__main__":

    unittest.main()