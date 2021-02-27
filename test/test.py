import numpy as np
from pysr import pysr, sympy2jax
from jax import numpy as jnp
from jax import random
from jax import grad
import sympy
X = np.random.randn(100, 5)

print("Test 1 - defaults; simple linear relation")
y = X[:, 0]
equations = pysr(X, y,
                 niterations=10,
                 user_input=False)
print(equations)
assert equations.iloc[-1]['MSE'] < 1e-4

print("Test 2 - test custom operator")
y = X[:, 0]**2
equations = pysr(X, y,
                 unary_operators=["sq(x) = x^2"], binary_operators=["plus"],
                 extra_sympy_mappings={'square': lambda x: x**2},
                 niterations=10,
                 user_input=False)
print(equations)
assert equations.iloc[-1]['MSE'] < 1e-4

X = np.random.randn(100, 1)
y = X[:, 0] + 3.0
print("Test 3 - empty operator list, and single dimension input")
equations = pysr(X, y,
                 unary_operators=[], binary_operators=["plus"],
                 niterations=10,
                 user_input=False)
print(equations)
assert equations.iloc[-1]['MSE'] < 1e-4

print("Test 4 - text JAX export")
x, y, z = sympy.symbols('x y z')
cosx = 1.0 * sympy.cos(x) + y
key = random.PRNGKey(0)
X = random.normal(key, (1000, 2))
true = 1.0 * jnp.cos(X[:, 0]) + X[:, 1]
f, params = sympy2jax(cosx, [x])
assert jnp.all(jnp.isclose(f(X, params), true)).item()
