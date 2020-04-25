# Domain Randomization

## Motivation
Deep RL are sample ineffecient and hence cannot be easily transferred from simulated environments to real environments. Domain randomization is one of the approaches used to tackle the sample ineffeciency of RL algorithms. Using domain randomization, we can create multiple variants of the same environment by randomizing certain properties of the environments(eg: lighting, camera angle, noise, sensor height etc.). When a Deep RL agent is trained on these variants of the simulated environment, it may consider the real environment as just another variant of the simulated environment. We also aim to explore whether agents trained with domain randomization outperform agents without domain randomization.

## Implementation
In this implementation of domain randomization, we consider various subdomains which contain various properties that can be randomized. Each subdomain pertains to a different aspect of the environment. The subdomains and properties are as follows (The properties specified as `*_range` are ranges and whenever `env.reset()` is called a random value from the specified range is selected):

- **Light Subdomain** : This subdomain controls and randomizes the lighting properties of the environment. The following light properties are included:
    - light position:
        - x_range : [-1.0, 1.0]
        - y_range : [-1.0, 1.0]
        - z_range : [-1.0, 1.0]
    - light color:
        - r_range : [0.9, 1.0]
        - g_range : [0.9, 1.0]
        - b_range : [0.0, 1.0]
        - a_range : [0.0, 1.0]
- **Sensor Subdomain** : This subdomain controls and randomizes sensor properties. The following sensor properties are included:
    - near_range : [0.01, 1.0]
    - far_range : [750, 1250]
    - hfov_range : [70, 130]
    - positionx_range : [0.0, 0.0]
    - positiony_range : [1.0, 2.5]
    - positionz_range : [0.0, 0.0]
    - orientationx_range : [-0.5, 0.5]
    - orientationy_range : [-0.5, 0.5]
    - orientationz_range : [0.0, 0.0]
    - noise_model : [`None`, `GaussianNoiseModel`, `PoissonNoiseModel`, `RedwoodDepthNoiseModel`, `SaltAndPepperNoiseModel`, `SpeckleNoiseModel`]
- **Agent Subdomain** : This subdomain controls and randomizes agent properties. The following agent properties are included:
    - height_range : [1.5, 2.5]
    - radius_range : [0.1, 2.1]
    - linear_acceleration_range : [10.0, 40.0]
    - angular_acceleration_range : [6.28, 18.84]
    - linear_friction_range : [0.1, 2.5]
    - angular_friction_range : [1.0, 2.0]
- **Action Space Subdomain** : This subdomain randomizes the properties of the actions taken by the government. These properties include:
    - forward_range : [0.05, 0.50]
    - turn_range : [5, 15]
- **Object Subdomain** : This subdomain allows placement of random number of objects at random navigable positions in the navmesh. It inccludes the following properties.
    - num_objects_range : [0, 10]
 
 
