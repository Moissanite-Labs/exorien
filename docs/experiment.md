# Common-ground probe 0.1

This is a deliberately narrow executable experiment, not a production parser or
security boundary. `python3 -m exorien FILE` reads one local JSON object and writes
a JSON report to stdout. It does not dereference evidence identifiers.

## Input

- `version`: exactly `"0.1"`.
- `tolerance`: nonnegative decimal string, expressed in the normalized output unit.
- `observations`: exactly two objects from distinct named observers.
- Each observation has nonempty strings: `observer`, `evidence`, `vocabulary`,
  `quantity`, `referent`, `frame`, `window`, `unit`, plus decimal-string `value`.
- Identifiers are opaque and case-sensitive. The caller must establish what they
  mean. Matching identifiers are declarations, not authenticated or verified facts.
- Values are finite, at most 20 significant digits, within +/-1e12, and at most
  12 fractional places. These are experimental numeric bounds, not physical laws.

The vocabulary, quantity, referent, frame, and window must all match exactly.
A mismatch returns `unknown`; there is no inferred correspondence or frame
transform. For declared `temperature`, C and K normalize to kelvin using 273.15;
negative absolute temperature is rejected in this ordinary-temperature model.
Other identical unit identifiers permit direct numeric comparison under the
shared declarations. Different unsupported units return `unknown`.

## Output

- `comparable`: absolute numeric difference is within the supplied tolerance.
- `different`: common declarations permit comparison but the difference exceeds it.
- `unknown`: a declared context or unit correspondence is missing.
- `evidence`: unchanged identifiers for the original observations.
- `trace`: context mismatches or transformations and comparison limitations.
- `action_authorized`: always false; this probe grants no permissions.

Exit codes: 0 comparable; 1 different or unknown; 2 invalid input or file error.
Extra object fields are ignored and are not preserved as evidence. Tolerance is
not a statistical confidence measure. No error propagation, sensor calibration,
freshness verification, authenticated identity, transport, memory, autonomous
actuation, or species-specific adapter is implemented. Do not feed its result
into real-world actions as a consent or safety signal.

## Acceptance checks

The test suite exercises exact conversion, mismatched meaning/context, unsupported
units, disagreement, invalid values, preservation of evidence, no mutation of the
input, and CLI exit behavior. Successful tests establish those software behaviors
only, not a general capability to interpret another being's experience.
