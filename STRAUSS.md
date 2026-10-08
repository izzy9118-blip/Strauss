# Strauss harness

Activating this repository loads the Strauss Reader from `izzy9118-blip/custos`.
Custos owns source examination and corpus building. Strauss retains its seven
foundational problems, existing corpus and findings, and ministerial reporting.

## Activation

```bash
python -m pip install 'PyYAML>=6,<7'
python adapter.py --pretty
```

The adapter refreshes a managed checkout from **Custos/main** under `.runtime/custos`,
then asks Custos itself for `custos.reader-context.v1`. The `reader` section contains
the full active `CUSTOS.md`, configuration, five-stage outer protocol, LC-001–LC-022
inner inventory, exact selected commit, and hashes of the authority documents.
Activation fails if the Reader cannot load; there is no silent fallback to an older
methodology. Loading context is not a completed reading.

For an existing checkout use `--custos-root /path/to/custos`, or set
`STRAUSS_CUSTOS_ROOT`. An explicit checkout is used as supplied, with its exact commit
recorded; its Reader instructions and code must be committed. The binding's
`tested_commit` records the integration baseline rather than freezing future corpus
work. Every activation uses the current compatible Reader in the selected checkout.

## Reading with the user

After activation, the conversational model applies `reader.instructions` and both
`reader.gates` to the source or inquiry explicitly supplied by the user. Close mode
is the ordinary mode: perform one bounded textual act, preserve the strongest rival
and uncertainty, return to the governing Strauss passage, and name the next act.
Use sweep mode for an explicitly requested whole-text documentary map.

The full literary inventory stays available; evidence governs activation of a named
technique. A supplied book is not automatically a completed close-reading inquiry.
Continue substantive examination with the user. CLI preparation alone is not that
examination.

## Executable reading

The same adapter delegates to Custos's existing runner. Supply exactly one input:

```bash
python adapter.py --source /path/to/witness.txt --mode close \
  --reasoner-command 'your-json-reasoner' --output /path/to/new-run

python adapter.py --source /path/to/witness.txt --mode sweep \
  --reasoner-command 'your-json-reasoner' --output /path/to/new-sweep

python adapter.py --inquiry inquiries/thoughts-on-machiavelli/chapter-01-note-01 \
  --reasoner-command 'your-json-reasoner' --output /path/to/new-close-run
```

Sources are UTF-8 witnesses. Inquiry paths are relative to the selected Custos checkout.
The reasoner receives a complete `custos.reader-request.v1` on standard input and must
return `custos.reader-response.v1` JSON. Custos validates the response and writes the
examination, structured response, and run record. The adapter propagates failures and
reports the actual Reader completion status. Without a reasoner, execution fails with
`READER_REASONER_REQUIRED`.
Reasoner commands run from the calling directory, so relative reasoner paths keep
their original meaning.

For an external or conversational reasoner that needs a prepared request:

```bash
python adapter.py --source /path/to/witness.txt --prepare-reader \
  --output /path/to/new-request
```

This stops at `PREPARED_FOR_REASONER` and claims no analysis. Reader outputs do not
automatically become admitted findings or certified ministerial reports.

## Validation

```bash
python adapter.py --validate
python scripts/validate_foundational_architecture.py
STRAUSS_CUSTOS_ROOT=/path/to/custos python -m unittest discover -s tests -p 'test_*.py'
```

The existing Sanctum `prepare-request` boundary receives the same Reader context through
`adapter.build_context`. Sanctum repository pins continue to identify the Strauss commit
chosen by Sanctum; this change does not rewrite another repository's registry.
