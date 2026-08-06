# Expected Distance to the Nearest Face of an n-Cube

[< Back to Projects](/projects)

## Expected Distance of a Random Interior Point in an n-Dimensional Hypercube to its Nearest Facet

Select a point uniformly at random from the interior of the unit square. What is the expected distance from that point to the nearest edge? This paper works through the two and three dimensional cases and then solves the problem in general.

The method is to partition the cube into regions according to which face is nearest, then subdivide each region so that symmetry makes every piece integrate to the same value. An $n$-cube has $2n$ faces of dimension $n-1$, and the region belonging to each face splits further into $2^{n-1}(n-1)!$ congruent pieces. Evaluating a single piece and multiplying through gives

$$
\mathbb{E}[X] = \frac{1}{2(n+1)}
$$

which recovers $1/6$ for the square and $1/8$ for the cube.

The closed form also describes how volume distributes in high dimensions. Since $\mathbb{E}[X]$ strictly decreases in $n$, the proportion of the cube lying near its boundary must grow with dimension. That concentration is not itself a new observation, and the paper notes it can be reached more directly from the fact that $(1-\epsilon)^n \to 0$ for any fixed $\epsilon > 0$. What the expectation adds is a rate: because it falls off linearly in $n$, halving the expected distance to the boundary requires roughly doubling the dimension.

The problem came from my Math 170A final. I worked out the general case afterward. Written in July 2023.

### View the Full Paper

You can view the full paper below or [download it directly](/projects/expected_val/Expected_Distance_of_a_Random_Interior_Point_of_an_n_cube_to_its_nearest_face.pdf).

```pdf
/projects/expected_val/Expected_Distance_of_a_Random_Interior_Point_of_an_n_cube_to_its_nearest_face.pdf
```
