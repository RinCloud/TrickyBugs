import os
import sys
import subprocess
import argparse
sys.path.append('.utils')
import utils.test

def runTest(program:str,test_dir:str,max_time:int,max_memory:int):
    checkRes,output=utils.test.test1sol1dir(program,test_dir,max_time,max_memory)
    short_output=utils.test.construct_short_out(program,test_dir,output)
    return output,short_output

def main(cwd):
    problemPath=os.path.join(cwd,'problems')
    parser = argparse.ArgumentParser()
    parser.add_argument('--program',type=str,required=True,help='The complete path of the program file to test. The program file should end with .cpp .java or .py.')
    parser.add_argument('--test_dir',type=str,required=True,help='The complete path of the test cases root dir. The spaces and newlines will be ignored. The test cases in the dir should be named as "1.in" "1.out" "2.in" "2.out" .... ')
    parser.add_argument('--max_time',type=float,default=20,help='The max time(seconds) for each test case. Default is 40 seconds.')
    parser.add_argument('--max_memory',type=float,default=4096,help='The max memory(MiB) for each test case. Default is 4096 MB.')
    parser.add_argument('--verbose',action='store_true',help='Whether show verbose test information.')
    args = parser.parse_args()

    print()
    print("Start Testing...")
    output,short_output=runTest(args.program,args.test_dir,args.max_time,args.max_memory)
    if args.verbose:
        real_output=output
    else:
        real_output=short_output
    print(real_output)

if __name__ == '__main__':
    #python ./main.py --program=./problems/p04005/buggy_programs/python/sol_65.py --test_dir=./problems/p04005/additional_test_cases

    #get current working directory
    scriptPath=os.path.dirname(__file__)
    problemPath = os.path.join(scriptPath, 'problems')
    if not os.path.exists(problemPath) :
        print(f'The data root directory {problemPath} is not found.')
        print("Please download the problems.tar.gz file and unzip it in the same directory as run.py.")
        print("Refer to README.md for more details.")
        exit()
    main(scriptPath)