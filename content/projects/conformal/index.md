# Conformal Invariance of Brownian Motion

[< Back to Projects](/projects)

## Lévy's Theorem, and a Probabilistic Proof of Liouville's Theorem

Push a complex Brownian motion through a conformal map and what comes out is a Brownian motion again, running on a different clock. That's Lévy's theorem: if $f : U \to V$ is conformal and $B_t$ is a complex Brownian motion started at $z_0$, then

$$
f(B_t) = \tilde{B}_{\sigma(t)}, \qquad \sigma(t) = \int_0^t |f'(B_s)|^2 \, ds
$$

That time change is the substance of the theorem. Stated without it, the claim is false.

This is an expository paper. It assumes complex analysis and probability but no prior exposure to stochastic processes, and develops the theory it needs before proving the result, largely following Lawler's _Conformally Invariant Processes in the Plane_. The last section turns the theorem around and gets Liouville's theorem out of it.

Brownian paths are almost surely nowhere differentiable, so ordinary calculus can't describe them. Quadratic variation is what replaces it, giving the identity $(dB_t)^2 = dt$ and, from that, Itô's formula.

From there, conformal invariance rests on two facts about a holomorphic $f = u + iv$. Harmonicity of $u$ and $v$ kills the $dt$ term, leaving both as martingales. Their quadratic variation evaluates to $\int_0^t |f'(B_s)|^2 ds$, which is exactly the time change Dubins-Schwarz needs. Conformality is more than the argument uses: any nonconstant holomorphic $f$ will do, since the zeros of $f'$ cannot accumulate.

The closing section runs the machinery backwards. If $f$ were a bounded nonconstant entire function, then $f(B_t)$ would be a bounded Brownian motion, and Brownian motion is almost surely unbounded. Liouville's theorem falls out, with no Cauchy estimates anywhere.

Written in March 2024, during the complex analysis course I took with Professor Tao.

### The Full Paper

Read it below, or [download it directly](/projects/conformal/Conformal_Invariance_of_Brownian_Motion.pdf).

```pdf
/projects/conformal/Conformal_Invariance_of_Brownian_Motion.pdf
```
