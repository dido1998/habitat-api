# Domain Randomization

## Motivation
Deep RL are sample ineffecient and hence cannot be easily transferred from simulated environments to real environments. Domain randomization is one of the approaches used to tackle the sample ineffeciency of RL algorithms. Using domain randomization, we can create multiple variants of the same environment by randomizing certain properties of the environments(eg: lighting, camera angle, noise, sensor height etc.). When a Deep RL agent is trained on these variants of the simulated environment, it may consider the real environment as just another variant of the simulated environment. We also aim to explore whether agents trained with domain randomization outperform agents without domain randomization.

## Implementation
### Subdomains
In this implementation of domain randomization, we consider various subdomains which contain various properties that can be randomized. Each subdomain pertains to a different aspect of the environment. The subdomains and properties are as follows: 

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
- **Object Subdomain** : This subdomain allows placement of random number of objects at random navigable positions in the navmesh. It includes the following properties.
    - num_objects_range : [0, 10]
    - physics_config_file : This configuration file is used by `habitat-sim` to load the relevant objecs before-hand. If not specified, `habitat-sim` will use its default domain randomization file(link)[https://github.com/facebookresearch/habitat-sim/blob/master/data/default.phys_scene_config.json].
    
The properties of each subdomain are specified using `json` files in `configs/domain_randomization/subdomain_properties`. Users can modify the properties according to their needs and also specify their own `json` files containing properties for a subdomain. If a particular property is not specified the implementation will automatically always fall back to the original value of that property. The subdomains to be included in the current randomization process are specified in `configs/domain_randomization/default.domain_randomization_properties.json`. To check how to enable domain randomization see `configs/tasks/pointnav_dr.yaml` (just have to set `ENABLE=True`).

NOTE: Each property file also contains a property called `original_probability` which specifies the probability with which the original environment configuration will be samples for the given subdomain.

NOTE: The properties specified as `*_range` are ranges and whenever `env.reset()` is called a random value from the specified range is selected.


### Extending the domain randomization framework
Users may want to add more subdomains for randomization. For example, `habitat-sim` may soon include the functionality that makes materials configurable[(#506)](https://github.com/facebookresearch/habitat-sim/issues/506). Once this functionality is added we may have a material_subdomain that controls and randomizes the properties of materials. Addition of other subdomains and their properties is extremely simple and effortless and can be done in three steps:

- Create a `<subdomain_name>_subdomain.json` file in `configs/domain_randomization/subdomain_properties`. This file contains the properties of the subdomain and their possible values. For reference, check `configs/domain_randomization/subdomain_properties/light_subdomain.json`.
- Add `<subdomain_name>_subdomain.json` to `configs/domain_randomization/default.domain_randomization_properties.json`. 
- Implement `<subdomain_name>_subdomain.py` in `habitat/subdomains`. The subdomain is implemented as a class which extends `habitat.core.subdomain.Subdomain`. Each subdomain class must implement the `sample()` function which samples random values for each property in the subdomain and sets them in the environment. For reference, please check `habitat/subdomains/light_subdomain.py`. After this you should add the required import to `habitat/subdomain/registration.py`.


## Examples
The following examples demonstrates domain randmization. Each example for each subdomain has varying properties that are randomly selected everytime `env.reset()` is called.

### Sensor Subomain
 <p float="left">
  <img src="https://github.com/dido1998/habitat-api/blob/domain_randomization/habitat/subdomains/examples/sensor_1.png" width="300" />
  <img src="https://github.com/dido1998/habitat-api/blob/domain_randomization/habitat/subdomains/examples/sensor_6.png" width="300" /> 
  <img src="https://github.com/dido1998/habitat-api/blob/domain_randomization/habitat/subdomains/examples/sensor_3.png" width="300" />
</p>

###  Light Subdomain
<p float="left">
  <img src="https://github.com/dido1998/habitat-api/blob/domain_randomization/habitat/subdomains/examples/light_1.png" width="300" />
  <img src="https://github.com/dido1998/habitat-api/blob/domain_randomization/habitat/subdomains/examples/light_2.png" width="300" /> 
  <img src="https://github.com/dido1998/habitat-api/blob/domain_randomization/habitat/subdomains/examples/light_3.png" width="300" />
  
### Object Subdomain
<p float="left">
  <img src="https://github.com/dido1998/habitat-api/blob/domain_randomization/habitat/subdomains/examples/object_1.png" width="300" />
  <img src="https://github.com/dido1998/habitat-api/blob/domain_randomization/habitat/subdomains/examples/object_2.png" width="300" /> 
  <img src="https://github.com/dido1998/habitat-api/blob/domain_randomization/habitat/subdomains/examples/object_3.png" width="300" />


