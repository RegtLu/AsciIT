import argparse
import os
import shutil

def delete(path:str):
    try:
        shutil.rmtree(f'{path}')
    except:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='删除')
    parser.add_argument('path', type=str, help='路径')
    args = parser.parse_args()
    delete(args.path)