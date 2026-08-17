# Phase 2.1 benchmark: IMG_1493 rope removal

## Problem

The phase-2 person support removed plants, ground, and posts, but short parts of two black queue ropes remained because each rope physically crosses a leg, shoe, or skirt.

## Tested approach

1. Grounding DINO was prompted with `black queue rope`, `queue barrier`, `stanchion post`, and `black cord`.
2. Its labels localized the correct lower-image regions, but the returned boxes were too broad to subtract directly.
3. The two rope-region boxes were passed to SAM2.1 Hiera Small.
4. All three SAM2 variants were exported. In both regions, zero-based variant index `1` isolated the rope most accurately.
5. Only pixels at SAM2 probability `>= 0.5` were subtracted from the phase-2 Alpha. RGB remained untouched.

Approved benchmark boxes:

- Left rope: `123.3,697.7,587.9,935.2`
- Right rope: `622.2,837.9,1011.4,1161.3`

## Result

- Both visible rope arcs were removed.
- Source dimensions remained 1178 x 1165.
- RGB pixel lock passed.
- Removed pixels were 1.930883% of the input person foreground, below the 3% safety limit.
- Runtime on cached Apple MPS was about 10 seconds.
- Transparent gaps remain where the ropes occluded legs or the skirt; no hidden anatomy was generated.

## Revised aesthetic decision

The subtraction is technically accurate, but the result fails the group-wholeness and future-silhouette aesthetic gate: removing the foreground ropes creates distracting transparent cuts through legs and the long skirt. Reject the cleaned result for this photo and select the phase-2 retained-context Alpha instead.

Foreground removal is now diagnostic and explicit-opt-in only. Retain an occluding object by default when it is visibly in front of the group, deleting it would fragment the subject, or its shape contributes to the composition. Remove only detached residue or an object explicitly judged harmful after comparing both versions.
