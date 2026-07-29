from pathlib import Path

import yaml

import adapter


ROOT = Path(__file__).resolve().parents[1]


def test_inquiry_0001_validates_and_builds_report():
    request_path = ROOT / "inquiries/INQ-000000001/speech-request.yaml"
    request = yaml.safe_load(request_path.read_text(encoding="utf-8"))

    assert adapter.validate_manifest(adapter.load_manifest()) == []
    assert adapter.validate_speech_request(request) == []

    report = adapter.build_candidate_report(request)
    assert report["record_type"] == "ministerial_report"
    assert report["id"] == "MREP-INQ000000001-LEO-STRAUSS"
    assert report["termination_status"] == "SOVEREIGN_STRAUSS_REPORT_COMPLETE_WITH_PRESERVED_UNCERTAINTY"
    assert {item["kind"] for item in report["propositions"]} == {
        "documented_finding",
        "supported_inference",
        "unresolved_uncertainty",
    }
    refs = {
        evidence["ref"]
        for proposition in report["propositions"]
        for evidence in proposition["grounds"]
    }
    assert "CORPUS-WIT-103" in refs
    assert "CORPUS-WIT-114" in refs
    assert report["contradictions_and_dissent"] == []
    assert report["unresolved_uncertainties"]
