# Hartogs' Extension Theorem

[< Back to Projects](/projects)

## Holomorphic Extension in Several Complex Variables

In one complex variable a function can be perfectly well behaved on an annulus and still admit no extension to the disc inside it. The standard example is $f(z) = 1/z$. In two or more variables that failure cannot occur. Hartogs' extension theorem, proved by Friedrich Hartogs in 1906, states that for $n > 1$ any holomorphic function on a polydisc with a smaller closed polydisc removed extends uniquely and holomorphically across the hole:

$$
f : B_\epsilon(0) \setminus \overline{B_{\epsilon'}(0)} \to \mathbb{C} \quad \text{extends to} \quad \hat{f} : B_\epsilon(0) \to \mathbb{C}
$$

This is an expository paper. It builds up holomorphicity in several variables from the Cauchy integral formula for polydiscs, proves the theorem, and then follows it to its stronger forms, drawing on Huybrechts for the foundations and on Simonič and Krantz for the generalizations.

The proof fixes all variables but one and expands the function as a Laurent series in the variable left free. A lemma establishing that a contour integral of a holomorphic function is again holomorphic makes the Laurent coefficients $a_n(w)$ holomorphic in the fixed variables. Near the outer boundary the function is defined on a full disc, so its negative coefficients vanish there, and the identity theorem forces them to vanish everywhere. What remains is a power series that converges inward, and the extension it defines is unique.

One consequence follows immediately and is worth stating on its own: a holomorphic function of several variables can have no isolated singularity and no isolated zero, since either could be translated to the origin and would contradict the theorem directly.

The second half of the paper surveys how much further the result can be pushed. Bochner's extension theorem replaces the polydisc with an arbitrary bounded domain and asks only that the function be holomorphic on some neighborhood of the boundary, however thin. The paper proves that this formulation and the general compact-hole version imply one another, and cites the literature for the proofs of the underlying theorems rather than reproving them. Further still, a CR function defined only on a $C^1$ boundary, satisfying the tangential Cauchy-Riemann equations, extends to a function holomorphic in the interior and continuous up to the boundary; that result is stated with a reference and not proved here. Together they express a theme running through complex analysis: the behavior of a holomorphic function on the boundary determines its behavior inside.

Written in December 2023.

### View the Full Paper

You can view the full paper below or [download it directly](/projects/hartogs/Hartogs__theorem.pdf).

```pdf
/projects/hartogs/Hartogs__theorem.pdf
```
