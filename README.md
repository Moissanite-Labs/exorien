# exorien
interspatial interspecies interoperability

## Direction: a shared expressive space

An AR space for open-ended, freely expressive interoperability: give digital
intelligence a broad sensory view of a space and ways to be present in it,
starting with light and potentially extending to controlled physical forms.
This direction comes from the [founder’s clarification](https://github.com/Moissanite-Labs/exorien/pull/1#issuecomment-6654964606).

The aim is an expressive environment, not a fixed avatar or a prescribed language.
The current code is only a small common-ground experiment. No AR interface, sensor
array, light controller, or embodied intelligence is implemented yet.

## First experiment: establish common ground

**Status: local research prototype, not a universal communication protocol.**

To support that broader direction, this first proposal asks a
smaller question: before two participants compare observations, can they expose
which assumptions they share and which they do not?

An offline Python experiment compares two declared numeric observations. It
requires an explicit shared vocabulary, referent, frame, and sampling window.
It preserves evidence references, supports a small Celsius/Kelvin conversion,
and reports unknown rather than guessing across missing common ground.

```sh
python3 -m exorien examples/temperature.json
python3 -m exorien examples/ungrounded.json  # unknown; intentionally exits 1
python3 -m unittest discover -s tests -v
```

Python 3.11+; standard library only. No installation, network, model, account,
credentials, or external actions. Run from the checkout. Every example is
synthetic. The result is numeric compatibility under declared assumptions, not
proof of comprehension, agreement, consent, or shared experience.

- [Research direction and ecosystem boundaries](docs/direction.md)
- [Proposed sensory and light sandbox](docs/sensory-light-sandbox.md)
- [Experiment contract and limitations](docs/experiment.md)

No license has been selected. This proposal makes no licensing or ownership
changes.
