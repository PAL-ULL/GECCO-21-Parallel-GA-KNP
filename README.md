
# First steps to solve the Algorithm Selection Problem through a Parallel Genetic Algorithm 

### Authors:

- Alejandro Marrero --- [@amarrerod](https://github.com/amarrerod)
- Eduardo Segredo --- [@esegredo](https://github.com/esegredo)
- Coromoto León --- [@cleon](https://github.com/coromoto)

### Abstract:
Deciding which optimisation technique to use for
solving a particular optimisation problem is an important and
arduous task that has been faced in the field of optimisation for
decades. The above problem is known as the Algorithm Selection
Problem (ASP). Many researchers have tried to solve the ASP
for a wide variety of problems. The optimisation techniques
considered in previous works have been, mainly, optimisation
techniques that can be executed in a fast manner. However, considering more sophisticated optimisation approaches for solving
the ASP, such as Evolutionary Algorithms, drastically increases
the computational cost involved. We are interested in solving
the ASP by considering different configurations of a Genetic
Algorithm (GA) applied to the well-known NP-hard 0/1 Knapsack
Problem (KNP). The above involves the execution of a significant
number of configurations of the said GA, in order to evaluate
their performance, when applied to a wide range of instances
with different features of the KNP, which is a computationally
expensive task. Therefore, the main aim of the current work is
to provide, as first step for solving the ASP, an efficient parallel
GA, which is able to attain competitive results, in terms of the
optimal objective value, in a short amount of time. Computational
results show that our approach is able to scale efficiently and
considerably reduces the average elapsed time for solving KNP
instances.


___
### [Paper](paper/)
### [Results](data/rankings/README.md)
### [Scalability Tables](data/scalability/README.md)
