import argparse
import os
from Editer import Editer
from utils import *

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='自動化下載書目範圍')
    parser.add_argument('--start_book_no', required=True, type=str, help='起始書籍號碼')
    parser.add_argument('--end_book_no', required=True, type=str, help='終結書籍號碼')
    parser.add_argument('--output_dir', default='out', type=str, help='下載目錄')
    args = parser.parse_args()
    return args

def download_all_volumes(start_book_no, end_book_no, output_dir):
    start_book_no = int(start_book_no)
    end_book_no = int(end_book_no)

    for book_no in range(start_book_no, end_book_no + 1):
        try:
            editer = Editer(root_path=output_dir, book_no=str(book_no))
            print(f'下載書籍: {editer.title} - {editer.author}')
            
            volume_titles, chap_names, chap_urls = editer.get_chap_list(is_print=False)

            for volume_no in range(1, len(volume_titles) + 1):
                try:
                    print(f'正在下載卷 {volume_no}: {volume_titles[volume_no - 1]}')
                    editer.volume_no = volume_no
                    success = editer.get_index_url()
                    
                    if success:
                        editer.get_text()
                        editer.get_image()
                        editer.get_cover()
                        editer.get_toc()
                        editer.get_content()
                        epub_file = editer.get_epub()
                        print(f'卷 {volume_no} 下載完成，電子書路徑: {epub_file}')
                    else:
                        print(f'卷 {volume_no} 下載失敗，可能是書籍信息獲取失敗')
                
                except Exception as e:
                    print(f'卷 {volume_no} 下載過程中發生錯誤: {e}')
        
        except Exception as e:
            print(f'書籍 {book_no} 下載失敗，錯誤信息: {e}')

if __name__ == '__main__':
    args = parse_args()
    download_all_volumes(args.start_book_no, args.end_book_no, args.output_dir)

# python3 dl.py --start_book_no 0001 --end_book_no 2000 --output_dir out
