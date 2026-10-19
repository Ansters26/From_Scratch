from concurrent import futures
from concurrency3 import save_flags, get_flag,main

def download_one(cc: str):
    image = get_flag(cc)
    save_flags(image,f'{cc}.gif')
    print(cc,end=' ',flush=True)
    return cc

def download_many(cc_list:list[str]):
    with futures.ThreadPoolExecutor() as executor:
        result = executor.map(download_one,sorted(cc_list))
    return len(list(result))

if __name__ == "__main__":
    main(download_many)
    