# TrickyBugs Dataset
This is TrickyBugs, a dataset of corner-case bugs in plausible programs. TrickyBugs contains 3,043 human-written buggy programs from 324 real-world competition coding tasks. Please refer to the attached papers `Who Judges the Judge: An Empirical Study on Online Judge Tests` and `TrickyBugs: A Dataset of Corner-case Bugs in Plausible Programs` for more details.

To start with your exploration of the bugs, please first download all the files in this repo and put them in the same directory. Then download the `problems.tar.gz` file from either of the two links below:  

- **OneDrive**: [Download from OneDrive](https://1drv.ms/u/s!AqF1ATQsra1GiloFTbnHBeueaFmy)
- **Baidu Drive**: [Link](https://pan.baidu.com/s/1FTqNlaGSiyfx8FzhXxmUnA?pwd=isuq) , Extraction Code: isuq

And unzip the `problem.tar.gz` by the following command:

```bash
tar -zxvf problems.tar.gz
```

# File Structure


The `problems` directory contains root directories of each coding task, an each root directory is named as the `pid` of its coding task, which uniquely identifies the coding task within the dataset. 


The root directory of each coding task contains the following files and subdirectories:

- `buggy_programs`: A directory. This directory contains all the buggy plausible programs we found. Programs in different programming languages (C++, Java, or Python) are included in separate subdirectories. 
- `reference_programs`: A directory. This directory contains reference programs in C++. A reference program always produces the major output for any test input throughout the process of our differential testing. Reference programs are considered correct. We provide multiple reference programs (up to five) because they can be used for preliminary verification of the validity of an input. Specifically, for any given test input, if all reference programs produce the same output, then this test input is likely valid. Otherwise, it is highly probable to be invalid.
  
- `fixed_programs` (optional): A directory. This directory contains the fixed version of some buggy plausible programs. These fixed programs are useful for fault localization. It's important to note that many bugs in TrickyBugs originate from logical corner cases. Therefore, the differences between the buggy program and its fixed version may not be limited to just one line but could involve multiple lines. Not every buggy program has a fixed version, and 224 out of 324 root directories of coding tasks contain this subdirectory.
  
- `original_test_cases` (optional): A directory. This directory contains all the original test cases (input/output pairs) for the coding task on AtCoder, and 274 out of 324 root directories of coding tasks contain this subdirectory because AtCoder has not publicly disclosed the test cases for some earlier coding task. However, it is still possible and easy to determine whether a program passes the original test cases by submitting the code on AtCoder. The submission URL corresponding to the coding task is provided in the `pid_metainfo.json`. A plausible program, whether they are buggy or not, should pass all the original test cases.
  
- `additional_test_cases`: A directory. This directory contains the additional test cases that have uncovered bugs successfully. The additional. The mapping between additional test cases and the buggy plausible programs they uncover is provided in the `pid_metainfo.json`. A bug-free program should pass all the original and additional test cases.
  
- `metainfo.json`: A file. This file contains serval meta info of the coding tasks such as `URL` and `test_program_mapping`. `URL` is the source of this coding task, which contains all the information about this coding task except the original test cases, and the submission results on this website indicate whether a program has passed all the original test cases. The `test_program_mapping` displays the mapping between an additional test case and the buggy plausible programs it has identified.
  
- `problem_description.txt`: A file. The file contains the problem description, input constraints, and several pairs of input/output examples for this coding task. It is a file version of the content from the URL of the coding task and represents a detailed program specification for the corresponding programs.  

# Environments
To run the programs in the directory, we recommend the following environment:

   - Python: Python 3.8.2.
   - Java: OpenJDK 11.0.6.
   - C++: GCC 9.2.1 or Clang 10.0.0.

# Getting Started

Here is a detailed example to get familiar with the bugs :-)

For example, open a directory `./problems/p04005`, the description of the coding task is shown in `./problems/p04005/problem_description.txt`:

```
We have a rectangular parallelepiped of size A×B×C, built with blocks of size 1×1×1. Snuke will paint each of the A×B×C blocks either red or blue, so that:
* There is at least one red block and at least one blue block.
* The union of all red blocks forms a rectangular parallelepiped.
* The union of all blue blocks forms a rectangular parallelepiped.
Snuke wants to minimize the difference between the number of red blocks and the number of blue blocks. Find the minimum possible difference.

CONSTRAINTS:
* 2≤A,B,C≤10^9

INPUT:
The input is given from Standard Input in the following format:
A B C

OUTPUT:
Print the minimum possible difference between the number of red blocks and the number of blue blocks.
```

Then we pick a buggy plausible programs in Python `./problems/p04005/buggy_programs/python/65.py`:

```python
a, b, c = map(int,input().split())

if (a+b+c) % 2 == 1:
    print(min(a*b,b*c,c*a))
else:
    print(0)
```

Look at the `./problems/p04005/metainfo.json`. The json file shows that the URL of this coding task is:

```
https://atcoder.jp/contests/agc004/tasks/agc004_a
```

Copy the source code of `65.py` and submit it to AtCoder at:
```
https://atcoder.jp/contests/agc004/submit
```

Oh ! **It passes all the tests and gets a AC (Accepted)**. So why we call it **buggy**? Look at the `test_program_mapping` attribute of  `./problems/p04005/metainfo.json`:

```
{
    ...
    "test_program_mapping": {
        "test1.in": [

						...
            [
                "64.py",
                "python"
            ],
            [
                "65.py",
                "python"
            ],

            ...
        ]
        ...
    }
}
```



we find that `65.py` belongs to the list of `test1.in`. The content of `./problems/p04005/additional_test_cases/test1.in` is:

```
852362023 343017532 782366666
```

The description of the problem requests us to divide a cuboid with A x B x C blocks to minimize the difference between the number of blocks of the two parts. If there are two odd numbers and one even number among A,B,C, the answer should be `0`, so the content  of the corresponding test output `./problems/p04005/additional_test_cases/test1.out` is:

```
0
```

but when we sumbit the solution `65.py` in the [Atcoder custom test](https://atcoder.jp/contests/agc004/custom_test) and enter the `test1.in` as input, we get the a wrong output:

```
268365482890388312
```

So the `65.py` can pass the original test cases but can not pass the additional test cases, and we call it a **buggy plausible program**.

