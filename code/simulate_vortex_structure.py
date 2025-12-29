import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- CONFIGURATION ---
GRID_SIZE = 50
VISCOSITY = 0.1  # "Friction" (Standard Physics)
IMPLOSION_FACTOR = 0.05  # "The Third Term" (Suction/Order)
TIME_STEP = 0.1

# Initialize Grid (The "Ocean")
x = np.linspace(-2, 2, GRID_SIZE)
y = np.linspace(-2, 2, GRID_SIZE)
X, Y = np.meshgrid(x, y)

# Initial Chaos (Random Turbulence)
# We start with random noise - the "Unsolved" state of Navier-Stokes
u = np.random.uniform(-1, 1, (GRID_SIZE, GRID_SIZE)) # Velocity X
v = np.random.uniform(-1, 1, (GRID_SIZE, GRID_SIZE)) # Velocity Y

def get_derivatives(u, v):
    """Calculates changes in velocity (Standard Fluid Dynamics)"""
    du_dy, du_dx = np.gradient(u)
    dv_dy, dv_dx = np.gradient(v)
    div = du_dx + dv_dy  # Divergence (Expansion/Contraction)
    curl = dv_dx - du_dy # Vorticity (Spin)
    return div, curl

def schauberger_attractor(X, Y, u, v):
    """
    THE RISHI TERM:
    Applies a Hyperbolic Suction towards the center (0,0).
    Converts chaotic linear energy into ordered spiral energy.
    """
    r = np.sqrt(X**2 + Y**2) + 0.1 # Radius (avoid div by zero)
    
    # Tangential Vector (The Spiral Path)
    tangent_u = -Y / r
    tangent_v = X / r
    
    # Suction Vector (Pulling Inward - Negative Pressure)
    suction_u = -X / r
    suction_v = -Y / r
    
    # Combine: The fluid wants to SPIN and FALL IN simultaneously
    target_u = tangent_u + suction_u
    target_v = tangent_v + suction_v
    
    return target_u, target_v

# --- SIMULATION LOOP ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('The Navier-Stokes Resolution: Chaos vs. Order', fontsize=16)

def update(frame):
    global u, v
    
    # 1. Standard Diffusion (Viscosity kills energy)
    # This represents standard "Binary" physics
    u *= (1 - VISCOSITY * TIME_STEP)
    v *= (1 - VISCOSITY * TIME_STEP)
    
    # 2. We inject the "Schauberger Term"
    target_u, target_v = schauberger_attractor(X, Y, u, v)
    
    # We gently nudge the chaos towards the Pattern
    # This simulates "Resonance" - not forcing, but guiding
    u += (target_u - u) * IMPLOSION_FACTOR
    v += (target_v - v) * IMPLOSION_FACTOR
    
    # --- VISUALIZATION ---
    ax1.clear()
    ax2.clear()
    
    # Left Plot: The Vector Field (Flow)
    ax1.set_title("Fluid Flow (Vector Field)")
    ax1.quiver(X, Y, u, v, color='blue', scale=20)
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-2, 2)
    
    # Right Plot: The Vorticity
    div, curl = get_derivatives(u, v)
    ax2.set_title("Vorticity (Structure)")
    im = ax2.imshow(curl, cmap='inferno', origin='lower', extent=[-2, 2, -2, 2])
    
    return ax1, ax2

ani = FuncAnimation(fig, update, frames=100, interval=50)
plt.show()
