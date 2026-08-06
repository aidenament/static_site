# Hartogs' Extension Theorem

[< Back to Projects](/projects)

## Why a Function of Several Variables Has No Isolated Singularities

In one complex variable a function can be perfectly well behaved on an annulus and still admit no extension to the disc inside it. $f(z) = 1/z$ is the standard example. In two or more variables that cannot happen. Hartogs proved in 1906 that for $n > 1$, any holomorphic function on a polydisc with a smaller closed polydisc removed extends uniquely and holomorphically across the hole:

$$
f : B_\epsilon(0) \setminus \overline{B_{\epsilon'}(0)} \to \mathbb{C} \quad \text{extends to} \quad \hat{f} : B_\epsilon(0) \to \mathbb{C}
$$

A holomorphic function of several variables therefore has no isolated singularities and no isolated zeros. Either could be translated to the origin, where it would contradict the theorem directly.

This is an expository paper. It builds up holomorphicity in several variables from the Cauchy integral formula for polydiscs, proves the theorem, then follows it to its stronger forms, drawing on Huybrechts for the foundations and on Simonič and Krantz for the generalizations.

The proof fixes all variables but one and expands the function as a Laurent series in the variable left free. A lemma establishing that a contour integral of a holomorphic function is again holomorphic makes the Laurent coefficients $a_n(w)$ holomorphic in the fixed variables. Near the outer boundary the function is defined on a full disc, so its negative coefficients vanish there, and the identity theorem forces them to vanish everywhere. What remains is a power series that converges inward, and the extension it defines is unique.

The second half surveys how much further the result can be pushed. Bochner's extension theorem replaces the polydisc with an arbitrary bounded domain and asks only that the function be holomorphic on some neighborhood of the boundary, however thin. The paper proves that this formulation and the general compact-hole version imply one another. Push it further and the domain shrinks to the boundary itself: a CR function on a $C^1$ boundary, satisfying the tangential Cauchy-Riemann equations, extends to a function holomorphic in the interior and continuous up to the boundary. Those underlying theorems are cited, not reproved. In every version, the boundary decides what happens inside.

I picked this up out of Huybrechts in my last year at UCLA and wrote it up in December 2023.

### The Full Paper

Read it below, or [download it directly](/projects/hartogs/Hartogs__theorem.pdf).

```pdf
/projects/hartogs/Hartogs__theorem.pdf
```
