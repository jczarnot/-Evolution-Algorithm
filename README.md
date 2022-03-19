# -Evolution-Algorithm
Evolutionary Algorithm with different approaches to transform solutions
taking into account the limitations.

Repair methods used:
Resampling - rejection of a given solution and again
performing selections and mutations
Projection - if any coordinate has crossed the boundary of the domain it is
projected onto this border
Reflection - if any coordinate has exceeded the boundary of the domain
we replace it with a "mirror image" of the appropriate border
Wrapping - we shift the coordinate which has crossed the boundary of the domain by
multiple of the domain size
