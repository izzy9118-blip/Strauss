import unittest

import sanctum_adapter


class SanctumAdapterV1Tests(unittest.TestCase):
    def test_descriptor_is_generic_and_pinned(self):
        descriptor = sanctum_adapter.describe()
        self.assertEqual(descriptor["record_type"], "sanctum_adapter_descriptor")
        self.assertEqual(descriptor["protocol"], "sanctum.adapter.v1")
        self.assertEqual(descriptor["minister_id"], "leo-strauss")
        self.assertEqual(descriptor["repository"], "izzy9118-blip/Strauss")
        self.assertEqual(len(descriptor["repository_commit"]), 40)
        self.assertEqual(
            descriptor["commands"],
            ["describe", "validate-interface", "prepare-request", "validate-report"],
        )
        self.assertNotEqual(descriptor["authority"], "OWNER_CERTIFIED")

    def test_underlying_interface_remains_authoritative_locally(self):
        result = sanctum_adapter.validate_interface()
        self.assertEqual(result["status"], "VALIDATED_INTERFACE_NOT_TRUTH_CERTIFIED")

    def test_prepare_rejects_wrong_pin(self):
        with self.assertRaises(sanctum_adapter.SanctumAdapterError):
            sanctum_adapter.prepare_request(
                {
                    "record_type": "sanctum_adapter_request",
                    "protocol": "sanctum.adapter.v1",
                    "minister_id": "leo-strauss",
                    "repository_pin": {
                        "repository": "izzy9118-blip/Strauss",
                        "commit": "0" * 40,
                    },
                    "inquiry_id": "TEST",
                    "question": "What follows?",
                    "common_briefing": {"sha256": "a" * 64},
                }
            )


if __name__ == "__main__":
    unittest.main()
