# Assignment 1 for MACS 30123

## Question 1 
`(a)` [see code in a1_1a.py] The original code took `3.64926815032959` to run and the numba-accelerated code took `0.28191637992858887` to run on a single core on Midway.

`(b)` [see code in a1_1b.py] The following figure plots the computation time for the 1,000 simulations (y-axis) against the number of cores for the particular run (x-axis). We can see that in general, computational time decreases when the number of cores increases, but there are fluctuations and the speedup is non-linear. The computation time first drops steeply as the number of mpi processes increases from 1 to 3, but the amount of acceleration flattens afterwards.

![Figure 2](https://github.com/lsc4ss-s21/assignment-1-YileC928/blob/main/a1_1b.png)

number of cores | computation time
--- | ---
1 | 0.4340555667877197
2 | 0.288053035736084 
3 | 0.19666218757629395 
4 | 0.14794468879699707 
5 | 0.12141728401184082 
6 | 0.10413551330566406 
7 | 0.09032034873962402 
8 | 0.08618783950805664 
9 | 0.07509398460388184 
10 | 0.06974077224731445 
11 | 0.06359076499938965 
12 | 0.06060457229614258 
13 | 0.060253143310546875 
14 | 0.054793357849121094 
15 | 0.053888559341430664 
16 | 0.05786919593811035 
17 | 0.04983878135681152 
18 |0.052588462829589844 
19 | 0.0486447811126709 
20 | 0.05004167556762695

`(c)` The speedup is not linear because: 

1. Part of the code is serial that cannot be parelleled. 
2. CPU solutions can be computation-bounded. When scaling up (using more cores), we have to deal with the communicate cost across processes.
3. Also, CPU solutions can be memory-bounded. For instance, memory bandwidth does not scale up with the processes.


## Question 2
`(a)` [see code in a1_2a.py] The code performing the grid search is a1_2a.py. It took `0.6546008586883545` seconds to to find the optimal ρ.

`(b)` The figure below plots the average number of periods to the first negative or zero health value zt ≤ 0 for each value of ρ.
![Figure 2](https://github.com/lsc4ss-s21/assignment-1-YileC928/blob/main/plot_a1_2b.png)

`(c)` The optimal persistence ρ is `-0.05251256281407035` and the corresponding average number of periods to negative health is `711.8014042126379`.

## Question 3
(For this question, I used a Pythonic Map Operation, a Elementwise Map solution would generate similar results.)

`(a)` [see my code a1_3a.py, sbatch in a1_3a.sbatch and output in a1_3a.out.] The seriel code took `0.04402518272399902` seconds, and the Opencl code took `0.04577493667602539` seconds. 

`(b)` As shown by the data in (a), the Opencl version does no better than the seriel version. I think the reason may be: though GPU are well-suited for large scale of repetitive calculations, transfer between GPU and CPU can be a bottleneck. In this case, data transfer cost may have offset the benefits of speeding up the NDVI calculation.

`(c)` [see code in a1_3a10.py and a1_3a20.py]
Increasing image size to 10x, the seriel version took `0.3214874267578125` seconds Opencl code took `0.2566795349121094` seconds.  Increasing image size to 20x, the seriel version took `0.6643545627593994` seconds Opencl code took `0.49678730964660645` seconds. 
 
The parallel solution performs progressively better in comparison to the serial solution as I increase the data size. 
The reason for this prograssive improvement is that when image data size increases, the task becomes more computationally intensive. So that the benefits of a GPU parallel solution outweigh the costs mentioned by (b).
