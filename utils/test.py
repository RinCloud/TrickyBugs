import subprocess
import os
import shutil
from . import tool
COMPILE_ERROR="COMPILE_ERROR"
RUN_ERROR="RUN_ERROR"
TIME_OUT="TIME_OUT"


def run_cmd(command, timeout=20):
    
    try:
        result = subprocess.run(command,text=True,shell=True,capture_output=True,encoding='utf-8', timeout=timeout)
    except subprocess.TimeoutExpired as time_e:
        print(f"TIMEOUT when running: {str(time_e)}")
        return TIME_OUT, None,None
    except Exception as e:
        print(f"ERROR when running: {str(e)}")
        return RUN_ERROR, None,None
    return result.returncode, result.stdout,result.stderr

def run_prog_with_input(execute_cmd, input_file,timeout_=20):
    
    try:
        with open(input_file,"r") as fin:
            result = subprocess.run(execute_cmd, stdin=fin,text=True,capture_output=True, timeout=timeout_)
    except subprocess.TimeoutExpired as time_e:
        print(f"TIMEOUT when running: {str(time_e)}")
        return TIME_OUT, None,None
    except Exception as e:
        print(f"ERROR when running: {str(e)}")
        return RUN_ERROR, None,None
    return result.returncode, result.stdout,result.stderr

def compile(file:str):
    
    if file.endswith('.cpp'):
        out_file = file.replace('.cpp', '.out')
        if not os.path.exists(out_file):
            compile_command = f"g++ {file} -o {out_file}"
            subprocess.check_call(compile_command, shell=True)
    elif file.endswith('.java'):
        out_file = file.replace('.java', '.class')
        if not os.path.exists(out_file):
            compile_command = f"javac {file}"
            subprocess.check_call(compile_command, shell=True)
    else:
        raise Exception("Error argument: file. The file should be path of .cpp .java file.")


def test1sol1dir(sol_file:str,test_dir:str,max_time=20,max_memory=4096):
    '''
    problems_dir: the root dir of all problems
    pid: the pid of the coding task
    sol_path: the complete path of .cpp or .py or .java file
    test_dir: the complete path of the test cases root dir
    '''
    
    if sol_file.endswith(".cpp"):
        lang="cpp"
    elif sol_file.endswith(".py"):
        lang="python"
    elif sol_file.endswith(".java"):
        lang="java"
    else:
        raise RuntimeError("The file name should ends with .cpp or .java or .py")
    
    tmp_file_list=[]
    tmp_dir_list=[]
    if lang=='cpp':
        exec_file_path=sol_file.replace(".cpp",".out")
        if not os.path.exists(exec_file_path):
            compile(sol_file)
        tmp_file_list.append(exec_file_path)
    elif lang=='python':
        exec_file_path=sol_file
    elif lang=='java':
        file_dir=os.path.dirname(sol_file)
        file_name=os.path.basename(sol_file)
        tmp_dir=os.path.join(file_dir,'tmp_java')
        tmp_dir_list.append(tmp_dir)
        if not os.path.exists(tmp_dir):
            os.mkdir(tmp_dir)
        exec_file_path=os.path.join(tmp_dir,'Main.class')
        tmp_java_file=os.path.join(tmp_dir,'Main.java')
        shutil.copy(sol_file,tmp_java_file)
        tmp_file_list.append(tmp_java_file)
        tmp_file_list.append(exec_file_path)
        if not os.path.exists(exec_file_path):
            compile(tmp_java_file)
    

    if not os.path.exists(exec_file_path):
        raise RuntimeError("Can not get executable file")
    if lang=='cpp':
        test_cmd=f'oj t -c "{exec_file_path}" -d {test_dir} -N --mle {max_memory} -t {max_time}'
    elif lang=='python':
        test_cmd=f'oj t -c "python {exec_file_path}" -d {test_dir} -N --mle {max_memory} -t {max_time}'
    elif lang=='java':
        test_cmd=f'oj t -c "java -classpath {tmp_dir} Main" -d {test_dir} -N --mle {max_memory} -t {max_time}'
    
    try:
        res=""
        code, output,err = run_cmd(test_cmd)

        if "test success" in output:
            res = "AC"
        elif "[FAILURE] TLE" in output:
            res ="TLE"
        elif "test failed" in output:
            res = "WA"
        else:
            raise RuntimeError(f"Error when testing, Error message:\n{output}")
    except subprocess.TimeoutExpired:
        res='TLE'
    except Exception as e:
        if res!="TLE" and res!="WA" :
            res='Er'
    for to_del_file in tmp_file_list:
        os.remove(to_del_file)
    for to_del_dir in tmp_dir_list:
        os.rmdir(to_del_dir)

    return res,output

def construct_short_out(program,test_dir,output):
    
    content=""
    content=content+f"Program Under Test: {program}\n"
    content=content+f"Test Cases Directory: {test_dir}\n"
    content=content+f"Test Results:\n"

    test_files=tool.find_paths(test_dir,type_="file",suffix=".in")
    test_name_list=[]
    for test_file in test_files:
        test_name_list.append(os.path.basename(test_file).split('.')[0])

    lines=output.split('\n')
    stack=[]
    for line in lines:
        if not "(for" in line:
            line_list=line.split(' ')
            for test_name in test_name_list:
                if test_name in line_list:
                    stack.append(test_name)
        if '[SUCCESS] AC' in line:
            res='AC'
        elif '[FAILURE]' in line:
            res=line.split(' ')[1].strip(':,')
        else:
            continue
        if (len(stack)>0):
            this_test_name=stack.pop()
            content=content+f"{this_test_name}: {res}\n"
    return content