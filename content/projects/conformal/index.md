# Conformal Invariance of Brownian Motion

[< Back to Projects](/projects)

## Lévy's Theorem, and a Probabilistic Proof of Liouville's Theorem

Conformal maps do not leave Brownian motion unchanged, but they come close in a precise way. Lévy's theorem states that if $f : U \to V$ is conformal and $B_t$ is a complex Brownian motion started at $z_0$, then $f(B_t)$ is again a complex Brownian motion, run on a different clock:

$$
f(B_t) = \tilde{B}_{\sigma(t)}, \qquad \sigma(t) = \int_0^t |f'(B_s)|^2 \, ds
$$

That time change is the substance of the theorem. Stated without it, the claim is false.

This is an expository paper. It assumes complex analysis and probability but no prior exposure to stochastic processes, and develops the theory it needs before proving the result, largely following Lawler's _Conformally Invariant Processes in the Plane_.

The obstacle to clear first is that Brownian paths are almost surely nowhere differentiable, so ordinary calculus cannot describe them. Quadratic variation is what replaces it, giving the identity $(dB_t)^2 = dt$ and, from that, Itô's formula. Conformal invariance then rests on two facts about a holomorphic $f = u + iv$. Harmonicity of $u$ and $v$ cancels the $dt$ term, leaving both as martingales, and their quadratic variation evaluates to $\int_0^t |f'(B_s)|^2 ds$, which is exactly the time change the Dubins-Schwarz theorem requires. The paper notes that conformality is stronger than the argument needs: any nonconstant holomorphic $f$ will do, since the zeros of $f'$ cannot accumulate.

A closing section runs the machinery in the other direction, deriving a complex analytic result from a probabilistic one. If $f$ were a bounded nonconstant entire function, then $f(B_t)$ would be a bounded Brownian motion, and Brownian motion is almost surely unbounded. Liouville's theorem follows without any appeal to Cauchy estimates.

Written in March 2024.

### View the Full Paper

You can view the full paper below or [download it directly](/projects/conformal/Conformal_Invariance_of_Brownian_Motion.pdf).

```pdf
/projects/conformal/Conformal_Invariance_of_Brownian_Motion.pdf
```
