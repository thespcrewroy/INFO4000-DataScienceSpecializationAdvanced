# Physics Informed Neural Networks (PINNs)

## What Are PINNs?

Imagine two students predicting the path of a thrown ball:

- **The standard student (a regular neural network)** has seen some examples and finds a pattern in them. Ask about a throw from a new spot and it can only guess, because it doesn't understand the physics behind the pattern.
- **The smart student (a physics informed neural network)** has seen a few examples and also studied the laws of gravity and motion. Even with limited data, its answers have to follow those laws, so its predictions are much more accurate.

A PINN is a neural network trained to respect the laws of physics. The broader idea, building any known scientific theory into training, is sometimes called a theory informed neural network (TINN).

### Why It Works

A standard neural network's test has one question: how well did you match the data? A PINN's test has two: how well did you match the data, and how well did you follow the laws of physics? It tries to score well on both.

**Applications:**

- **Weather forecasting:** using the equations of atmospheric fluid dynamics along with past weather data
- **Engineering and design:** simulating airflow over a new airplane wing faster than traditional methods
- **Healthcare:** modeling blood flow in arteries or how a drug spreads through the body
- **Ball trajectories:** predicting where a ball will go from only a few data points, because the model understands gravity

### Strengths and Challenges

| Strengths | Challenges |
|---|---|
| Need less data, since they already "know" the physics | Training can take a lot of computing power |
| Handle problems that are hard for traditional methods, like complex shapes or incomplete information | The physics has to be known, and if our understanding is wrong, the predictions will be too |
| Simulations much faster than traditional physics simulators | Very complex physics can be too hard to write into the loss |

## Example: Lake Temperature

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/8-1.jpg"/>
</p>

> The General Lake Model: lake water temperature depends on many physical processes, including heating of the surface by incoming shortwave radiation from the sun, that radiation weakening (attenuating) as it goes deeper, mixing between layers at different depths, and heat leaving the surface through evaporation and longwave radiation. The task is to predict water temperature as a function of depth and time, which matters for understanding how climate change affects lakes and for managing water resources. One known law: the relationship between temperature and density is known, and deeper water should be denser. If the model predicts higher density for a point closer to the surface than for a deeper point, that prediction is physically inconsistent, so the model is penalized through its cost function.

## The Loss Function

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/8-2.jpg"/>
</p>

> How a PINN trains: a neural network takes position $x$ and time $t$ as inputs and outputs $u$. Automatic differentiation then computes the derivatives $\frac{\partial u}{\partial t}$, $\frac{\partial u}{\partial x}$, and $\frac{\partial^2 u}{\partial x^2}$, and plugs them into the governing PDE, here $\frac{\partial u}{\partial t} + u \frac{\partial u}{\partial x} - \nu \frac{\partial^2 u}{\partial x^2} = 0$ (Burgers' equation, where $\nu$ is viscosity). Anything other than zero is a physics error. The data loss (MSE against known data points) and the physics loss are combined into the total loss. If it is below a tolerance $\varepsilon$, training is done, and if not, the network's weights are updated and the loop repeats.

## Building a PINN

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/8-3.jpg"/>
</p>

> Physics based vs. data based models: a physics based model turns data into output by following known equations, while a data based model learns from data to make predictions. A PINN feeds both the data and the physics based model's knowledge into the data based model, so its predictions match observations and obey the physics.

**Example: the heat equation.** For heat spreading along a metal rod, the temperature $u(x, t)$ at position $x$ and time $t$ follows

$$
\frac{\partial u(x, t)}{\partial t} = \alpha \frac{\partial^2 u(x, t)}{\partial x^2}
$$

where $\alpha$ is the thermal diffusivity, a constant for the material. This is also called the diffusion equation. To build a PINN for it:

1. Create a neural network with inputs $x$ and $t$ and output $u(x, t)$
2. Train it to match any known temperatures, such as the initial condition (the rod at $t = 0$) or the boundary conditions (the ends of the rod)
3. Add a physics term to the loss that forces the network to respect the heat equation, using the residual $\frac{\partial u}{\partial t} - \alpha \frac{\partial^2 u}{\partial x^2}$, which should be 0
4. Compute those derivatives with PyTorch's automatic differentiation
5. Minimize the total loss, data loss plus physics loss

## Example: RC Circuit

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/8-4.jpg"/>
</p>
<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/8-5.jpg"/>
</p>

> Resistor capacitor (RC) circuit: a resistor R and a capacitor C are connected in series to a voltage source $V_s$. When the switch closes, a step input voltage $V(t) = V_0$ starts charging the capacitor from 0 V (the initial condition $V_C(0) = 0$). The capacitor voltage rises quickly during the transient period, reaches about 63% of the source voltage after one time constant $\tau = RC$, and levels off at the steady state after about $5\tau$. The PINN's job is to predict $V_C(t)$, and its physics loss comes from the governing equation $V(t) = V_C(t) + RC \frac{dV_C(t)}{dt}$.

## Class Exercise: Newton's Law of Cooling

<p align="left">
  <img src="https://github.com/thespcrewroy/INFO4000-DataScienceSpecializationAdvanced/blob/main/Notes/assets/8-6.jpg"/>
</p>

> Newton's law of cooling: a hot object, like a cup of coffee, loses heat to its surroundings at a rate proportional to the temperature difference, $\frac{dT}{dt} = -k(T - T_s)$, where $T$ is the object's temperature, $T_s$ is the surroundings (room) temperature, and $k$ is the cooling constant. The temperature drops quickly at first and then levels off toward room temperature. It's a first order ODE.

You measured a cup of coffee's temperature at minutes 0, 10, and 30 and want a neural network that predicts its temperature at any minute.

- **With a standard neural network,** the input is $t$, the output is the predicted temperature $\hat{T}$, and the loss is the MSE against the 3 measurements. With only 3 points, the network has no idea what happens between minutes 10 and 30, and it can fit any curve through those points, even ones that rise or wiggle.
- **With a PINN,** the loss adds a physics term that forces $\hat{T}$ to obey the law of cooling everywhere, not just at the measured points:

$$
\text{Loss}_{physics} = \text{mean}\left( \frac{d\hat{T}}{dt} + k(\hat{T} - T_{env}) \right)^2
\qquad
\text{Loss}_{total} = \text{Loss}_{data} + \lambda \cdot \text{Loss}_{physics}
$$

- **If the room temperature isn't constant,** $T_{env}$ can be given as a function of time $T_{env}(t)$, either as an extra network input or from measurements plugged into the physics loss.

## PyTorch Automatic Differentiation

PINNs put the governing ODEs or PDEs into the loss function, and checking them requires the derivatives of the network's output with respect to its inputs. Automatic differentiation gives exact derivatives, unlike numerical methods such as finite differences, which only approximate them and can be computationally expensive.

PyTorch's `torch.autograd` module computes derivatives automatically for any tensor created with `requires_grad=True`. Neural networks already use it for backpropagation, and PINNs use it to get first and second order partial derivatives of the output with respect to the inputs.

```python
import torch

x = torch.tensor(2.0, requires_grad=True)
y = x ** 3

dy_dx = torch.autograd.grad(y, x, create_graph=True)[0]  # 3x^2 = 12
d2y_dx2 = torch.autograd.grad(dy_dx, x)[0]               # 6x = 12
```

`create_graph=True` keeps track of the first derivative's computation so it can be differentiated again for the second derivative.

**The physics loss for the heat equation:**

```python
def physics_loss(model, x, t, alpha):
    x.requires_grad_(True)
    t.requires_grad_(True)
    u = model(torch.cat([x, t], dim=1))

    ones = torch.ones_like(u)
    u_t = torch.autograd.grad(u, t, ones, create_graph=True)[0]
    u_x = torch.autograd.grad(u, x, ones, create_graph=True)[0]
    u_xx = torch.autograd.grad(u_x, x, torch.ones_like(u_x), create_graph=True)[0]

    residual = u_t - alpha * u_xx  # should be 0 if the physics is followed
    return (residual ** 2).mean()

# total_loss = data_loss + lam * physics_loss(model, x_points, t_points, alpha)
```

The `x` and `t` points for the physics loss don't need measured temperatures, since the equation itself is the target. They can be sampled anywhere in the rod and time range.

## Worked Examples

### Total Loss

$$
\text{Loss}_{total} = \text{Loss}_{data} + \lambda \cdot \text{Loss}_{physics}
$$

$\lambda$ sets how much the physics counts compared with the data. Suppose a model has Loss_data = 0.04 and Loss_physics = 0.5:

| $\lambda$ | Calculation | Total loss | Effect |
|---|---|---|---|
| 0.1 | $0.04 + 0.1 \times 0.5$ | 0.09 | Mostly about matching the data |
| 1 | $0.04 + 1 \times 0.5$ | 0.54 | Physics errors dominate, pushing the model to fix them |
| 0 | $0.04 + 0 \times 0.5$ | 0.04 | Physics ignored, so it's just a standard neural network |

### Checking the Heat Equation Residual

The residual is $r = \frac{\partial u}{\partial t} - \alpha \frac{\partial^2 u}{\partial x^2}$, and the physics loss is the average of $r^2$.

**A prediction that breaks the physics:** say the network outputs $u(x, t) = x^2 + t$ with $\alpha = 1$

$$
\frac{\partial u}{\partial t} = 1
\qquad
\frac{\partial u}{\partial x} = 2x
\qquad
\frac{\partial^2 u}{\partial x^2} = 2
$$

$$
r = 1 - 1 \times 2 = -1
\qquad
\text{physics loss} = (-1)^2 = 1
$$

The residual isn't 0 anywhere, so this function doesn't describe real heat flow, and training pushes the network away from it.

**A prediction that follows the physics:** $u(x, t) = e^{-\alpha \pi^2 t} \sin(\pi x)$, a sine shaped temperature profile that fades over time

$$
\frac{\partial u}{\partial t} = -\alpha \pi^2 u
\qquad
\frac{\partial^2 u}{\partial x^2} = -\pi^2 u
$$

$$
r = -\alpha \pi^2 u - \alpha(-\pi^2 u) = 0
$$

The residual is exactly 0 everywhere, so the physics loss is 0.

### Lake Density Penalty

Deeper water should be denser. For two points at depths $d_1 < d_2$, a simple penalty is

$$
\text{penalty} = \max\big(0, \ \rho(d_1) - \rho(d_2)\big)
$$

which is 0 when the deeper point is denser (physically consistent) and positive when it isn't.

| Shallow point (2 m) | Deep point (8 m) | Penalty | Consistent? |
|---|---|---|---|
| 999.5 kg/m³ | 999.8 kg/m³ | $\max(0, -0.3) = 0$ | Yes |
| 999.8 kg/m³ | 999.5 kg/m³ | $\max(0, 0.3) = 0.3$ | No, so the cost function is penalized |

Adding this penalty (often squared, $0.3^2 = 0.09$) to the loss steers the model away from predictions that break the known relationship.

### RC Circuit Charging

For a step input $V_0$ and an uncharged capacitor, the solution to $V_0 = V_C + RC \frac{dV_C}{dt}$ is

$$
V_C(t) = V_0 \left( 1 - e^{-t/\tau} \right)
\qquad
\tau = RC
$$

**Example:** $R = 1000 \ \Omega$ and $C = 0.001$ F give $\tau = 1000 \times 0.001 = 1$ second. With $V_0 = 5$ V:

| Time | Calculation | $V_C$ | Share of $V_0$ |
|---|---|---|---|
| $t = 0$ | $5(1 - e^{0})$ | 0 V | 0% |
| $t = \tau = 1$ s | $5(1 - e^{-1})$ | ≈ 3.16 V | ≈ 63% |
| $t = 5\tau = 5$ s | $5(1 - e^{-5})$ | ≈ 4.97 V | ≈ 99% |

**Checking the physics:** $\frac{dV_C}{dt} = \frac{V_0}{\tau} e^{-t/\tau}$, so

$$
V_C + RC \frac{dV_C}{dt} = V_0 - V_0 e^{-t/\tau} + \tau \cdot \frac{V_0}{\tau} e^{-t/\tau} = V_0
$$

The equation holds at every $t$, so a PINN predicting this curve has a physics loss of 0.

### Newton's Law of Cooling: Why the Physics Helps

Suppose the real coffee follows $T(t) = 20 + 70 e^{-0.1t}$ (room at 20°C, starting at 90°C, $k = 0.1$ per minute). The three measurements are:

| Minute | 0 | 10 | 30 |
|---|---|---|---|
| Temperature | 90°C | ≈ 45.75°C | ≈ 23.49°C |

**What a data only model might predict at minute 20:** a straight line between minutes 10 and 30 gives $\hat{T}(20) \approx 34.62$°C, with a slope of $\frac{23.49 - 45.75}{20} \approx -1.11$°C per minute.

**Checking it against the physics:** at 34.62°C, the law of cooling says the slope should be

$$
\frac{dT}{dt} = -0.1 (34.62 - 20) \approx -1.46 \text{ °C per minute}
$$

The residual is $-1.11 - (-1.46) \approx 0.35$, not 0, so the physics loss penalizes this guess. The true value at minute 20 is $20 + 70e^{-2} \approx 29.47$°C, and the physics loss is what pulls the PINN toward it, even though minute 20 was never measured.

### Checking an ODE With Autograd

The slides practice differentiation on the equation $\frac{dx}{dt} = t \frac{d^2 x}{dt^2}$. Try $x(t) = t^2$:

$$
\frac{dx}{dt} = 2t
\qquad
\frac{d^2 x}{dt^2} = 2
\qquad
t \cdot 2 = 2t
$$

Both sides match, so the residual $\frac{dx}{dt} - t \frac{d^2 x}{dt^2}$ is 0. In PyTorch:

```python
import torch

t = torch.tensor(3.0, requires_grad=True)
x = t ** 2

dx_dt = torch.autograd.grad(x, t, create_graph=True)[0]  # 2t = 6
d2x_dt2 = torch.autograd.grad(dx_dt, t)[0]               # 2
residual = dx_dt - t * d2x_dt2                           # 6 - 3*2 = 0
```

