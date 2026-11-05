# Proposed sensory and light sandbox

**Status: design proposal, not implemented.** Grounded in the
[founder's direction](https://github.com/Moissanite-Labs/exorien/pull/1#issuecomment-6654964606).
The current runnable code remains the common-ground probe described in
[the experiment contract](experiment.md).

## What to make tangible next

A small virtual room that a digital participant can sense and express itself in.
The first output is light: spatial color, gradients, patterns, and geometry rather
than a mandatory humanoid avatar or a fixed set of emotional labels. An expression
can be exploratory or aesthetic; it need not be a command or translated sentence.

The design should leave the expressive space open while keeping the experiment
measurable. Initially a deterministic controller will exercise the loop. A model
can become a replaceable controller later; scripted behavior must not be presented
as a model choosing its own forms.

## A bounded first loop

1. Replay a **synthetic** room scene with a shared coordinate frame and clock.
2. Offer distinct visual, acoustic, thermal, and pressure event streams. Missing
   channels stay missing; we do not invent smell or taste from unrelated sensors.
3. Let a controller propose an expression using a virtual light field.
4. Validate it against the simulation's declared bounds and render it in a local
   preview. Validation is not a hardware safety certification or consent grant.
5. Record the input references, controller version, proposed expression, rejected
   proposals, and resulting scene so a run can be replayed and compared.

The simulator is a study of interfaces and expression. It cannot establish that
the participant is aware, experiencing the room, or understood by a human.

## Proposed records, not a standard

- **Observation:** source, channel, timestamp and time basis, frame, sample or local
  artifact reference, units where meaningful, calibration status, and uncertainty
  when actually known. Preserve raw observations separately from interpretations.
- **Interpretation:** cited observation IDs, proposed meaning, and unresolved
  alternatives. A generated label must not replace the source measurement.
- **Expression:** controller identity/version, input references, spatial primitives,
  colors, timing, and a finite duration. It may have a declared intent or none.
- **Scene result:** accepted/rejected expression, reason, rendered-state reference,
  and the simulation policy version. Keep proposal and effect distinct.

Do not build another transport protocol yet. Test whether these records explain
one encounter before considering integration with ABIOS or another carrier.

## Candidate acceptance checks

- A recorded synthetic scene and controller seed reproduce the same output.
- A missing, stale, or unregistered channel is marked explicitly, never silently
  substituted by a zero reading or an invented interpretation.
- Unit and coordinate-frame differences require a declared mapping. The existing
  common-ground probe can inform this contract but is not a multimodal adapter.
- The viewer distinguishes observations, interpretations, and expressive output.
- Invalid numeric values, out-of-room coordinates, and unlimited-duration commands
  are rejected; pause/reset returns the *simulated* output to a known state.
- The controller can create more than predefined icons or emotional categories.
- No camera, microphone, network service, physical light, motor, or actuator is
  accessed. The preview labels its inputs and outputs as synthetic.

## Physical and perceptual questions to keep honest

“Light collision” is a creative direction, not a settled optical mechanism.
Ordinary beams crossing in air do not by themselves create visible solid geometry.
AR overlays, surface projection, scattering media, volumetric displays, and
wave-optical effects are different routes with different constraints. Select and
validate one only after the virtual experiment makes the desired effect clearer.

A thermal sensor and a pressure sensor offer additional channels; they do not
by themselves reproduce human sensation. Smell and taste involve distinct
chemical measurement problems. A DLP analogy does not establish that a freely
reshaping material can be built, reversibly actuated, or safely inhabited.

Before any physical experiment: specify the site, people present, privacy and
recording choices, optical exposure and flicker constraints, mechanical limits,
independent stop controls, and the qualified review needed for the chosen hardware.
A model output must not directly become an unbounded actuator command. Those
limits protect the room without dictating what forms it is allowed to express
within the chosen medium. No hardware procurement or activation is proposed in
this increment.
